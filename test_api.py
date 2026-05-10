import requests
import os
#
# CLIENT_ID=os.getenv('OPENSKY_CLIENT_ID')
# CLIENT_SECRET=os.getenv('OPENSKY_CLIENT_SECRET')

CLIENT_ID = "moemoev-api-client"
CLIENT_SECRET = "33su5NrzlgdK7HjuFWHHGQ4MYvocBdjU"
print(CLIENT_ID)
print(CLIENT_SECRET)

def get_token():
    token = requests.post("https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token",
                          headers={"Content-Type": "application/x-www-form-urlencoded"},
                          data={"grant_type": "client_credentials",
                                "client_id": CLIENT_ID,
                                "client_secret": CLIENT_SECRET})

    print(token.status_code)
    print(token.json())

    return token.json()['access_token']

token = get_token()

print(f"This is the token so far : {token}")