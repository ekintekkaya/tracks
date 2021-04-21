import base64
from urllib.parse import urlencode

import requests


class SpotifyAPI(object):
    client_id = ""
    client_secret = ""
    access_token = None

    def __init__(self):
        token_url = "https://accounts.spotify.com/api/token"
        client_cred = f"{self.client_id}:{self.client_secret}"
        cred_64 = base64.b64encode(client_cred.encode())
        token_data = {
            "grant_type": "client_credentials"
        }
        token_header = {
            "Authorization": f"Basic {cred_64.decode()}"
        }
        r = requests.post(token_url, data=token_data, headers=token_header)
        response = r.json()
        self.access_token = response['access_token']

    def find_artist_id(self, genre, artist):
        header = {
            "Authorization": f"Bearer {self.access_token}"
        }
        url_base = 'https://api.spotify.com/v1/search'
        params = urlencode({"q": artist, "type": "artist", "limit": 1})
        url = f"{url_base}?{params}"
        response = requests.get(url, headers=header).json()
        return response['artists']['items'][0]['id']

    def get_top_ten(self, artist_id):
        header = {
            "Authorization": f"Bearer {self.access_token}"
        }
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
        response = requests.get(url, headers=header).json()
        list_len = min(10, len(response['tracks']))
        top_ten_list = []
        for i in range(list_len):
            top_ten_list.append({'artist': response['tracks'][i]['artists'][0]['name'], 'track': response['tracks'][i]['name'],
             'album_image_url': response['tracks'][i]['album']['images'][0]['url'],
             'preview_url': response['tracks'][i]['external_urls']['spotify']})
        return top_ten_list

