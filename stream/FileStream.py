from Stream import *


class FileStream(Stream):

    def __init__(self, stream):
        Stream.__init__(self, stream)

        self._overtake_attribute('fileno')
        self._overtake_attribute('flush')
        self._overtake_attribute('read')
        self._overtake_attribute('write')
        self._overtake_attribute('writelines')
        self._overtake_attribute('readlines')

    def update(self):
        pass
        
