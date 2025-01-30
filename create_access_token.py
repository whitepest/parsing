import requests
import json

# Load configuration and authorization code
with open("config.json", "r") as config_file:
    config = json.load(config_file)

with open("auth_code.json", "r") as auth_code_file:
    auth_data = json.load(auth_code_file)

authorization_code = auth_data["authorization_code"]

# Prepare token request data
url = "https://api.getjobber.com/api/oauth/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "client_id": config["client_id"],
    "client_secret": config["client_secret"],
    "grant_type": "authorization_code",
    "code": authorization_code,
    "redirect_uri": config["redirect_uri"]
}

# Send the POST request to exchange the code for tokens
response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    tokens = response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    # Save the access token separately (optional)
    with open("tokens.json", "w") as tokens_file:
        json.dump({"access_token": access_token}, tokens_file, indent=4)

    # Update config.json to store refresh_token
    config["refresh_token"] = refresh_token
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

    print("✅ Access token saved to tokens.json")
    print("✅ Refresh token saved to config.json")
    print(f"🔑 Access Token: {access_token}")
    print(f"🔄 Refresh Token: {refresh_token}")

else:
    print(f"❌ Failed to create access token: {response.status_code}")
    print(response.json())
