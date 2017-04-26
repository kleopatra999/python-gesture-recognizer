from http.server import *
import uuid

class GesturesService( BaseHTTPRequestHandler ):
    def do_POST(self):
        self.send_response( 200 )
        self.send_header( "location", uuid.uuid4() )
        self.end_headers()

def run(server_class=HTTPServer, handler_class = GesturesService ):
    server_address = ('', 49217) 
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
