# -*- coding: utf8 -*-

# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import json
import socket


class Client:
    """JSON Connection to anaconda server
    """

    def __init__(self, host, port=None, timeout=None):

        if timeout is None:
            timeout = socket._GLOBAL_DEFAULT_TIMEOUT
        self.timeout = timeout

        self.host = host
        self.port = port
        self.sock = None
        self.file = None

    def connect(self):
        """Connect to the specified host and port in constructor time
        """

        self.sock = socket.create_connection(
            (self.host, self.port), self.timeout
        )

    def close(self):
        """Close the connection to the anaconda server
        """

        if self.sock:
            self.sock.close()
            self.sock = None

    def send(self, data):
        """
        Send data to the anaconda server in JSON formated string with
        new line ending
        """

        if self.sock is None:
            self.connect()

        self.sock.send(bytes('{}\r\n'.format(data), 'UTF-8'))

    def request(self, method, **kwargs):
        """Send a request to the server
        """

        kwargs['method'] = method
        self.send(json.dumps(kwargs))

        return self.getresponse()

    def getresponse(self):
        """Get the response from the server
        """

        if self.file is None:
            self.file = self.sock.makefile('r')

        try:
            line = self.file.readline()
        except socket.error as e:
            self.close()
            raise RuntimeError('Connection unexpectedly closed: ' + str(e))

        if not line:
            self.close()
            raise RuntimeError('Connection unexpectedly closed')

        self.file.close()
        self.file = None
        self.close()

        return json.loads(line)
