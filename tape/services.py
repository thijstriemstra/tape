# Copyright (c) 2007-2009 The Tape Project.
# See LICENSE for details.

from twisted.application import internet
from twisted.internet import protocol
from twisted.web import http

from rtmpy.rtmp import RTMPProtocol, Modes
from gateway import FlashRemotingGateway

class RTMPServerFactory(protocol.ServerFactory):
    protocol = RTMPProtocol
    mode = Modes.SERVER

class RTMPClientFactory(protocol.ClientFactory):
    protocol = RTMPProtocol
    mode = Modes.CLIENT

class FlashRemoting(http.HTTPChannel):
    requestFactory = FlashRemotingGateway

class RemotingServerFactory(http.HTTPFactory):
    protocol = FlashRemoting

class RTMPServer(internet.TCPServer):
    def __init__(self, host, port):
        internet.TCPServer.__init__(self, port, RTMPServerFactory())

class RTMPClient(internet.TCPClient):
    def __init__(self, host, port):
        internet.TCPClient.__init__(self, host, port, RTMPClientFactory())

class RemotingServer(internet.TCPServer):
    def __init__(self, host, port):
        internet.TCPServer.__init__(self, port, RemotingServerFactory())
