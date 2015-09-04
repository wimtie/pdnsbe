# pypdns
Python PowerDNS Generic Backend

This is a simple pluggable library that allows the user to create a socket-based PowerDNS pipe backend. The server class extends SocketServer, so one would use it in the same manner.

All the user needs to do is extend the AbstractPDNSResolver class, implement its lookup_query method, and set that on the Server object.

Example:
```python
#!/usr/bin/python

import pypdns.backend
import pypdns.core


class ExampleResolver(pypdns.backend.AbstractPDNSResolver):

    def lookup_query(self, query):
        return [pypdns.core.PDNSRecord("example.com", "IN", "A", 300, -1,
                                       "93.184.216.34")]

 
s = pypdns.backend.ForkingPDNSBackendServer("/tmp/mysocket.socket")
s.set_query_resolver(ExampleResolver())
s.serve_forever()
```
