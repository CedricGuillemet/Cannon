#!/usr/bin/env python3

import http.server
import socketserver
import urllib.parse
import json
import base64
import os

# Define the port on which you want to run the server
PORT = 8000
    
class CORSHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        """Set the necessary headers for CORS and content type."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # Allow all origins for CORS. Adjust as needed for security.
        self.send_header('Access-Control-Allow-Origin', '*')
        # Allow specific headers
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # Allow specific methods
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

    def do_OPTIONS(self):
        """Respond to preflight CORS requests."""
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        try:
            # Parse the URL to get query parameters
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)

            # Helper function to extract single values and remove quotes
            def get_param(param_name):
                value = query_params.get(param_name, [None])[0]
                if value:
                    # Remove surrounding quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                return value

            # Extract 'prompt' and 'query' parameters
            prompt = get_param('prompt')
            query = get_param('query')

            # Initialize response data
            response = {
                'received_parameters': {
                    'prompt': prompt,
                    'query': query
                },
                'message': 'Parameters received successfully.'
            }
            print(response)

            # Perform computation based on 'query' parameter

            mime_type = 'application/octet-stream'  # Default MIME type

        
            with open("ninja.glb", 'rb') as f:
                file_content = f.read()

            # Set headers with the appropriate MIME type
            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.end_headers()

            # Write the file content to the response
            self.wfile.write(file_content)
            return

        except Exception as e:
            # Error reading the file
            self._set_headers('application/json')
            response['error'] = f"Error reading file '{file_name}': {str(e)}"
            self.wfile.write(json.dumps(response, indent=4).encode('utf-8'))

    def parse_query_parameters(self):
        """Parse query parameters from the URL."""
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        # Convert query parameters to a regular dictionary
        # parse_qs returns values as lists, so we simplify it
        params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
        return params
    
    def do_POST(self):
        """Handle POST requests: parse form data and respond with it in JSON."""
        try:
            #params = self.parse_query_parameters()
            #prompt = params.get('prompt')
            #print(prompt)

            #print(self.headers)
            content_length = int(self.headers.get('Content-Length', 0))
            #print(content_length)

            post_data = self.rfile.read(content_length).decode('utf-8')
            base64_str = post_data.split('base64,')[-1]
            image_data = base64.b64decode(base64_str)

            with open("useImage.png", 'wb') as image_file:
                image_file.write(image_data)
            
            # do something with the image and return a new image

            mime_type = 'image/png'  # Default MIME type
        
            with open("img2imgResult.png", 'rb') as f:
                file_content = f.read()

            # Set headers with the appropriate MIME type
            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.end_headers()

            # Write the file content to the response
            self.wfile.write(file_content)

        except Exception as e:
            self._set_headers('application/json')
            response = {}
            response['error'] = f"Error ': {str(e)}"
            self.wfile.write(json.dumps(response, indent=4).encode('utf-8'))

def run(server_class=http.server.HTTPServer, handler_class=CORSHTTPRequestHandler):
    """Run the HTTP server."""
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {PORT}...")
    print(f"Open http://localhost:{PORT}/ in your browser or send HTTP requests.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server.")
        httpd.server_close()

if __name__ == '__main__':
    run()
