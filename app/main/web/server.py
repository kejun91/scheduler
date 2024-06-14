from http.server import HTTPServer
import os
from socketserver import ThreadingMixIn
import webbrowser
from app.main.web.handler import RequestHandler

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def start_server(port = 8888):
    try:
        server_address = ('', port)
        httpd = ThreadedHTTPServer(server_address, RequestHandler)
        print('Server running on port', port)
        webbrowser.open('http://localhost:' + str(port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Exiting...")
        os._exit(130)