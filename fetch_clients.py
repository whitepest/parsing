import requests
import json

# Load configuration from auth_code.json or access_token.json
def load_config():
    try:
        with open("tokens.json", "r") as file:
            data = json.load(file)
            return data["access_token"]
    except FileNotFoundError:
        print("Error: tokens.json not found.")
        return None
    except KeyError:
        print("Error: Access token not found in access_token.json.")
        return None

# Fetch the clients
def fetch_clients(access_token):
    url = "https://api.getjobber.com/api/clients"  # Replace with the correct endpoint for fetching clients
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return len(data.get("clients", []))  # Adjust the key based on Jobber's API response structure
    else:
        print(f"Failed to fetch clients: {response.status_code} {response.text}")
        return None

# Main script
def main():
    access_token = load_config()
    if not access_token:
        print("No valid access token found.")
        return

    client_count = fetch_clients(access_token)
    if client_count is not None:
        print(f"Number of clients: {client_count}")
    else:
        print("Failed to retrieve the number of clients.")

if __name__ == "__main__":
    main()
