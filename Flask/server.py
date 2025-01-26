from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "OAuth 2.0 Flask Local Server is Running!"

@app.route("/callback")
def callback():
    # Extract the authorization code from the query parameters
    authorization_code = request.args.get("code")
    state = request.args.get("state")
    
    if authorization_code:
        # Write the authorization code into auth_code.json
        auth_data = {"authorization_code": authorization_code, "state": state}
        with open("auth_code.json", "w") as json_file:
            json.dump(auth_data, json_file, indent=4)
        
        return jsonify({"message": "Authorization code received and saved.", "data": auth_data})
    else:
        return "Authorization code not found!", 400

if __name__ == "__main__":
    app.run(port=5001)
