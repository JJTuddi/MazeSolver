dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

# states for matrix
enqueued = 0
visited = 1

class Solve:
    def __init__(self, nRows, nCols, matrix, free, startValue, endValue):
        self._nRows = nRows
        self._nCols = nCols
        self._matrix = matrix
        self._free = free
        self._startValue = startValue
        self._endValue = endValue
        # i implemented a queue using a list, because i will need it later into shortest path algorithm
        self._pos = 0
        self._queue = [(startValue, -1, 0)]
        self.isThereAPath = False
        self._distMatrix = [0] * nRows
        for i in range(nRows):
            self._distMatrix[i] = [-1]* nCols
    def canWork(self):
        if self._pos >= len(self._queue):
            print("The algorithm is done, you can't do anything anymore, see the shortest path if it exists")
            if (self._pos == len(self._queue)):
                print("\tPS: there is no path, don't try")
            return False
        else:
            actual = self._queue[self._pos]
            discovery = actual[2]
            actual = actual[0]
            if self._matrix[actual[0]][actual[1]] != 30:
                self._matrix[actual[0]][actual[1]] = visited
            for i in range(len(dx)):
                if self._matrix[actual[0] + dx[i]][actual[1] + dy[i]] in self._free:
                    self._distMatrix[actual[0] + dx[i]][actual[1] + dy[i]] = discovery
                    self._queue.append(((actual[0] + dx[i], actual[1] + dy[i]), self._pos, discovery + 1))
                    self._matrix[actual[0] + dx[i]][actual[1] + dy[i]] = enqueued
                elif self._matrix[actual[0] + dx[i]][actual[1] + dy[i]] == 40:
                    self._queue.append(((actual[0] + dx[i], actual[1] + dy[i]), self._pos, discovery + 1))
                    self._pos = len(self._queue) + 1
                    self.isThereAPath = True
                    return False
            self._pos += 1
            return True
    def getMatrix(self):
        return self._matrix
    def getVector(self):
        return self._queue
    def getDistMatrix(self):
        return self._distMatrix
    def setDistMatrix(self, distMatrix):
        self._distMatrix = distMatrix