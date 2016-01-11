import asyncio.queues as queues
import logging
import click
import socketserver
import socket
import pdnsbe.backend as backend
import pdnsbe.core as core

logger =  logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(handlers=[logging.StreamHandler()])


class MockRequest(socket.socket):

    def __init__(self, helo_line, iterations):
        self.__helo_line = helo_line
        self.__counter = 0
        self.__iterations = iterations
        self.resolver = None
        self.__mode = None
        self.__closed = False
        self.__response_buffer = []

    def makefile(self, mode=None):
        self.__mode = mode
        return self

    def readline(self):
        if self.__closed:
            raise Exception("Something's amiss!")
        query = "Q\twww.example.com\tIN\tA\t-1\t8.8.8.8"
        if self.__counter == 0:
            logger.debug("sending helo")
            query = self.__helo_line
        if self.__counter == self.__iterations:
            # Last query has been sent
            query = ""
            return query
        self.__counter += 1
        logger.debug("Writing line %s" % query)
        return "%s\n" % query

    def write(self, line):
        self.__response_buffer.append(line)

    def flush(self):
        pass

    def close(self):
        self.__closed = True

    def read_response(self):
        return self.__response_buffer


class MockServer(object):

    def get_loglevel(self):
        return logging.DEBUG

    def lookup_query(self, query: core.PDNSQuery):
        return self.resolver.lookup_query(query)

    def register_handler(self, handler):
        self.handler = handler

    def unregister_handler(self, handler):
        logger.debug("registering handler!")

    def set_resolver(self, resolver: backend.PDNSResolver):
        self.resolver = resolver


class ExampleResolver(backend.PDNSResolver):

    def lookup_query(self, query):
        return [core.PDNSRecord("example.com", "IN", "A", 300, -1,
                                "93.184.216.34")]


def test_handler():
    logger.debug("testing handler")
    server = MockServer()
    server.set_resolver(ExampleResolver())
    request = MockRequest("HELO\t1", 1)
    handler = backend.PDNSBackendHandler(request, "8.8.8.8",
                                         server)
    server.register_handler(handler)
    for line in request.read_response():
        print("response line: %s" % line)
    handler.handle()


def test_handler_handshake():
    logger.debug("testing handshake")
    try:
        handler = backend.PDNSBackendHandler(MockRequest("LOLZ 1", 1), "8.8.8.8",
                                             MockServer())
        handler.handle()
    except core.PDNSHandshakeException:
        logger.info("Got expected exception")
        # this is what we want
        return
    raise Exception("test failed, expected exception")


@click.command()
def run_tests():
    test_handler_handshake()
    test_handler()


@click.command()
def profile():
    pass

if __name__ == "__main__":
    run_tests()
