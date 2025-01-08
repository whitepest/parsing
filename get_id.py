from dotenv import load_dotenv
import os

# Explicitly load .env file
load_dotenv()

client_id = os.getenv("CLIENT_ID")

# Debugging: Print the client_id to check if it's loaded
print("CLIENT_ID from .env:", client_id)
