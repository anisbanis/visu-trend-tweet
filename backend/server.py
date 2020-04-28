#!/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import socket

def _get_addr_family(*address):
    # retrieve socket address
    info = socket.getaddrinfo(*address,
                              type=socket.SOCK_STREAM,
                              flags=socket.AI_PASSIVE)
    family, _, _, _, sockaddr = next(iter(info))
    return family, sockaddr

def serve(ServerClass=HTTPServer,
          HandlerClass=BaseHTTPRequestHandler,
          protocol='HTTP/1.0',
          port=8080,
          bind=None):
    ServerClass.address_family, addr = _get_addr_family(bind, port)
    HandlerClass.protocol_version = protocol

    with ServerClass(addr, HandlerClass) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f'[{host}]' if ':' in host else host
        print(
            f"Serving HTTP on {host} port {port} "
            f"(http://{url_host}:{port}/) ..."
        )
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)

if __name__ == '__main__':
    serve(HTTPServer, BaseHTTPRequestHandler, bind='127.0.0.1')
