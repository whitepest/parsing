import requests
import json

# Load credentials from config.json
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

# Save updated tokens to config.json
def save_config(config):
    with open("config.json", "w") as file:
        json.dump(config, file, indent=2)

# Function to refresh the access token
def refresh_access_token():
    config = load_config()
    
    url = "https://api.getjobber.com/api/oauth/token"  # Jobber token refresh endpoint
    data = {
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "grant_type": "refresh_token",
        "refresh_token": config["refresh_token"]
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        new_tokens = response.json()
        
        # Update tokens in config.json
        config["access_token"] = new_tokens["access_token"]
        config["refresh_token"] = new_tokens["refresh_token"]  # Update refresh token
        save_config(config)
        
        print("Access token refreshed successfully.")
        print(f"New Access Token: {config['access_token']}")
    else:
        print(f"Failed to refresh access token: {response.status_code} {response.text}")
        print("Reauthorization may be required.")

# Run the refresh token function
if __name__ == "__main__":
    refresh_access_token()
