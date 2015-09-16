#!/usr/bin/python

import socket
import sys


verbose = False

if len(sys.argv) > 2 and sys.argv[2] == "-v":
    verbose = True

def read():
    return f.readline().strip()


def main():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect("/tmp/mysocket.socket")
    f = sock.makefile()
    f.write("HELO\t1\n")
    f.flush()
    host = "vcs-edge-2.c.booking.com"
    host = "c.booking.com"
    myip = "1.0.64.10"
    myip = "37.10.26.3"
    myip = "8.8.8.8"
    query = "Q\t%s\tIN\tANY\t-1\t%s\n" % (host, myip)

    for i in range(1, int(sys.argv[1])):
        f.write(query)
        f.flush()
        line = read()
        while line:
            if verbose:
                print line
            if line.startswith("END"):
                break
            line = read()
