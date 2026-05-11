import os
import requests

CLIENT_ID=os.getenv('OPENSKY_CLIENT_ID')
CLIENT_SECRET=os.getenv('OPENSKY_CLIENT_SECRET')

def get_token():
    token = requests.post("https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token",
                          headers={"Content-Type": "application/x-www-form-urlencoded"},
                          data={"grant_type": "client_credentials",
                                "client_id": CLIENT_ID,
                                "client_secret": CLIENT_SECRET})


    return token.json()['access_token']