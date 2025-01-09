import json
import subprocess
import webbrowser
import http.server
import socketserver
import threading
import urllib.parse
import os

def start_server(redirect_uri):
    """Start a temporary local server to capture the authorization code."""
    class RequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            # Parse the query parameters from the redirected URL
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            print(f"Received query params: {params}")  # Debug info

            if "code" in params:
                auth_code = params["code"][0]
                print(f"Authorization code received: {auth_code}")

                # Load or create auth_code.json safely
                data = {}
                if os.path.exists("auth_code.json"):
                    try:
                        with open("auth_code.json", "r") as file:
                            data = json.load(file)
                    except (json.JSONDecodeError, FileNotFoundError):
                        print("auth_code.json is empty or invalid. Overwriting.")

                # Save the new authorization code
                data["authorization_code"] = auth_code
                with open("auth_code.json", "w") as file:
                    json.dump(data, file, indent=4)
                print("Authorization code saved to auth_code.json.")

                # Respond to the browser
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Authorization code received and saved. You can close this tab.")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Authorization code not found.")

    # Parse the port from the redirect URI
    port = int(redirect_uri.split(":")[-1].split("/")[0])

    # Start the HTTP server
    with socketserver.TCPServer(("", port), RequestHandler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

# Step 1: Generate the authorization URL
url = subprocess.check_output(["python", "generate_url.py"]).decode().strip()

# Step 2: Open the authorization URL in the browser
print(f"Opening browser to: {url}")
webbrowser.open(url)

# Step 3: Start the server to handle the callback
with open("config.json", "r") as config_file:
    config = json.load(config_file)

redirect_uri = config["redirect_uri"]

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server, args=(redirect_uri,))
server_thread.daemon = True
server_thread.start()

# Wait for the user to complete the authorization
server_thread.join()
