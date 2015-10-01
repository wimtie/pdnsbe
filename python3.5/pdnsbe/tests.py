import logging
import click
import pdnsbe.backend as backend
import pdnsbe.core as core


class MockRequest(object):

    def __init__(self, helo_line):
        self.__helo_line = helo_line
        self.__counter = 0

    def makefile(self):
        return self

    def readline(self):
        if self.__counter == 0:
            return self.__helo_line
        return "Q\twww.booking.com\tIN\tA\t-1\t8.8.8.8"


class MockServer(object):

    def get_loglevel(self):
        return logging.DEBUG


def test_handler():
    handler = backend.PDNSBackendHandler(MockRequest("HELO\t1"), "8.8.8.8", MockServer())
    handler.handle()


def test_handler_handshake():
    try:
        handler = backend.PDNSBackendHandler(MockRequest("EHLO 1"), "8.8.8.8", MockServer())
        handler.handle()
    except core.PDNSHandshakeException:
        # this is what we want
        return
    raise Exception("test failed, expected exception")


@click.command()
def run_tests():
    test_handler()
    test_handler_handshake()


@click.command()
def profile():
    pass

if __name__ == "__main__":
    run_tests()