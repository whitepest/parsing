import requests
from dotenv import load_dotenv
import os
load_dotenv()

def get_access_token(client_id, client_secret, authorization_code, redirect_uri):
    url = "https://api.getjobber.com/api/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        tokens = response.json()
        print("Access Token:", tokens.get("access_token"))
        print("Refresh Token:", tokens.get("refresh_token"))
        return tokens.get("access_token"), tokens.get("refresh_token")
    else:
        print("Failed to get tokens:", response.status_code, response.text)
        return None, None

# Replace with your values
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
authorization_code = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOjE2MzU3MDUsImlzcyI6Imh0dHBzOi8vYXBpLmdldGpvYmJlci5jb20iLCJjbGllbnRfaWQiOiI2NzY2OWRiOC1lZTQ4LTRiY2UtYmNhZC1mZWNhMGMwNGY4OTUiLCJzY29wZSI6InJlYWRfY2xpZW50cyByZWFkX3JlcXVlc3RzIHJlYWRfcXVvdGVzIHJlYWRfam9icyByZWFkX3NjaGVkdWxlZF9pdGVtcyByZWFkX3VzZXJzIHJlYWRfY3VzdG9tX2ZpZWxkX2NvbmZpZ3VyYXRpb25zIiwiYXBwX2lkIjoiNjc2NjlkYjgtZWU0OC00YmNlLWJjYWQtZmVjYTBjMDRmODk1IiwidXNlcl9pZCI6MTYzNTcwNSwiYWNjb3VudF9pZCI6Mjg2NTE0LCJleHAiOjE3MzYzNjg1ODd9.1hzslr8C2ccF-vYbYo8_z2wz1jQ2i2DY8vfysTEndKE"  # Replace with the code you received
redirect_uri = "http://localhost:5000/callback"  # Replace with your redirect URI

# Get tokens
access_token, refresh_token = get_access_token(client_id, client_secret, authorization_code, redirect_uri)
