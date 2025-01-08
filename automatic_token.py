import requests
import time
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve client credentials and redirect URI
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"

TOKEN_FILE = "tokens.json"

def load_tokens():
    """Load tokens from a file."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            return json.load(file)
    return {}

def save_tokens(tokens):
    """Save tokens to a file."""
    with open(TOKEN_FILE, "w") as file:
        json.dump(tokens, file)

def get_new_access_token(refresh_token):
    """Refresh the access token using the refresh token."""
    url = "https://api.getjobber.com/api/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        tokens = response.json()
        save_tokens(tokens)
        print("Access token refreshed successfully.")
        return tokens.get("access_token")
    else:
        print("Failed to refresh token:", response.text)
        return None

def get_access_token():
    """Retrieve a valid access token, refreshing it if needed."""
    tokens = load_tokens()
    if not tokens:
        print("No tokens found. Please authenticate manually.")
        return None

    access_token = tokens.get("access_token")
    expires_at = tokens.get("expires_at", 0)

    # Check if the token has expired
    if time.time() >= expires_at:
        print("Access token expired. Refreshing...")
        return get_new_access_token(tokens.get("refresh_token"))
    return access_token

def authenticate():
    """Authenticate the user and obtain initial tokens."""
    print("Please generate the authorization code and paste it here.")
    authorization_code = input("Authorization Code: ")

    url = "https://api.getjobber.com/api/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        tokens = response.json()
        # Calculate expiration time (e.g., current time + token TTL)
        tokens["expires_at"] = time.time() + tokens.get("expires_in", 3600)
        save_tokens(tokens)
        print("Authenticated successfully. Tokens saved.")
    else:
        print("Authentication failed:", response.text)

# Example API Call
def make_api_request(endpoint):
    """Make an authenticated API request."""
    access_token = get_access_token()
    if not access_token:
        print("No valid access token. Exiting.")
        return

    url = f"https://api.getjobber.com/api/{endpoint}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("API Response:", response.json())
    else:
        print("API Request failed:", response.status_code, response.text)

# Main Workflow
if __name__ == "__main__":
    tokens = load_tokens()
    if not tokens:
        authenticate()
    else:
        print("Existing tokens found. Using them.")

    # Example: Make an API call
    make_api_request("jobs")  # Replace "jobs" with the desired endpoint
