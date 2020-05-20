import os
from functools import wraps
from .server import CompleteHTTPServer
from .server import CompleteHTTPRequestHandler
from .server import serve

class Application:

    """    rules : { url -> (methods, endpoint) }    """
    rules = {}
    """    endpoint -> runnable    """
    endpoints = {}
    """    r_endpoint : endpoint -> url    """
    r_endpoint = {}

    def __init__(self,
                 app_name,
                 serve_location=os.getcwd(),
                 port=8080,
                 host='127.0.0.1'
                 ):
        pass

    def _endpoint_with_runnable(self, runnable):
        if runnable is None:
            raise ValueError('Either endpoint or runnable'
                             'should be provided.')
        return runnable.__name__

    def make_rule(self, url_rule='/', runnable=None, endpoint=None, args=None, methods=('GET',)):
        if endpoint is None:
            endpoint = self._endpoint_with_runnable(runnable)

        if url_rule not in self.rules:
            if endpoint not in self.endpoints and endpoint not in self.r_endpoint:
                # If the endpoint does not exist, we register it
                self.endpoints[endpoint] = runnable
                self.r_endpoint[endpoint] = url_rule
            # If the endpoint has already been registered and the provided url
            # has not been allocated, we can safely bind the two together
            self.rules[url_rule] = (methods, endpoint)
        else:
            _, c_endpoint = self.rules.get(url_rule)
            c_runnable = self.endpoints[c_endpoint]
            if c_endpoint == endpoint or c_runnable != runnable:
                raise ValueError(f'An endpoint for the url {url_rule} has already been defined.')

            if c_endpoint not in self.endpoints and c_runnable is None:
                # If there is either no current endpoint or there is no runnable
                # currently attached to it, we can safely add the new one
                self.rules[url_rule] = (methods, endpoint)
                self.endpoints[endpoint] = runnable
                self.r_endpoint[endpoint] = url_rule

    def rule(self, url):
        def decorator(f):
            self.make_rule(url_rule=url, runnable=f)
            return f
        return decorator

    def run(self):
            serve(directory='frontend',
                  bind='127.0.0.1',
                  threaded = True,
                  wait_for_threads = True,
                  app=self
                )

    def url_for(self, endpoint):
        rule = self.endpoints.get(endpoint, None)
        if rule:
            return f'http://{self.host}:{self.port}/{rule}'
        else:
            raise ValueError('Unknown provided endpoint {endpoint}.')

    def print_state(self):
        from pprint import pprint
        pprint(f'{self.rules=}')
        pprint(f'{self.endpoints=}')
        pprint(f'{self.r_endpoint=}')
