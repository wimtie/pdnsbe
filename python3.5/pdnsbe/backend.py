
""" Python Generic Backend for PowerDNS """

import socketserver
import logging
import pdnsbe.core as core


class PDNSResolver(object):

    def lookup_query(self, query: core.PDNSQuery) -> list:
        raise Exception("Not implemented.")


class PDNSBackendServer(socketserver.UnixStreamServer):

    def __init__(self, socket, loglevel=logging.INFO):
        self.__logger = logging.getLogger()
        self.__logger.setLevel(loglevel)
        logging.basicConfig(format="%(process)d %(processName)s %(levelname)s %(message)s")
        self.__resolver = None
        self.__logger.info("Init server...")
        socketserver.UnixStreamServer.__init__(self, socket, PDNSBackendHandler)

    def set_loglevel(self, loglevel):
        self.__logger.setLevel(loglevel)

    def get_loglevel(self):
        return self.__logger.getEffectiveLevel()

    def set_resolver(self, resolver: PDNSResolver):
        self.__logger.info("Setting resolver: %r" % resolver)
        self.__resolver = resolver

    def lookup_query(self, query: core.PDNSQuery) -> list:
        if self.__resolver is None:
            raise Exception("This backend server has no resolver set!")
        return self.__resolver.lookup_query(query)


class ForkingPNDSBackendServer(PDNSBackendServer, socketserver.ForkingMixIn):
    pass


class ThreadingPDNSBackendServer(PDNSBackendServer, socketserver.ThreadingMixIn):
    pass


class PDNSBackendHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.__server = server
        self.__logger = logging.getLogger()
        self.__logger.setLevel(server.get_loglevel())
        logging.basicConfig(format="%(process)d %(processName)s %(levelname)s %(message)s")
        self.__request = request
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        self.__f = self.__request.makefile(mode="rw")
        self.__version = self.__handshake()
        self.__logger.debug("Start handling")
        line = self.__readline()
        while line:
            query = self.__parse_query(line)
            results = self.__server.lookup_query(query)
            for result in results:
                self.__write_line_sync(self.__to_response_line(result))
            self.__write_line_sync("END")
            line = self.__readline()
        self.__logger.info("Done with session, exiting...")

    def __readline(self):
        return self.__f.readline().strip()

    def __handshake(self):
        line = self.__readline()
        matcher = core.HELO_REGEX.match(line)
        if matcher is None:
            raise core.PDNSHandshakeException("Handshake failed: %s" % line)
        _ = matcher.group(1)
        version = matcher.group(2)
        self.__write_line_sync("HELO\tdefault backend")
        return version

    def __parse_query(self, line) -> core.PDNSQuery:
        return core.PDNSQuery(*line.split(core.Q_SEPARATOR))

    def __write_line_sync(self, line: str):
        self.__f.write(line if line.endswith("\n") else "%s\n" % line)
        self.__f.flush()

    def __to_response_line(self, result: core.PDNSRecord):
        return "%s\t%s\t%s\t%s\t%d\t%d\t%s" % ("Q", result.get_name(), result.get_type(), result.get_class(),
                                               result.get_ttl(), result.get_id(), result.get_content())
