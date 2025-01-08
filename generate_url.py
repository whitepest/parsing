import urllib.parse
from dotenv import load_dotenv
import os
import secrets

load_dotenv()


def generate_auth_url(client_id, redirect_uri, scope, state):
    base_url = "https://api.getjobber.com/api/oauth/authorize"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "state": state,
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"

# Replace with your values
client_id = os.getenv("CLIENT_ID")
redirect_uri = "http://localhost:5000/callback"  # Must match what you registered
scope = "jobs.read clients.read"   # Adjust scope based on your needs
state = secrets.token_urlsafe(8) # For CSRF protection (any random string)

# Generate and print the authorization URL
auth_url = generate_auth_url(client_id, redirect_uri, scope, state)
print("Go to the following URL to authorize:", auth_url)
