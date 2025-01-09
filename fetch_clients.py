import requests
import json

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


access_token = load_config()
if not access_token:
    raise ValueError("Access token is missing. Ensure tokens.json is properly configured.")

# Define the endpoint and headers
url = "https://api.getjobber.com/api/graphql"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "X-JOBBER-GRAPHQL-VERSION": "2024-12-05"
}

# Define the GraphQL query
query = """
query SampleQuery {
  clients {
    totalCount
  }
}
"""

# Send the POST request
response = requests.post(url, json={"query": query}, headers=headers)

# Check and print the response
if response.status_code == 200:
    print("Response JSON:", response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")
