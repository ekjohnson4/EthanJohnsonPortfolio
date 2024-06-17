from flask import render_template, Flask, url_for, session, request, redirect
from utilities import render_template_wrapper
from settings import PORT
from spotipy.oauth2 import SpotifyOAuth
import requests
import time

render_template = render_template_wrapper(render_template)
SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
SPOTIFY_GET_RECENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/recently-played'

app = Flask(__name__)
app.secret_key = "xxxxxx"


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth("user-read-recently-played")
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/properties', methods=['GET', 'POST'])
def properties():
    return render_template('properties.html')


@app.route('/music', methods=['GET', 'POST'])
def music():
    return render_template('music.html', track_info='')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# @app.route('/music', methods=['GET', 'POST'])
# def music():
#     sp_oauth = create_spotify_oauth("user-read-recently-played")
#     session.clear()
#     code = request.args.get('code')
#     token_info = sp_oauth.get_access_token(code)
#     session["token_info"] = token_info
#
#     session['token_info'], authorized = get_token("user-read-recently-played")
#     session.modified = True
#     if not authorized:
#         return redirect('/login')
#
#     track_info = get_recent_track(
#         session['token_info']['access_token']
#     )
#
#     return render_template('music.html', track_info=track_info)


def get_recent_track(access_token):
    response = requests.get(
        SPOTIFY_GET_RECENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    json_resp = response.json()
    json_resp = json_resp['items'][-1]

    album_name = json_resp['track']['album']['name']
    album_artwork = json_resp['track']['album']['images'][0]['url']
    track_id = json_resp['track']['id']
    track_name = json_resp['track']['name']
    artist_names_list = []
    artist_names = json_resp['track']['artists']
    for artist in artist_names:
        artist_names_list.append(artist['name'])
    if len(artist_names_list) == 1:
        artist_names_list = artist_names_list[0]
    elif len(artist_names_list) == 2:
        artist_names_list[-1] = " and " + artist_names_list[-1]
        artist_names_list = "".join(artist_names_list)
    elif len(artist_names_list) > 2:
        artist_names_list[-1] = "and " + artist_names_list[-1]
        artist_names_list = ", ".join(artist_names_list)
    link = json_resp['track']['external_urls']['spotify']

    recent_track_info = {
        "id": track_id,
        "track_name": track_name,
        "artists": artist_names_list,
        "link": link,
        "album_name": album_name,
        "album_artwork": album_artwork
    }

    return recent_track_info


# Checks to see if token is valid and gets a new token if not
def get_token(scope):
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if is_token_expired:
        sp_oauth = create_spotify_oauth(scope)
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid


def create_spotify_oauth(scope):
    return SpotifyOAuth(
        client_id="xxxxx",
        client_secret=app.secret_key,
        redirect_uri=url_for('music', _external=True),
        scope=scope)


if __name__ == "__main__":
    app.run(port=PORT)
