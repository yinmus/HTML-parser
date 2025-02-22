import os
import sys
import ctypes
import signal
import socket
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

def find_files(extension):
    return [f for f in os.listdir('.') if f.endswith(extension)]

def ask_file(extension, default=None):
    if default == "None":
        return None
    if default:
        return default
    files = find_files(extension)
    if files:
        print(f"Available {extension.upper()} files:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
    else:
        print(f"No {extension.upper()} files found.")
    
    choice = input("Enter number or custom path: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(files):
        return files[int(choice) - 1]
    return choice if choice else None

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

def kill_process_on_port(port):
    if sys.platform.startswith("linux"):
        os.system(f"fuser -k {port}/tcp")
    elif sys.platform.startswith("win"):
        os.system(f"netstat -ano | findstr :{port} > temp.txt && for /f \"tokens=5\" %i in (temp.txt) do taskkill /F /PID %i && del temp.txt")
    else:
        print("Unsupported OS for auto-kill. Kill process manually.")

if len(sys.argv) > 1:
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid port number.")
        sys.exit(1)
else:
    port = int(input("Enter port: "))

if is_port_in_use(port):
    choice = input(f"Port {port} is in use. Kill process? [y/n]: ").strip().lower()
    if choice == "y":
        kill_process_on_port(port)
    else:
        print("Exiting.")
        sys.exit(1)

HTMLfile = ask_file(".html", sys.argv[2] if len(sys.argv) > 2 else None)
JSfile = ask_file(".js", sys.argv[3] if len(sys.argv) > 3 else None)
CSSfile = ask_file(".css", sys.argv[4] if len(sys.argv) > 4 else None)

lib = ctypes.CDLL('./libparser.so')
lib.parse_html.argtypes = [ctypes.c_char_p]
lib.parse_js.argtypes = [ctypes.c_char_p]
lib.parse_css.argtypes = [ctypes.c_char_p]

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' and HTMLfile:
            with open(HTMLfile, "r") as f:
                content = f.read()
            lib.parse_html(content.encode('utf-8'))
        
        if self.path == '/styles.css' and CSSfile:
            with open(CSSfile, "r") as f:
                content = f.read()
            lib.parse_css(content.encode('utf-8'))
        
        if self.path == '/script.js' and JSfile:
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
