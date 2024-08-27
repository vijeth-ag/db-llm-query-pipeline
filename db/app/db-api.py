from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from vec_db import store_embeddings, get_similar_docs, init_db
from embedding import encode
import json

init_db()

def ok(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/store':
            content_length = int(self.headers['Content-Length'])
            
            # Read the body of the request
            post_data = self.rfile.read(content_length)
            
            # Convert the received data to a dictionary (assuming JSON)
            post_payload = json.loads(post_data)
            try:
                vec =  encode(post_payload["data"])
                print("vec",len(vec))
                store_embeddings(vec, post_payload["data"])
                ok(self)             
            except:
                print("error encoding/storing", post_payload["data"])
                ok(self)


    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/health':
            # Handle the health check
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
            return        

        if parsed_path.path == '/get':
            query_params = parse_qs(parsed_path.query)
            similar_docs = get_similar_docs(query_params['query'][0])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(str(similar_docs), 'utf-8'))

        else:
            # Handle other paths or return a 404 Not Found response
            self.send_response(404)
            self.end_headers()


# Set up and start the server
server_address = ('', 5123)  # Serve on all available interfaces at port 9000
httpd = HTTPServer(server_address, MyHandler)
print("DB Server running on port 5123...")
httpd.serve_forever()