import requests
from dotenv import load_dotenv
import os


load_dotenv("config.env")

def get_new_access_token(client_id, client_secret, refresh_token):
    url = "https://api.getjobber.com/api/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        print("New access token:", access_token)
        print("New refresh token:", refresh_token)
        return access_token, refresh_token
    else:
        print("Failed to refresh token:", response.json())
        return None, None

# Replace these with your actual credentials and refresh token
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
refresh_token = "YOUR_REFRESH_TOKEN"

# Get a new access token
new_access_token, new_refresh_token = get_new_access_token(client_id, client_secret, refresh_token)

# You can now use new_access_token for API requests, and new_refresh_token for future refreshes
