import urllib.parse
import json
import secrets

def generate_auth_url():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    base_url = "https://api.getjobber.com/api/oauth/authorize"
    params = {
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_uri"],
        "response_type": "code",
        "scope": config["scope"],
        "state": secrets.token_urlsafe(8),  # For CSRF protection
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"

if __name__ == "__main__":
    print(generate_auth_url())

"""# Replace with your values
client_id = config["client_id"]
redirect_uri = "http://localhost:5000/callback"  # Must match what you registered
scope = "jobs.read clients.read"   # Adjust scope based on your needs
state = secrets.token_urlsafe(8) # For CSRF protection (any random string)"""


