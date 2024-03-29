
import socket
import cPickle

import sys
sys.path.append('..')

try:
    import stream.PickleStream as PickleStream
    import stream.StreamWrap as StreamWrap
except ImportError:
    sys.path.remove('..')
    import distobj.stream.PickleStream as PickleStream
    import distobj.stream.StreamWrap as StreamWrap

try:
    from socket import create_connection
except ImportError:
    # stolen from socket for older python versions
    _GLOBAL_DEFAULT_TIMEOUT = object()

    def create_connection(address, timeout=_GLOBAL_DEFAULT_TIMEOUT,
                          source_address=None):
        """Connect to *address* and return the socket object.

        Convenience function.  Connect to *address* (a 2-tuple ``(host,
        port)``) and return the socket object.  Passing the optional
        *timeout* parameter will set the timeout on the socket instance
        before attempting to connect.  If no *timeout* is supplied, the
        global default timeout setting returned by :func:`getdefaulttimeout`
        is used.  If *source_address* is set it must be a tuple of (host, port)
        for the socket to bind as a source address before making the connection.
        An host of '' or port 0 tells the OS to use the default.
        """

        host, port = address
        err = None
        for res in getaddrinfo(host, port, 0, SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            sock = None
            try:
                sock = socket(af, socktype, proto)
                if timeout is not _GLOBAL_DEFAULT_TIMEOUT:
                    sock.settimeout(timeout)
                if source_address:
                    sock.bind(source_address)
                sock.connect(sa)
                return sock

            except error as _:
                err = _
                if sock is not None:
                    sock.close()

        if err is not None:
            raise err
        else:
            raise error("getaddrinfo returns an empty list")

def wrapSocketForPickle(sock):
    file = StreamWrap.SocketStream(sock)
    return PickleStream.PickleStream(file)

    
def createPickleConnection(address, *args, **kw):
    sock = create_connection(address, *args, **kw)
    return wrapSocketForPickle(sock)
