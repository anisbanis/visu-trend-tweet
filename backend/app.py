import os
from functools import wraps
from inspect import getfullargspec

from .server import CompleteHTTPServer
from .server import CompleteHTTPRequestHandler
from .server import serve

class Application:

    """    rules : { url -> {methods, args, endpoint} }    """
    rules = {}
    """    endpoint -> runnable    """
    endpoints = {}
    """    r_endpoint : endpoint -> url    """
    r_endpoint = {}

    method = None

    def __init__(self,
                 app_name,
                 serve_location=os.getcwd(),
                 port=8080,
                 host='127.0.0.1'
                 ):
        self.port = port
        self.host = host
        self.app_name = app_name
        self.loc = serve_location

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
            self.rules[url_rule] = {'methods':methods, 'endpoint': endpoint, 'args': args}
        else:
            _, c_endpoint = self.rules.get(url_rule)
            c_runnable = self.endpoints[c_endpoint]
            if c_endpoint == endpoint or c_runnable != runnable:
                raise ValueError(f'An endpoint for the url {url_rule} has already been defined.')

            if c_endpoint not in self.endpoints and c_runnable is None:
                # If there is either no current endpoint or there is no runnable
                # currently attached to it, we can safely add the new one
                self.rules[url_rule] = {'methods': methods, 'endpoint': endpoint, 'args': args}
                self.endpoints[endpoint] = runnable
                self.r_endpoint[endpoint] = url_rule

    def rule(self, url, methods=('GET',)):
        def decorator(f):
            self.make_rule(url_rule=url,
                           runnable=f,
                           methods=methods,
                           args=getfullargspec(f).args)
            return f
        return decorator

    def _exec_rule(self, rule, method, params):
        if method in self.rules[rule]['methods']:
            self.method = method

            endpoint = self.rules[rule]['endpoint']
            expected_params = self.rules[rule]['args']
            if set(expected_params) != set(params):
                raise ValueError(f'Error in call to {endpoint} : parametes mismatch\n'
                                 f'Got {list(params)} expected {expected_params}.')
            
            output = self.endpoints[endpoint](**params)
            self.method = None
            return output
        else:
            raise ValueError(f'Rule {rule} does not support method {method}.')

    def is_rule(self, rule):
        return rule in self.rules

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
        print('self.rules  ', self.rules)
        print('self.endpoints', self.endpoints)
        print('self.r_endpoint', self.r_endpoint)
