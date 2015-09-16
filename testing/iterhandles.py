#!/usr/bin/python

import sys
import profile
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
            return ""
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


def main(iterations):
    pdnsbe.backend.PDNSHandler(MockRequest(iterations), "8.8.8.8", MockServer())

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[2] == "-profile":
        profile.run("main(%d)" % int(sys.argv[1]))
    else:
        main(sys.argv[1])
