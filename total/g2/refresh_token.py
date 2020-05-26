
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_refresh_token(
    client_id, client_secret, refresh_token,
):
    params = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }

    authorization_url = "https://www.g2smart.com/g2smart/api/oauth2/token"

    r = requests.post(authorization_url, data=params)

    if r.ok:
        return r.json()
    else:
        return None

print(get_refresh_token(os.getenv('client_id'),os.getenv('client_secret'),os.getenv('refresh_token')))

