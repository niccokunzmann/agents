def writeString(stream, string):
    stream.write(str(len(string)) + '\n')
    stream.write(string)

def readString(stream):
    length = int(stream.readline())
    return stream.read(length)

def writeStringTuple(stream, tup):
    if not (type(tup is tuple) and all([type(e) is str for e in tup])):
        raise ValueError('tuple elements must be strings')
    stream.write(str(len(tuple)) + '\n')
    for e in tup:
        writeString(stream, s)

def readStringTuple(stream):
    length = int(stream.readline())
    return tuple([readString(stream) for i in xrange(length)])
    
