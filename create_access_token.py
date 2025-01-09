import requests
import json

# Step 1: Load configuration and authorization code
with open("config.json", "r") as config_file:
    config = json.load(config_file)

with open("auth_code.json", "r") as auth_code_file:
    auth_data = json.load(auth_code_file)

authorization_code = auth_data["authorization_code"]

# Step 2: Prepare token request data
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

# Step 3: Send the POST request to exchange the code for tokens
response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    tokens = response.json()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    # Step 4: Save the tokens to a JSON file
    with open("tokens.json", "w") as tokens_file:
        json.dump(tokens, tokens_file, indent=4)

    print("Access token and refresh token saved to tokens.json.")
    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {refresh_token}")

else:
    print(f"Failed to create access token: {response.status_code}")
    print(response.json())
