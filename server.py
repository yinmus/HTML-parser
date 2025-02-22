import os
import sys
import ctypes
import signal
import socket
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

def f(ext): return [x for x in os.listdir('.') if x.endswith(ext)]

def ask(ext, def_v=None):
    if def_v == "None": return None
    if def_v: return def_v
    files = f(ext)
    for i, x in enumerate(files, 1): print(f"{i}. {x}")
    ch = input("Num/Path: ").strip()
    return files[int(ch)-1] if ch.isdigit() and 1 <= int(ch) <= len(files) else ch or None

def p_in_use(p): 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: return s.connect_ex(("localhost", p)) == 0

def kill(p):
    if sys.platform.startswith("linux"): os.system(f"fuser -k {p}/tcp")
    elif sys.platform.startswith("win"): os.system(f"netstat -ano | findstr :{p} > temp.txt && for /f \"tokens=5\" %i in (temp.txt) do taskkill /F /PID %i && del temp.txt")
    else: print("Kill manually.")

if len(sys.argv) > 1: port = int(sys.argv[1]) if sys.argv[1].isdigit() else None
else: port = int(input("Port: "))

if port and p_in_use(port):
    if input(f"Port {port} in use. Kill? [y/n]: ").strip().lower() == "y": kill(port)
    else: sys.exit(1)

HTML = ask(".html", sys.argv[2] if len(sys.argv) > 2 else None)
JS = ask(".js", sys.argv[3] if len(sys.argv) > 3 else None)
CSS = ask(".css", sys.argv[4] if len(sys.argv) > 4 else None)

lib = ctypes.CDLL('./libparser.so')
lib.parse_html.argtypes = [ctypes.c_char_p]
lib.parse_js.argtypes = [ctypes.c_char_p]
lib.parse_css.argtypes = [ctypes.c_char_p]

class H(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' and HTML:
            with open(HTML, "r") as f: lib.parse_html(f.read().encode('utf-8'))
        if self.path == '/styles.css' and CSS:
            with open(CSS, "r") as f: lib.parse_css(f.read().encode('utf-8'))
        if self.path == '/script.js' and JS:
            with open(JS, "r") as f: lib.parse_js(f.read().encode('utf-8'))
        return super().do_GET()

def shutdown(s, f):
    print("Shutting down...")
    httpd.server_close()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

httpd = TCPServer(("", port), H)

print(f"Running on http://localhost:{port}")
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    shutdown(None, None)
