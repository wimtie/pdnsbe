#!/usr/bin/python

import sys
import profile
import pdnsbe.backend
import pdnsbe.core


class ExampleResolver(pdnsbe.backend.AbstractPDNSResolver):

    def lookup_query(self, query):
        return [pdnsbe.core.PDNSRecord("example.com", "IN", "A", 300, -1,
                                       "93.184.216.34")]


def main():
    try:
        s = pdnsbe.backend.ForkingPDNSBackendServer("/tmp/mysocket.socket")
        s.set_query_resolver(ExampleResolver())
        s.serve_forever()
    except KeyboardInterrupt:
        print "^C: exiting"

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "profile":
        profile.run("main()")
    else:
        main()
