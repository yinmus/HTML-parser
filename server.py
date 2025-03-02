import os
import sys
import ctypes
import signal
import socket
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
def port_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0
def killuport(port):
    if sys.platform.startswith("linux"):
        os.system(f"fuser -k {port}/tcp")
    elif sys.platform.startswith("win"):
        os.system(f"for /f \"tokens=5\" %i in ('netstat -ano ^| findstr :{port}') do taskkill /F /PID %i")
    else:
        print("Пожалуйста, завершите процесс вручную.")
def libr_load():
    lib = ctypes.CDLL('./libparser.so')
    lib.parse_html.argtypes = [ctypes.c_char_p]
    lib.parse_js.argtypes = [ctypes.c_char_p]
    lib.parse_css.argtypes = [ctypes.c_char_p]
    return lib
class Hdlr(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.html_path = kwargs.pop('html_path', None)
        self.js_path = kwargs.pop('js_path', None)
        self.css_path = kwargs.pop('css_path', None)
        self.lib = kwargs.pop('lib', None)
        super().__init__(*args, **kwargs)
    def do_GET(self):
        if self.path == '/' and os.path.exists(self.html_path):
            self.srv_file(self.html_path, "text/html", self.lib.parse_html)
        elif self.path == '/script.js' and self.js_path != "None" and os.path.exists(self.js_path):
            self.srv_file(self.js_path, "application/javascript", self.lib.parse_js)
        elif self.path == '/styles.css' and self.css_path != "None" and os.path.exists(self.css_path):
            self.srv_file(self.css_path, "text/css", self.lib.parse_css)
        else:
            super().do_GET()
    def srv_file(self, file_path, content_type, parse_func):
        with open(file_path, "r") as f:
            content = f.read()
            parse_func(content.encode('utf-8'))
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
def stdwm(signum, frame):
    print("Завершение работы...")
    httpd.server_close()
    sys.exit(0)
def main():
    if len(sys.argv) < 3:
        print("Использование: python server.py <port> <html> [js] [css]")
        sys.exit(1)
    port = int(sys.argv[1])
    html, js, css = sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None, sys.argv[4] if len(sys.argv) > 4 else None
    if port_use(port):
        choice = input(f"Порт {port} используется. Завершить процесс? [y/n]: ").strip().lower()
        if choice == 'y':
            killuport(port)
            while port_use(port):
                pass
        else:
            sys.exit(1)
    lib = libr_load()
    signal.signal(signal.SIGINT, stdwm)
    signal.signal(signal.SIGTERM, stdwm)
    handler = lambda *args, **kwargs: Hdlr(*args, **kwargs, html_path=html, js_path=js, css_path=css, lib=lib)
    httpd = TCPServer(("", port), handler)
    print(f"Сервер запущен на http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        stdwm(None, None)
if __name__ == "__main__":
    main()
