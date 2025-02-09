import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import ctypes
import signal
import sys

port = int(input("Enter port: "))
choiceJS = input("JS file [y/n]: ")
choiceCSS = input("CSS file [y/n]: ")
HTMLfile = input("HTML file: ")

CSSfile = ""
JSfile = ""

if choiceCSS.lower() == "y":
    CSSfile = input("Enter the path to the CSS file: ")

if choiceJS.lower() == "y":
    JSfile = input("Enter the path to the JS file: ")

lib = ctypes.CDLL('./libparser.so')

lib.parse_html.argtypes = [ctypes.c_char_p]
lib.parse_js.argtypes = [ctypes.c_char_p]
lib.parse_css.argtypes = [ctypes.c_char_p]

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            with open(HTMLfile, "r") as f:
                content = f.read()
            lib.parse_html(content.encode('utf-8'))

        if self.path == '/styles.css' and choiceCSS.lower() == "y" and CSSfile:
            with open(CSSfile, "r") as f:
                content = f.read()
            lib.parse_css(content.encode('utf-8'))

        if self.path == '/script.js' and choiceJS.lower() == "y" and JSfile:
            with open(JSfile, "r") as f:
                content = f.read()
            lib.parse_js(content.encode('utf-8'))

        return super().do_GET()

def shutdown(signum, frame):
    print("Server shutting down...")
    httpd.server_close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

httpd = TCPServer(("", port), Handler)

print(f"Server running on http://localhost:{port}")
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    shutdown(None, None)

