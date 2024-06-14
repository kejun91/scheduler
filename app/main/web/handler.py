from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
import importlib
import json
import mimetypes
import pkgutil
from typing import Optional
from urllib.parse import parse_qs, urlparse
from app.utils.common import CustomEncoder
from app.main.web.decorator import api_routes, webpage_routes

package = importlib.import_module(__package__ + '.routes')
for _, module_name, _ in pkgutil.walk_packages(package.__path__,prefix=package.__name__ + '.'):
    module = importlib.import_module(module_name)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def do_PUT(self):
        self.handle_request('PUT')

    def do_DELETE(self):
        self.handle_request('DELETE')

    def handle_request(self, method):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path.startswith('/api/'):
            response_body = None
            response_code = 200
            matched_path = False
            handler = None
            for route in api_routes:
                if route.get('method') == method and path.startswith(route.get('path')):
                    matched_path = True
                    handler = route.get('func')
                    break
            
            if matched_path:
                if handler is not None:
                    content_length = int(self.headers['Content-Length'] or '0')
                    response_body = handler(Request(
                        path = path,
                        query_params = parse_qs(parsed_url.query),
                        body = json.loads(self.rfile.read(content_length).decode()) if content_length > 0 else {}
                    ))
                else:
                    response_code = 405
            else:
                response_code = 404

            self.send_response(response_code)
            self.send_header('Content-type', 'application/json')

            self.end_headers()
            self.wfile.write(json.dumps(f"{str(response_code)} {HTTPStatus(response_code).phrase}" if response_body is None else response_body, cls=CustomEncoder).encode())
        else:
            file_path = None
            content_type = 'text/plain'
            response_code = 200
            handler = None
            for route in webpage_routes:
                if path.startswith(route.get('path')):
                    handler = route.get('func')
                    break

            if handler is not None:
                if method == 'GET':
                    file_path = handler(path)
                    guessed_type, _ = mimetypes.guess_type(file_path)
                    content_type = guessed_type or content_type
                else:
                    response_code = 405
            else:
                response_code = 404

            self.send_response(response_code)
            self.send_header('Content-type', content_type)

            if content_type.startswith('image') or content_type.endswith('css') or content_type.endswith('javascript'):
                self.send_header('Cache-Control', 'max-age=86400')
            self.end_headers()

            if file_path is not None:
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.wfile.write(f'{str(response_code)} {HTTPStatus(response_code).phrase}'.encode())
@dataclass
class Request:
    path: str
    query_params: Optional[dict] = None
    body: Optional[any] = None