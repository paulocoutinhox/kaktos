import os
import socketserver
import sys
from http.server import SimpleHTTPRequestHandler

from pygemstones.io import file as f
from pygemstones.util import log as l


# -----------------------------------------------------------------------------
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        directory = os.path.join(os.getcwd(), "build")
        self.directory = os.fspath(directory)
        super().__init__(directory=directory, *args, **kwargs)

    extensions_map = {
        "": "application/octet-stream",
        ".css": "text/css",
        ".html": "text/html",
        ".jpg": "image/jpg",
        ".js": "application/x-javascript",
        ".json": "application/json",
        ".manifest": "text/cache-manifest",
        ".png": "image/png",
        ".wasm": "application/wasm",
        ".xml": "application/xml",
    }

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        SimpleHTTPRequestHandler.end_headers(self)


# -----------------------------------------------------------------------------
def run(params={}):
    directory = os.path.join(os.getcwd(), "build")

    if not f.dir_exists(directory):
        l.e("Build directory not exists")

    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5555
    with socketserver.TCPServer(("localhost", port), Handler) as httpd:
        l.i(f"Serving on port: {port}")
        httpd.serve_forever()
