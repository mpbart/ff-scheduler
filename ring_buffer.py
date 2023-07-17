class RingBuffer:
    def __init__(self, names):
        self.__buffer = [name for name in names]

    def shift(self):
        tmp = self.__buffer[-1]
        for i in reversed(xrange(2, len(self.__buffer))):
            self.__buffer[i] = self.__buffer[i - 1]
        self.__buffer[1] = tmp

    @property
    def buffer(self):
        return self.__buffer

    def get_opposites(self):
        results = []
        for i in xrange(len(self.__buffer) / 2):
            results.append((self.__buffer[i], self.__buffer[len(self.__buffer) - 1 - i]))
        return results
