
""" Core concepts for PowerDNS backends """

import re


Q_SEPARATOR = "\t"
HELO_REGEX = re.compile("^(HELO)%s([1-3]{1})$" % Q_SEPARATOR)


class PDNSHandshakeException(Exception):
    pass


class PDNSRecord(object):

    def __init__(self, name: str, result_class: str, type: str, ttl: int, id: int, content: str):
        self.__name = name
        self.__result_class = result_class
        self.__type = type
        self.__ttl = ttl
        self.__id = id
        self.__content = content

    def get_name(self):
        return self.__name

    def get_class(self):
        return self.__result_class

    def get_type(self):
        return self.__type

    def get_ttl(self):
        return self.__ttl

    def get_id(self):
        return self.__id

    def get_content(self):
        return self.__content


class PDNSQuery(object):

    def __init__(self, q_command, q_name, q_class, q_type, q_id, q_remote_ip):
        self.__q_command = q_command
        self.__q_name = q_name
        self.__q_class = q_class
        self.__q_type = q_type
        self.__q_id = q_id
        self.__q_remote_ip = q_remote_ip

    def get_command(self):
        return self.__q_command

    def get_name(self):
        return self.__q_name

    def get_class(self):
        return self.__q_class

    def get_type(self):
        return self.__q_type

    def get_id(self):
        return self.__q_id

    def get_remote_ip(self):
        return self.__q_remote_ip
