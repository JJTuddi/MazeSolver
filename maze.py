import pygame
import random
import solver
r = random.randint
imgSize = 32
class Maze():
    def __init__(self, nRows, nColumns, ecran, font):
        # loading the textures for the canvas
        self._water = [0] * 4
        self._magma = [0] * 4
        for i in range(4):
            self._water[i] = pygame.image.load(f"img\\water\\water{i + 1}.png")
        for i in range(4):
            self._magma[i] = pygame.image.load(f"img\\magma\\magma{i + 1}.png")
        self._start = pygame.image.load("img\\boat.png")
        self._end = pygame.image.load("img\\chest.png")
        self._enqueued = pygame.image.load("img\\actual.png")
        self._visited = pygame.image.load("img\\vizitat.png")
        # setting the starting and ending point to null
        self._startPoint = 0
        self._endPoint = 0

        self._ecran = ecran
        self._nRows = nRows
        self._nColumns = nColumns
        self._matrix = [0] * nRows
        for i in range(nRows):
            self._matrix[i] = [0] * nColumns
        self.initializeMatrix()
        self._font = font

        self._s = 0
    def borderMatrix(self):
        # creates the magma wall
        for i in range(self._nRows):
            self._matrix[i][0] = self._matrix[i][self._nColumns - 1] = 20 + r(1, 4)
        for i in range(self._nColumns):
            self._matrix[0][i] = self._matrix[self._nRows - 1][i] = 20 + r(1, 4)
    def initializeMatrix(self):
        # puts only water and magma wall, and reset the states of the class
        self._s = 0
        self._startPoint = self._endPoint = 0
        for i in range(self._nRows):
            for j in range(self._nColumns):
                self._matrix[i][j] = 10 + r(1, 4)
        self.borderMatrix()
    def showMatrix(self):
        # setting images on canvas
        if self._s != 0:
            distMatrix = self._s.getDistMatrix()
        for i in range(self._nRows):
            for j in range(self._nColumns):
                if self._matrix[i][j] // 10 == 0:
                    if self._matrix[i][j] == 0:
                        self._ecran.blit(self._visited, (i * imgSize, j * imgSize))
                    elif self._matrix[i][j] == 1:
                        self._ecran.blit(self._enqueued, (i * imgSize, j * imgSize))
                elif self._matrix[i][j] // 10 == 1:
                    self._ecran.blit(self._water[self._matrix[i][j] % 10 - 1], (i * imgSize, j * imgSize))
                elif self._matrix[i][j] // 10 == 2:
                    self._ecran.blit(self._magma[self._matrix[i][j] % 10 - 1], (i * imgSize, j * imgSize))
                elif self._matrix[i][j] // 10 == 3:
                    self._ecran.blit(self._start, (i * imgSize, j * imgSize))
                elif self._matrix[i][j] // 10 == 4:
                    self._ecran.blit(self._end, (i * imgSize, j * imgSize))
                if self._s != 0 and distMatrix[i][j] >= 0:
                    self._ecran.blit(self._font.render(str(distMatrix[i][j]), True, self.getColor(distMatrix[i][j])), (i * imgSize, j * imgSize))
    def draw(self, x, y):
        # a long long condition to not kill the boat or the treasure
        if self._testXY(x, y) and (self._startPoint != 0 and (self._startPoint[0] != x or self._startPoint[1] != y)) and (self._endPoint != 0 and (self._endPoint[0] != x or self._endPoint[1] != y)):
            self._matrix[x][y] = 20 + r(1, 4)
    def erase(self, x, y):
        # a long long condition to not draw over the boat or treasure and delete the walls
        if self._testXY(x, y) and (self._startPoint != 0 and (self._startPoint[0] != x or self._startPoint[1] != y)) and (self._endPoint != 0 and (self._endPoint[0] != x or self._endPoint[1] != y)):
            self._matrix[x][y] = 10 + r(1, 4)
    def canStart(self):
        # this let the algotithm start iff you set the startingPoint and endingPoint
        if self._startPoint != 0 and self._endPoint != 0:
            return True
        else:
            return False
    def setStart(self, x, y):
        if self._startPoint != 0 and self._endPoint != 0 and (self._endPoint[0] == x and self._endPoint[1] == y):
            # this conditional statement is just for swap the boat with treasure
            self._startPoint, self._endPoint = self._endPoint, self._startPoint
            self._matrix[self._startPoint[0]][self._startPoint[1]] = 30
            self._matrix[self._endPoint[0]][self._endPoint[1]] = 40
        else:
            if self._startPoint != 0 and (self._startPoint[0] != x or self._startPoint[1] != y):
                # if you try to put the boat on the same position nothing will changes, only if is somewhere else
                self._matrix[self._startPoint[0]][self._startPoint[1]] = r(1, 2) * 10 + r(1, 4) # int the last position of the boat will appear magma or water
                self._startPoint = 0
            if self._matrix[x][y] // 10 == 1:
                # this won't let you to put the boat on magma
                self._matrix[x][y] = 30
                self._startPoint = (x, y)
        print(self._startPoint, self._endPoint)
    def setEnd(self, x, y):
        if self._endPoint != 0 and self._startPoint != 0 and (self._startPoint[0] == x and self._startPoint[1] == y):
            # this if is just for swap the treasure with the boat, it isn't necessary but it looks cool
            self._startPoint, self._endPoint = self._endPoint, self._startPoint
            self._matrix[self._startPoint[0]][self._startPoint[1]] = 30
            self._matrix[self._endPoint[0]][self._endPoint[1]] = 40
        else:
            # this is the most important part in setting the ending point
            if self._endPoint != 0 and (self._endPoint[0] != x or self._endPoint[1] != y):
                # if you trie to put the treasure on same place, it will let it unchanged
                self._matrix[self._endPoint[0]][self._endPoint[1]] = r(1, 2) * 10 + r(1, 4) # when you change the position of the treasure, in the last place will be magma or water
                self._endPoint = 0
            if self._matrix[x][y] // 10 == 1:
                # with this condition you can put the treasure only on water
                self._matrix[x][y] = 40
                self._endPoint = (x, y)
        print(self._startPoint, self._endPoint)
    def _testXY(self, x, y):
        # test if x and y are inside the map
        return x != 0 and x != self._nRows - 1 and y != 0 and y != self._nColumns - 1
    def startSolve(self):
        # create instance of class Solve, this is more for visualisation
        # if i made an method that solves Lee/DFS, then i saw only the beginning and the result of algorithm
        # using a functor, i can redraw the map after every step
        self._s = solver.Solve(self._nRows, self._nColumns, self._matrix, [11, 12, 13, 14], self._startPoint, self._endPoint)
    def continueSolve(self):
        if self._s.canWork():
            self._matrix = self._s.getMatrix()
            self.showMatrix()
            return True
        return False
    def makeItLikeBeforeLee(self):
        # different from  initializeMatrix because it keeps painted walls an erase path, distance and enqueued tiles
        self._startPoint = self._endPoint = 0
        for i in range(self._nRows):
            for j in range(self._nColumns):
                if self._matrix[i][j] < 10:
                    self._matrix[i][j] = 10 + r(1, 4)
        self.borderMatrix()
    def minPath(self):
        # v is queue used in solving returned as a vector, with the structure of a tuple with (actualPosition, parentPosition, discoveryTime)
        # parentPosition is used to find the path faster than in O(n^2)
        # discoveryTime is just for coloring
        distMatrix = [0] * self._nRows
        for i in range(self._nRows):
            distMatrix[i] = [-1] * self._nColumns
        if self._s.isThereAPath:
            self.makeItLikeBeforeLee()
            v = self._s.getVector()
            i = -1
            while v[i][1] != -1:
                self._matrix[v[i][0][0]][v[i][0][1]] = 0
                distMatrix[v[i][0][0]][v[i][0][1]] = v[i][2]
                i = v[i][1]
            self._matrix[v[-1][0][0]][v[-1][0][1]] = 40
            self._matrix[v[0][0][0]][v[0][0][1]] = 30
            self._s.setDistMatrix(distMatrix)
        else:
            print("There is no path from ship to the treasure")
    def saveMatrix(self):
        # just saving the matrix in secondary memory, also nothing fancy
        with open("map.txt", "w") as g:
            for i in range(self._nRows):
                for j in range(self._nColumns):
                    if self._matrix[i][j] < 10:
                        g.write(f"{10 + r(1, 4)} ")
                    else:
                        g.write(f"{self._matrix[i][j]} ")
                g.write("\n")
            print("Matricea a fost salvata")
    def getMatrixFromFile(self):
        # just reading the matrix from map.txt then show it, nothing fancy
        self.initializeMatrix()
        self._startPoint = self._endPoint = 0
        try:
            f = open("map.txt", "r")
            for i in range(self._nRows):
                self._matrix[i] = list(map(int, f.readline().split()))
                for j in range(len(self._matrix[i])):
                    if self._matrix[i][j] == 30:  # the ship
                        self._startPoint = (i, j)
                    elif self._matrix[i][j] == 40:  # the treasure
                        self._endPoint = (i, j)
            print(self._startPoint, self._endPoint)
            self.showMatrix()
            f.close()
        except:
            print("File not found!")
    def getColor(self, n): # Calculate the color for visual distance
        r = 255
        g = 255 - 2 * n
        b = 0
        if g < 0:
            g = 0
            b = (-g) % 256
        return (r, g, b)