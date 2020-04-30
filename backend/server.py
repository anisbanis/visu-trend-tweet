#!/bin/python3

from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import sys
import os
import socket
from threading import Thread
from functools import partial

from .tools import progress_bar

class CompleteHTTPServer(HTTPServer)
    threaded = False
    _threads = None
    wait_for_threads = True

    def _process_request(self, request, client_address):
        from time import sleep
        try:
            self.finish_request(request, client_address)
            sleep(10)
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

class CompleteHTTPRequestHandler(BaseHTTPRequestHandler):
    handler = None
    pass

def _get_addr_family(*address):
    # retrieve socket address
    info = socket.getaddrinfo(*address,
                              type=socket.SOCK_STREAM,
                              flags=socket.AI_PASSIVE)
    family, _, _, _, sockaddr = next(iter(info))
    return family, sockaddr

def serve(ServerClass=HTTPServer,
          HandlerClass=BaseHTTPRequestHandler,
          protocol='HTTP/1.1',
          port=8080,
          bind=None,
          threaded=False,
          wait_for_threads=False,
          *args, **kwargs):

    ServerClass.address_family, addr = _get_addr_family(bind, port)
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

def main():
    print(os.getcwd())
    serve(CompleteHTTPServer,
          partial(SimpleHTTPRequestHandler, directory = os.path.join(os.getcwd(), 'frontend')),
          bind='127.0.0.1',
          threaded = True,
          wait_for_threads = True)
