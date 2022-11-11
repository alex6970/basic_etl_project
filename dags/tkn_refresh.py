import base64
import requests


def refresh_spotify_token(client_id, client_secret, refresh_token):

    auth_str = '{}:{}'.format(client_id, client_secret)
    b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()

    url = "https://accounts.spotify.com/api/token"

    response = requests.post(url, 
                                data={
                                    "grant_type": "refresh_token",
                                    "refresh_token": refresh_token},

                                headers={
                                    "Authorization": "Basic " + b64_auth_str}
                                    )
    
    response_data = response.json()

    return response_data["access_token"]

