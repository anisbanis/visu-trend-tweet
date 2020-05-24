#!/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import sys
import os
import socket
from threading import Thread
from functools import partial
from urllib.parse import urlparse, parse_qsl

from .tools import progress_bar

class CompleteHTTPServer(HTTPServer):
    threaded = False
    _threads = None
    wait_for_threads = True

    def _process_request(self, request, client_address):
        try:
            self.finish_request(request, client_address)
        except Exception:
            self.handle_error(request, client_address)
        finally:
            self.shutdown_request(request)

    def process_request(self, request, client_address):
        if not self.threaded:
            self._process_request(request, client_address)
        else:
            thread = Thread(target = self._process_request,
                                    args = (request, client_address))
            thread.daemon = True
            if self.wait_for_threads:
                if self._threads is None:
                    self._threads = []
                self._threads.append(thread)
            thread.start()

    def server_close(self):
        super().server_close()
        if self.wait_for_threads:
            threads, self._threads = self._threads, None
            if threads:
                l = len(threads)
                progress_bar((t.join() for t in threads),
                             l,
                             prefix='Waiting for threads :',
                             suffix='Completed :',
                             bar_length=50)
        else:
            print('Not waiting for threads, terminating.')
    

class CompleteHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.directory = kwargs.pop('directory')
        self.app = kwargs.pop('app')
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        url = urlparse(self.path)
        path = url.path
        query = dict(parse_qsl(url.query))

        if self.app.is_rule(path):
            output = bytes(str(self.app._exec_rule(path, 'GET', query)), 'utf-8')
            self.wfile.write(output)
        else:
            super().do_GET()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        data_input = self.rfile.read(int(self.headers['Content-Length']))

        if not 'json' in self.headers['Content-Type']:
            self.send_response(501)
            self.end_headers()
            return

        self.send_response(200)
        self.end_headers()

        url = urlparse(self.path)
        path = url.path
        query = dict(parse_qsl(url.query))

        import json
        data = json.loads(data_input)

        if self.app.is_rule(path):
            output = bytes(str(self.app._exec_rule(path,
                                                   'POST',
                                                   dict(query, data=data))),
                           'utf-8')
            self.wfile.write(output)
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def _get_addr_family(*address):
    # retrieve socket address
    info = socket.getaddrinfo(*address,
                              type=socket.SOCK_STREAM,
                              flags=socket.AI_PASSIVE)
    family, _, _, _, sockaddr = next(iter(info))
    return family, sockaddr

def serve(ServerClass=CompleteHTTPServer,
          HandlerClass=CompleteHTTPRequestHandler,
          protocol='HTTP/1.1',
          port=8080,
          directory='.',
          bind=None,
          threaded=False,
          wait_for_threads=False,
          app=None):

    ServerClass.address_family, addr = _get_addr_family(bind, port)
    HandlerClass = partial(HandlerClass, directory=directory, app=app)
    HandlerClass.protocol_version = protocol

    with ServerClass(server_address=addr,
                     RequestHandlerClass=HandlerClass) as httpd:
        httpd.threaded = threaded
        httpd.wait_for_threads = wait_for_threads

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
