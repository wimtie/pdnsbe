#!/usr/bin/python

import sys
import os
import profile
import pdnsbe.backend
import pdnsbe.core
import logging

EXAMPLE_SOCKET = "/tmp/example.socket"

logger = logging.getLogger()
logging.basicConfig(format="%(process)d %(processName)s %(levelname)s %(message)s")
logger.setLevel(logging.DEBUG)
logger.info("PowerDNS backend handler init")


class ExampleResolver(pdnsbe.backend.PDNSResolver):

    def lookup_query(self, query):
        return [pdnsbe.core.PDNSRecord("example.com", "IN", "A", 300, -1,
                                       "93.184.216.34")]


def main():
    if os.path.exists(EXAMPLE_SOCKET):
        os.unlink(EXAMPLE_SOCKET)
    try:
        logger.info("Starting example server")
        s = pdnsbe.backend.ThreadingPDNSBackendServer(EXAMPLE_SOCKET)
        s.set_resolver(ExampleResolver())
        s.serve_forever()
        logger.info("Example server shutting down")
    except KeyboardInterrupt:
        print("^C: exiting")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "profile":
        profile.run("main()")
    else:
        main()
