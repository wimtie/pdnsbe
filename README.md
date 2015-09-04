# pypdns
Python PowerDNS Generic Backend

This is a simple pluggable library that allows the user to create a socket-based PowerDNS pipe backend. The server class extends SocketServer, so one would use it in the same manner.

All the user needs to do is extend the AbstractPDNSResolver class, implement its lookup_query method, and set that on the Server object.

Example:
```
 1 #!/usr/bin/python
 2
 3 import pypdns.backend
 4 import pypdns.core
 5
 6
 7 class ExampleResolver(pypdns.backend.AbstractPDNSResolver):
 8
 9     def lookup_query(self, query):
10         return [pypdns.core.PDNSRecord("example.com", "IN", "A", 300, -1,
11                                        "93.184.216.34")]
12
13
14 s = pypdns.backend.ForkingPDNSBackendServer("/tmp/mysocket.socket")
15
16 s.set_query_resolver(ExampleResolver())
17
18 s.serve_forever()
```
