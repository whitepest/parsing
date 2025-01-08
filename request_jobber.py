import requests
access_token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOjI3MDE1MDQsImlzcyI6Imh0dHBzOi8vYXBpLmdldGpvYmJlci5jb20iLCJjbGllbnRfaWQiOiI2NzY2OWRiOC1lZTQ4LTRiY2UtYmNhZC1mZWNhMGMwNGY4OTUiLCJzY29wZSI6InJlYWRfY2xpZW50cyB3cml0ZV9jbGllbnRzIHJlYWRfcmVxdWVzdHMgd3JpdGVfcmVxdWVzdHMgcmVhZF9xdW90ZXMgd3JpdGVfcXVvdGVzIHJlYWRfam9icyB3cml0ZV9qb2JzIHJlYWRfc2NoZWR1bGVkX2l0ZW1zIHdyaXRlX3NjaGVkdWxlZF9pdGVtcyByZWFkX3VzZXJzIHdyaXRlX3VzZXJzIHJlYWRfY3VzdG9tX2ZpZWxkX2NvbmZpZ3VyYXRpb25zIiwiYXBwX2lkIjoiNjc2NjlkYjgtZWU0OC00YmNlLWJjYWQtZmVjYTBjMDRmODk1IiwidXNlcl9pZCI6MjcwMTUwNCwiYWNjb3VudF9pZCI6MTUxMTQwNiwiZXhwIjoxNzMwNjU0MDI1fQ.LnqSlmDhzM0CSiq3hu-uYFVtvNuWeSTA6rlWKtdTK9E"
client_id = "67669db8-ee48-4bce-bcad-feca0c04f895"
client_secret = "bd19777156515639d71a235cbdb771f1e8803ab698b1a8840e76332ed0ef7b82"
def get_access_token(client_id, client_secret):
    url = "https://api.getjobber.com/api/token"
    data = {
        #"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOjI3MDE1MDQsImlzcyI6Imh0dHBzOi8vYXBpLmdldGpvYmJlci5jb20iLCJjbGllbnRfaWQiOiI2NzY2OWRiOC1lZTQ4LTRiY2UtYmNhZC1mZWNhMGMwNGY4OTUiLCJzY29wZSI6InJlYWRfY2xpZW50cyB3cml0ZV9jbGllbnRzIHJlYWRfcmVxdWVzdHMgd3JpdGVfcmVxdWVzdHMgcmVhZF9xdW90ZXMgd3JpdGVfcXVvdGVzIHJlYWRfam9icyB3cml0ZV9qb2JzIHJlYWRfc2NoZWR1bGVkX2l0ZW1zIHdyaXRlX3NjaGVkdWxlZF9pdGVtcyByZWFkX3VzZXJzIHdyaXRlX3VzZXJzIHJlYWRfY3VzdG9tX2ZpZWxkX2NvbmZpZ3VyYXRpb25zIiwiYXBwX2lkIjoiNjc2NjlkYjgtZWU0OC00YmNlLWJjYWQtZmVjYTBjMDRmODk1IiwidXNlcl9pZCI6MjcwMTUwNCwiYWNjb3VudF9pZCI6MTUxMTQwNiwiZXhwIjoxNzMwNjUwMjQ1fQ.D1JBvFRUfmyP1pUXrkoLBnJ8nZrr5acuGVXZmTUxxG4",
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, data=data)
    print(response.text)


access_token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOjI3MDE1MDQsImlzcyI6Imh0dHBzOi8vYXBpLmdldGpvYmJlci5jb20iLCJjbGllbnRfaWQiOiI2NzY2OWRiOC1lZTQ4LTRiY2UtYmNhZC1mZWNhMGMwNGY4OTUiLCJzY29wZSI6InJlYWRfY2xpZW50cyB3cml0ZV9jbGllbnRzIHJlYWRfcmVxdWVzdHMgd3JpdGVfcmVxdWVzdHMgcmVhZF9xdW90ZXMgd3JpdGVfcXVvdGVzIHJlYWRfam9icyB3cml0ZV9qb2JzIHJlYWRfc2NoZWR1bGVkX2l0ZW1zIHdyaXRlX3NjaGVkdWxlZF9pdGVtcyByZWFkX3VzZXJzIHdyaXRlX3VzZXJzIHJlYWRfY3VzdG9tX2ZpZWxkX2NvbmZpZ3VyYXRpb25zIiwiYXBwX2lkIjoiNjc2NjlkYjgtZWU0OC00YmNlLWJjYWQtZmVjYTBjMDRmODk1IiwidXNlcl9pZCI6MjcwMTUwNCwiYWNjb3VudF9pZCI6MTUxMTQwNiwiZXhwIjoxNzMwNjU0MDI1fQ.LnqSlmDhzM0CSiq3hu-uYFVtvNuWeSTA6rlWKtdTK9E"
def make_request(endpoint, method="POST", data=None):
    headers = {"Authorization": f"Bearer {access_token}",
                "X-JOBBER-GRAPHQL-VERSION": "2024-09-23"}
    url = f"https://api.getjobber.com/api/{endpoint}"
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers)
    
    print(response)
    #response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()

jose = make_request("graphql", method="POST",)