from Stream import *


class FileStream(Stream):

    def __init__(self, stream):
        Stream.__init__(self, stream)

        self._overtake_attribute('fileno')
        self._overtake_attribute('flush')
        self._overtake_attribute('read')
        self._overtake_attribute('write')
        self._overtake_attribute('writelines')
        self._overtake_attribute('readline')
        self._overtake_attribute('readlines')
        self._overtake_attribute('update')

    def readline(self):
        c = ''
        s = ''
        while c != '\n':
            c = self.read(1)
            if c == '':
                time.sleep(0.001)
            s+= c
        print 'reading line:', repr(s)
        return s

    def readlines(self, sizehint = 0): # from StringIO
        """Read until EOF using readline() and return a list containing the
        lines thus read.

        If the optional sizehint argument is present, instead of reading up
        to EOF, whole lines totalling approximately sizehint bytes (or more
        to accommodate a final whole line).
        """
        total = 0
        lines = []
        line = self.readline()
        while line[-1:] == '\n': # here the difference
            lines.append(line)
            total += len(line)
            if 0 < sizehint <= total:
                break
            line = self.readline()
        return lines # also in StringStream    

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def update(self):
        pass
        
