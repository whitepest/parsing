import requests

# Define the API endpoint and the access token
url = "https://api.getjobber.com/api/clients"
access_token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOjE2MzU3MDUsImlzcyI6Imh0dHBzOi8vYXBpLmdldGpvYmJlci5jb20iLCJjbGllbnRfaWQiOiI2NzY2OWRiOC1lZTQ4LTRiY2UtYmNhZC1mZWNhMGMwNGY4OTUiLCJzY29wZSI6InJlYWRfY2xpZW50cyByZWFkX3JlcXVlc3RzIHJlYWRfcXVvdGVzIHJlYWRfam9icyByZWFkX3NjaGVkdWxlZF9pdGVtcyByZWFkX3VzZXJzIHJlYWRfY3VzdG9tX2ZpZWxkX2NvbmZpZ3VyYXRpb25zIiwiYXBwX2lkIjoiNjc2NjlkYjgtZWU0OC00YmNlLWJjYWQtZmVjYTBjMDRmODk1IiwidXNlcl9pZCI6MTYzNTcwNSwiYWNjb3VudF9pZCI6Mjg2NTE0LCJleHAiOjE3MzEwNDE2MTd9.7ur7IVdciMJzvepf2O2L8pZSx58m6N4Lksg_uAnfNl0"

# Set up the headers with the Authorization token
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Make the GET request to the API endpoint
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response (if the response is in JSON format)
    data = response.json()
    print("Response data:", data)
else:
    print("Failed to retrieve data:", response.status_code, response.text)
