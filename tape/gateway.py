# Copyright (c) 2007-2009 The Tape Project.
# See LICENSE for details.

import pyamf

from twisted.web import http, static

def renderHomePage(request):
    request.write("""
    <html>
    <head>
      <title>Tape Server</title>
    </head>
    <body>
        <h2>Tape Server</h2>
        <p>
          Welcome!
        </p>
    </body>
    </html>""")
    request.finish()

def favicon(request):
    """Returns favicon.ico"""
    iconfile = open('resources/favicon.ico','r')
    request.write(iconfile.read())
    request.finish()
    iconfile.close()
    
def crossdomain(request):
    """Returns crossdomain.xml file"""
    cdfile = open('resources/crossdomain.xml','r')
    request.write(cdfile.read())
    request.finish()
    cdfile.close()

def remotingGateway(request):
    # Read HTTP Header
    contentType = request.getHeader('Content-Type')
    # Return AMF
    if contentType == GeneralTypes.AMF_MIMETYPE:
        # Add AMF headers to the response.
        request.setHeader('Content-Type', GeneralTypes.AMF_MIMETYPE)
        # Parse AMF data.
        input = decodeAMF(request.content)
        print input
        # Patch the path. there are only a few options:
        # - 'someurl' + method >> someurl.method
        # - 'someurl/someother' + method >> someurl.someother.method
        if not request.path.endswith('/'):
            request.path += '/'
        # Process AMF data.
        headers, body = processAMF(input, request.path)
        # Encode AMF data.
        output, contentLength = encodeAMF(headers, body)
        # Set header content length.
        request.setHeader('Content-Length', contentLength)
        # Write AMF response to the client.
        request.write(output)
    else:
        # Add text/html content-type header to the response.
        request.setHeader('Content-Type', 'text/html')
    # send back the response.
    request.finish()

"""
The http.Request class parses an incoming HTTP request and provides an
interface for working with the request and generating a response.
"""
class FlashRemotingGateway(http.Request):
    pageHandlers = {
        '/': renderHomePage,
        '/gateway': remotingGateway,
        '/crossdomain.xml': crossdomain,
        '/favicon.ico': favicon
        }
    
    """
    The process method will be called after the request has been completely
    received. It is responsible for generating a response and then calling
    self.finish() to indicate that the response is complete.
    """
    def process(self):
        # Use the path property to find out which path is being requested.
        if self.pageHandlers.has_key(self.path):
            handler = self.pageHandlers[self.path]
            # respond to page requests.  
            handler(self)
        else:
            # page not found
            self.setResponseCode(http.NOT_FOUND)
            self.write("""<html><head><title>Page Not Found</title></head>
                    <h1>404</h1></html>""")
            self.finish()
              
def decodeAMF(data):
    # If there is AMF content, then data will contain 
    # an instance of cStringIO.
    if data:
        amfData = data.getvalue()
        # Read AMF data. 
        amfDecoder = AMFMessageDecoder(amfData) 
        try:
            # Parse AMF request.
            amfRequest = amfDecoder.decode()
        except:
            raise
            print "FAILED to parse   ---> ", amfData.rsplit("\\",1)[-1],
        else:
            return amfRequest

def encodeAMF(headers, body):
    # Write AMF data. 
    amfEncoder = AMFMessageEncoder(headers, body) 
    # Encode AMF result.
    amfResult = amfEncoder.encode()
    # Return raw AMF and content length.
    return amfResult.getvalue(), str(amfResult.tell())
                    
def processAMF(amfMessage, path):
    # The AMF response headers to a request have the exact same structure as the 
    # request headers.
    headers = amfMessage.headers
    print "Original AMF Bodies:", amfMessage.bodies
    # add results to bodies.
    for body in amfMessage.bodies:
        # The AMF response body to a request has the exact same structure as the 
        # request body. 
        if isinstance(body, AMFMessageBody):
            try:
                # If the client requested something with response index "/1", and 
                # the call was successful, "/1/onResult" should be sent back.
                body.target = body.response + '/onResult'
                # Response: should be set to the string "null".
                body.response = 'null'
                # Data: set to the returned data. 
                # TODO: echo back exact data for now.
                # body.data = "Hello world!"
            except (SystemExit, KeyboardInterrupt):
                raise
            except:
                cls, e, tb = sys.exc_info()
                details = traceback.format_exception(cls, e, tb)
                # Return runtime error with "/onStatus". 
                body.target = body.response + '/onStatus'
                # Response: should be set to the string "null".
                body.response = 'null'
                # Data: set to the returned data.
                body.data = dict(
                    code='SERVER.PROCESSING',
                    level='Error',
                    description='%s: %s' % (cls.__name__, e),
                    type=cls.__name__,
                    details=''.join(details),
                )
    bodies = amfMessage.bodies
    print "Modified AMF Bodies:",  bodies     
    return headers, bodies
