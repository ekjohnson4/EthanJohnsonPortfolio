import json


with open("settings.json") as f:
    _settings = json.load(f)

PORT = _settings.get("PORT", "5000")