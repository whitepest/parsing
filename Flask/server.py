from flask import Flask, request

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
        return f"Authorization code received: {authorization_code}"
    else:
        return "Authorization code not found!", 400

if __name__ == "__main__":
    app.run(port=5001)
