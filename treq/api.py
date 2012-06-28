from zope.interface import implements

from twisted.internet import reactor
from twisted.internet.defer import succeed

from twisted.web.client import Agent
from twisted.web.iweb import IBodyProducer
from twisted.web.http_headers import Headers

from treq.response import Response


def head(url, headers=None, params=None):
    return request('HEAD', url, headers, params)


def get(url, headers=None, params=None):
    return request('GET', url, headers, params)


def post(url, headers=None, body=None):
    return request('POST', url, headers, body)


def put(url, headers=None, body=None):
    return request('PUT', url, headers, body)


def delete(url, headers=None):
    return request('DELETE', url, headers)


def request(method, url, headers=None, body=None):
    if body:
        body = _StringProducer(body)

    d = _getAgent().request(method, url, Headers(headers), body)
    d.addCallback(Response, method)

    return d


#
# Private API
#

class _StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


_agent = None


def _getAgent():
    global _agent

    if _agent is not None:
        return _agent

    _agent = Agent(reactor)
    return _agent
