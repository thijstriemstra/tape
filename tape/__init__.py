# Copyright (c) 2007-2009 The Tape Project.
# See LICENSE for details.

"""
Tape is a media server for the Flash Platform.

@copyright: Copyright (c) 2007-2009 The Tape Project. All Rights Reserved.
@contact: U{tape-dev@collab.eu<mailto:tape-dev@collab.eu>}
@see: U{http://tape.collab.eu}

@since: August 2007
@status: Planning
@version: 0.1
"""

import sys
from twisted.web import http, server, resource, static
from twisted.application import service
from twisted.python import usage
import twisted.scripts.twistd as td

import services
from services import RemotingServer, RTMPServer
from log import LogService

__all__ = ['__version__']

#: Tape version number.
__version__ = (0, 1, 0, 'planning')

LOG_DIR             = "."
ERROR_LOG_NAME      = "error.log"
ACCESS_LOG_NAME     = "access.log"

rtmpMode = "server"
rtmpHost = "0.0.0.0"
rtmpPort = 1935
httpHost = "0.0.0.0"
httpPort = 8080

def run():
    tdcmds = ["-no", "-y", __file__]
    tdoptions = td.ServerOptions()
    try:
        tdoptions.parseOptions(tdcmds)
    except usage.UsageError, errortext:
        print '%s' % (errortext)
        sys.exit(1)
    # run app with twistd
    td.runApp(tdoptions)
    
if __name__ == '__main__':
    run()

else:
    # Normal twistd startup.
    application = service.Application("Tape")

    # Create a MultiService, and hook up a the RTMP
    # and HTTP TCPServers as children.
    flashServices = service.MultiService()

    # HTTP/AMF server.
    remotingServer = RemotingServer(httpHost, httpPort)
    remotingServer.setServiceParent(flashServices)

    # RTMP server.
    rtmpServer = RTMPServer(rtmpHost, rtmpPort)
    rtmpServer.setServiceParent(flashServices)

    # Connect services to the application.
    flashServices.setServiceParent(application)
    
    LogService(ACCESS_LOG_NAME, LOG_DIR, "access").setServiceParent(application)
    LogService(ERROR_LOG_NAME, LOG_DIR, "error").setServiceParent(application)
