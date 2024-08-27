from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from rag import get_similar_docs, get_results

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/health':
            # Handle the health check
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Query server health OK')
            return

        # Check if the requested path is /query
        if parsed_path.path == '/query':
            # Process the request as needed
            query_params = parse_qs(parsed_path.query)
            print("query_params",query_params)
            question = query_params['question'][0]
            similar_docs = get_similar_docs(question)

            print("similar_docs len",len(similar_docs))

            reults = get_results(question, similar_docs)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(reults.encode())
        else:
            # Handle other paths or return a 404 Not Found response
            self.send_response(404)
            self.end_headers()


# Set up and start the server
server_address = ('', 8123)  # Serve on all available interfaces at port 8123
httpd = HTTPServer(server_address, MyHandler)
print("Server running on port 8123...")
httpd.serve_forever()
