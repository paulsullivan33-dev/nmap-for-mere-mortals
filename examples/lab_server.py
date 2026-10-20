#!/usr/bin/env python3
"""Specimen listeners for "Nmap for Mere Mortals".

Stands up four small services on this machine so the
guide's scans have something of *yours* to look at:

    TCP 8080   a tiny web server ("LabHTTP/1.0")
    TCP 8022   a banner server wearing an SSH-style banner
    TCP 8888   a greeting server ("LABCHAT")
    UDP 53535  a listener that answers any datagram

Two ports are deliberately left closed, because a
closed port is a lesson too:

    TCP 59999  nothing here — a closed port
    UDP 59998  nothing here either

Usage:
    python3 lab_server.py            run until Ctrl-C
    python3 lab_server.py --check    print what would listen, then exit

Everything is bound to all local interfaces so the
services answer on 127.0.0.1 and on this machine's
own network address alike. The services are
specimens: the web page is invented, the "SSH"
banner is a costume (there is no SSH server
behind it), and the chat server believes anything
you tell it. Run this only on a machine you own.
"""

import socket
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

WEB_PORT = 8080
BANNER_PORT = 8022
CHAT_PORT = 8888
UDP_PORT = 53535

PAGE = """<!DOCTYPE html>
<html>
<head><title>Lab Web - Specimen Page</title></head>
<body>
<h1>Lab Web</h1>
<p>This page belongs to the nmap lab. It is a
specimen: a real web server, serving an invented
page, on a machine you own, so that a scan has
something honest to find.</p>
</body>
</html>
"""


class LabWebHandler(BaseHTTPRequestHandler):
    server_version = "LabHTTP/1.0"
    sys_version = ""

    def do_GET(self):
        body = PAGE.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # keep the lab quiet
        pass


def banner_server():
    """Answer each connection with an SSH-style banner."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", BANNER_PORT))
    sock.listen(5)
    while True:
        conn, _ = sock.accept()
        try:
            conn.settimeout(2)
            conn.sendall(b"SSH-2.0-OpenSSH_9.6p1 LabSSH\r\n")
            conn.recv(1024)  # whatever the client says, we nod
        except (socket.timeout, ConnectionError, OSError):
            pass  # a rude client must not kill the lab
        finally:
            conn.close()


def chat_server():
    """Greet, echo one line back, hang up."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", CHAT_PORT))
    sock.listen(5)
    while True:
        conn, _ = sock.accept()
        try:
            conn.settimeout(5)
            conn.sendall(b"LABCHAT 1.0 ready - say something\r\n")
            data = conn.recv(1024)
            if data:
                reply = b"you said: " + data.strip() + b"\r\n"
                conn.sendall(reply)
        except (socket.timeout, ConnectionError, OSError):
            pass  # a rude client must not kill the lab
        finally:
            conn.close()


def udp_server():
    """Answer any datagram with a short proof of life."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", UDP_PORT))
    while True:
        try:
            _, addr = sock.recvfrom(1024)
            sock.sendto(b"lab-udp alive\n", addr)
        except OSError:
            pass  # keep listening whatever one datagram does


def main():
    if "--check" in sys.argv:
        print(f"would listen: tcp/{WEB_PORT} (web), "
              f"tcp/{BANNER_PORT} (banner), tcp/{CHAT_PORT} (chat), "
              f"udp/{UDP_PORT} (udp)")
        print("deliberately closed: tcp/59999, udp/59998")
        return
    for target in (banner_server, chat_server, udp_server):
        threading.Thread(target=target, daemon=True).start()
    web = ThreadingHTTPServer(("0.0.0.0", WEB_PORT), LabWebHandler)
    print(f"lab listening: tcp/{WEB_PORT}, tcp/{BANNER_PORT}, "
          f"tcp/{CHAT_PORT}, udp/{UDP_PORT} — Ctrl-C to stop")
    try:
        web.serve_forever()
    except KeyboardInterrupt:
        print("\nlab stopped")


if __name__ == "__main__":
    main()
