from flask import g


def render_template_wrapper(func):
    """
    Simple wrapper for flask render_template
    Makes sure to pass in user to the kwargs just so we don't have to do it
    manually each time
    """
    def wrapper(*args, **kwargs):
        if 'user' not in kwargs:
            user = g.get('user', None)
            kwargs['user'] = user
        return func(*args, **kwargs)
    return wrapper
