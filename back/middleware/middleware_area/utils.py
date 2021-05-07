import requests

def get_user_from_headers(headers):
    auth = headers.get('Authorization', None)
    if auth is None:
        return None
    token = auth.split("Bearer ")[1]
    resp = requests.get("http://parse-server:1337/parse/users/me", headers={
        "X-Parse-Application-Id": "",
        "X-Parse-REST-API-Key": "",
        "X-Parse-Session-Token": token
    })

    if resp.status_code != 200:
        return None
    return resp.json()