#!/usr/bin/python

import os
import sys
import ctypes
import signal
import socket
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

def port_use(p):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", p)) == 0

def killuport(p):
    if sys.platform.startswith("linux"):
        os.system(f"fuser -k {p}/tcp")
    elif sys.platform.startswith("win"):
        os.system(f"for /f \"tokens=5\" %i in ('netstat -ano ^| findstr :{p}') do taskkill /F /PID %i")
    else:
        print("Kill process manually.")

def libr_load():
    lib = ctypes.CDLL('./libparser.so')
    lib.parse_html.argtypes = [ctypes.c_char_p]
    lib.parse_js.argtypes = [ctypes.c_char_p]
    lib.parse_css.argtypes = [ctypes.c_char_p]
    return lib

class Hdlr(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        self.html_path, self.js_path, self.css_path, self.lib = kw.pop('html_path', None), kw.pop('js_path', None), kw.pop('css_path', None), kw.pop('lib', None)
        super().__init__(*a, **kw)
    def do_GET(self):
        if self.path == '/' and os.path.exists(self.html_path):
            self.srv_file(self.html_path, "text/html", self.lib.parse_html)
        elif self.path == '/script.js' and self.js_path != "None" and os.path.exists(self.js_path):
            self.srv_file(self.js_path, "application/javascript", self.lib.parse_js)
        elif self.path == '/styles.css' and self.css_path != "None" and os.path.exists(self.css_path):
            self.srv_file(self.css_path, "text/css", self.lib.parse_css)
        else:
            super().do_GET()
    def srv_file(self, path, ctype, func):
        with open(path, "r") as f:
            d = f.read()
            func(d.encode('utf-8'))
            self.send_response(200)
            self.send_header("Content-type", ctype)
            self.end_headers()
            self.wfile.write(d.encode('utf-8'))

def stdwm(sig, frame):
    global httpd
    print("Exit...")
    httpd.server_close()
    sys.exit(0)

def main():
    global httpd
    if len(sys.argv) < 3:
        print("Usage: python server.py <port> <html> [js] [css]")
        sys.exit(1)
    p, html, js, css = int(sys.argv[1]), sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None, sys.argv[4] if len(sys.argv) > 4 else None
    if port_use(p):
        if input(f"Port {p} in use. Kill process? [y/n]: ").strip().lower() == 'y':
            killuport(p)
            while port_use(p):
                pass
        else:
            sys.exit(1)
    lib = libr_load()
    signal.signal(signal.SIGINT, stdwm)
    signal.signal(signal.SIGTERM, stdwm)
    httpd = TCPServer(("", p), lambda *a, **kw: Hdlr(*a, **kw, html_path=html, js_path=js, css_path=css, lib=lib))
    print(f"Server running on http://localhost:{p}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        stdwm(None, None)

if __name__ == "__main__":
    main()
