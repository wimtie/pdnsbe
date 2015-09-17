#!/usr/bin/python

import sys
import logging
import click
import cProfile
import pdnsbe.backend

RECORD = pdnsbe.core.PDNSRecord("example.com", "IN", "A", 300, -1,
                                "93.184.216.34")


class MockRequest(object):

    def __init__(self, max_iterations):
        self.__max_iterations = max_iterations
        self.__counter = 0

    def makefile(self):
        return self

    def readline(self):
        if self.__counter < 1:
            self.__counter += 1
            return "HELO\t1"
        if self.__counter > self.__max_iterations:
            return "\n"
        self.__counter += 1
        return "Q\twww.booking.com\tIN\tA\t-1\t8.8.8.8"

    def write(self, line):
        pass
        # print line

    def flush(self):
        # nothing to flush
        pass

    def close(self):
        self.__file.close()


class MockServer(object):

    def __init__(self):
        pass

    def get_banner(self):
        return "PROFILING MOCK SERVER"

    def lookup_query(self, query):
        return [RECORD]

    def get_loglevel(self):
        return logging.WARNING


@click.command()
@click.option("--iterations", "-i", help="iterations (queries) to run",
              required = True)
@click.option("--profile", "-p", help="use cProfile", is_flag = True,
              default = False)
def main(iterations, profile):
    iterations = int(iterations)
    if profile:
        cProfile.run("run(%d)" % iterations)
        return
    run(iterations)


def run(iterations):
    pdnsbe.backend.PDNSHandler(MockRequest(iterations), "8.8.8.8", MockServer())

if __name__ == "__main__":
    main()
