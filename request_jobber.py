import requests
from dotenv import load_dotenv
import os
load_dotenv()

access_token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOjE2MzU3MDUsImlzcyI6Imh0dHBzOi8vYXBpLmdldGpvYmJlci5jb20iLCJjbGllbnRfaWQiOiI2NzY2OWRiOC1lZTQ4LTRiY2UtYmNhZC1mZWNhMGMwNGY4OTUiLCJzY29wZSI6InJlYWRfY2xpZW50cyByZWFkX3JlcXVlc3RzIHJlYWRfcXVvdGVzIHJlYWRfam9icyByZWFkX3NjaGVkdWxlZF9pdGVtcyByZWFkX3VzZXJzIHJlYWRfY3VzdG9tX2ZpZWxkX2NvbmZpZ3VyYXRpb25zIiwiYXBwX2lkIjoiNjc2NjlkYjgtZWU0OC00YmNlLWJjYWQtZmVjYTBjMDRmODk1IiwidXNlcl9pZCI6MTYzNTcwNSwiYWNjb3VudF9pZCI6Mjg2NTE0LCJleHAiOjE3MzYzNjg1ODd9.1hzslr8C2ccF-vYbYo8_z2wz1jQ2i2DY8vfysTEndKE"
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