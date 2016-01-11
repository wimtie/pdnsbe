#!/usr/bin/python

import sys
import profile
import pdnsbe.backend
import pdnsbe.core
import logging

logger = logging.getLogger()
logging.basicConfig(format="%(process)d %(processName)s %(levelname)s %(message)s")
logger.setLevel(logging.INFO)
logger.info("PowerDNS backend handler init")


class ExampleResolver(pdnsbe.backend.PDNSResolver):

    def lookup_query(self, query):
        return [pdnsbe.core.PDNSRecord("example.com", "IN", "A", 300, -1,
                                       "93.184.216.34")]


def main():
    try:
        logger.info("Starting example server")
        s = pdnsbe.backend.ForkingPDNSBackendServer("/tmp/example.socket")
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
