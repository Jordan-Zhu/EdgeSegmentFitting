

import numpy as np
import Queue

import time, random

UP_LEFT = 1
UP = 2
UP_RIGHT = 3
RIGHT = 4
DOWN_RIGHT = 5
DOWN = 6
DOWN_LEFT = 7
LEFT = 8

global checkDir
global compDir


class MyQueue:
    # QSIZE = 8
    # q = Queue.Queue(QSIZE)
    noItems = 0
    rear = 0

    def __init__(self):
        self.qsize = 8
        self.items = [None] * self.qsize
        self._noItems = 0
        self._rear = 0
        # self.__queue = queue

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def add(self, dir):
        self._rear += 1
        self.items.insert(self._rear, dir)
        if (self._rear >= self.qsize):
            self._rear = 0
        if self._noItems < self.qsize:
            self._noItems += 1

    def getCardinalDir(self, analysisDir):
        global checkDir
        compare = np.zeros((2,), dtype = np.int)

        # We want to find the side that is most likely to be an edge.
        # So these lists contain each direction of one the sides and
        # we only need one complete side since the other direction
        # will be anything else.
        if(analysisDir == LEFT or analysisDir == RIGHT):
            checkDir = {UP, DOWN, LEFT, DOWN_LEFT, UP_LEFT, RIGHT}
        elif analysisDir == UP or analysisDir == DOWN:
            checkDir = {LEFT, RIGHT, UP, UP_LEFT, UP_RIGHT, DOWN}

        # Determine the strongest direction.
        for i in xrange(0, self._noItems):
            if self.items[i] == checkDir[0] or self.items[i] == checkDir[1]:
                continue

            if(self.items[i] == checkDir[2] or self.items[i] == checkDir[3] or self.items[i] == checkDir[4]):
                compare[0] += 1
            else:
                compare[1] += 1

        if compare[0] >= compare[1]:
            return checkDir[2]
        else:
            return checkDir[5]

    def getDiagonalDir(self, analysisDir):
        global checkDir
        compare = np.zeros((2,), dtype=np.int)

        # Sides to check for each diagonal.
        if analysisDir == UP_LEFT:
            checkDir = [UP, LEFT]
        elif analysisDir == UP_RIGHT:
            checkDir = [UP, RIGHT]
        elif analysisDir == DOWN_RIGHT:
            checkDir = [DOWN, RIGHT]
        else:
            checkDir = [DOWN, LEFT]

        # Compare to find the strongest side.
        for i in xrange(0, self._noItems):
            if self.items[i] == checkDir[0]:
                compare[0] += 1
            elif self.items[i] == checkDir[1]:
                compare[1] += 1

        # Return the one that is most likely
        # to be the next direction.
        if compare[0] >= compare[1]:
            return checkDir[0]
        else:
            return checkDir[1]

    def computeNextDir(self, analysisDir):
        global compDir
        # Check the sets to determine the type of direction.
        cardinalDir = frozenset([LEFT, RIGHT, UP, DOWN])
        diagonalDir = frozenset([UP_LEFT, UP_RIGHT, DOWN_RIGHT, DOWN_LEFT])

        if analysisDir in cardinalDir:
            compDir = self.getCardinalDir(analysisDir)
        elif analysisDir in diagonalDir:
            compDir = self.getDiagonalDir(analysisDir)

        return compDir


class CreateEdgeSeg:
    # initialization
    def __init__(self, width, height):
        self.width = width
        self.height = height


    def Walk8Dirs(self, edgeImg, width, height, row, col, dir):
        Q = MyQueue()
        count = 0
        pixels = np.full((edgeImg.shape[0], edgeImg.shape[1], 3), 255, np.int)

        # Directions done by row, column.
        U =  [-1, 0]
        D =  [1, 0]
        L =  [0, -1]
        R =  [0, 1]
        UR = [-1, 1]
        UL = [-1, -1]
        DR = [1, 1]
        DL = [1, -1]


        while 1:
            # Check bounds.
            if row <= 0 or row >= height - 1:
                return count
            if col <= 0 or col >= width:
                return count

            pixels[count].r = row
            pixels[count].c = col
            # row = edgeImg.shape[0]
            # col = edgeImg.shape[1]
            count += 1

            # Add the current direction to the queue.
            Q.add(dir)

            if dir == UP_LEFT:
                nextDir = Q.computeNextDir(UP_LEFT)

                # Up-Left?
                if edgeImg[(row + UR[0]) * width + (col + UR[1])]:
                    if nextDir == UP:
                        # Up?
                        if edgeImg[(row + U[0]) * width + (col + U[1])]:
                            pixels[count].r = row + U[0]
                            pixels[count].c = col + U[1]
                            count += 1
                            edgeImg[(row - UR[0]) * width + col] = 0
                        # Left?
                        elif edgeImg[(row + L[0]) * width + col + L[1]]:
                            pixels[count].r = row + L[0]
                            pixels[count].c = col + L[1]
                            count += 1
                            edgeImg[row * width + col + L[1]] = 0
                    else:
                        # Left?
                        if edgeImg[(row + L[0]) * width + col + L[1]]:
                            pixels[count].r = row + L[0]
                            pixels[count].c = col + L[1]
                            count += 1
                            edgeImg[row * width + col + L[1]] = 0

                        # Up?
                        elif edgeImg[(row + U[0]) * width + col]:
                            pixels[count].r = row + U[0]
                            pixels[count].c = col + U[1]
                            count += 1
                            edgeImg[(row + U[0]) * width + col] = 0

                    row += UL[0]
                    col += UL[1]
                    dir = UP_LEFT
                    continue

                if nextDir == UP:
                    # Up
                    if edgeImg[(row + U[0]) * width + (col + U[1])]:
                        row -= 1
                        dir = UP
                        continue

                    # Left
                    if edgeImg[(row + L[0]) * width + (col + L[1])]:
                        col -= 1
                        dir = LEFT
                        continue

                    # Up-Right
                    if edgeImg[(row + UR[0]) * width + (col + UR[1])]:
                        row -= 1
                        col += 1
                        dir = UP_RIGHT
                        continue

                    # Down-Left
                    if edgeImg[(row + DL[0]) * width + (col + DL[1])]:
                        row += 1
                        col -= 1
                        dir = DOWN_LEFT
                        continue

                    # Right
                    if edgeImg[(row + R[0]) * width + (col + R[1])]:
                        col += 1
                        dir = RIGHT
                        continue

                    # Down
                    if edgeImg[(row + D[0]) * width + (col + D[1])]:
                        row += 1
                        dir = DOWN
                        continue
                else:
                    # Left
                    if edgeImg[(row + L[0]) * width + (col + L[1])]:
                        col -= 1
                        dir = LEFT
                        continue

                    # Up
                    if edgeImg[(row + U[0]) * width + (col + U[1])]:
                        row -= 1
                        dir = UP
                        continue

                    # Down-Left
                    if edgeImg[(row + DL[0]) * width + (col + DL[1])]:
                        row += 1
                        col -= 1
                        dir = DOWN_LEFT
                        continue

                    # Up-Right
                    if edgeImg[(row + UR[0]) * width + (col + UR[1])]:
                        row -= 1
                        col += 1
                        dir = UP_RIGHT
                        continue

                    # Down
                    if edgeImg[(row + D[0]) * width + (col + D[1])]:
                        row += 1
                        dir = DOWN
                        continue

                    # Right
                    if edgeImg[(row + R[0]) * width + (col + R[1])]:
                        col += 1
                        dir = RIGHT
                        continue

                # Nowhere to go
                return count


            elif dir == UP:
                # Up
                if edgeImg[(row + U[0]) * width + col]:
                    row -= 1
                    dir = UP
                    continue

                # Should we check LEFT or RIGHT first?
                nextDir = Q.computeNextDir(LEFT)

                if nextDir == LEFT:
                    # Up-Left
                    if edgeImg[(row + UL[0]) * width + (col + UL[1])]:
                        if edgeImg[row * width + (col + UL[1])]:
                            edgeImg[row * width + (col + UL[1])] = 0
                            pixels[count].r = row
                            pixels[count].c = col + UL[1]
                            count += 1

                    # Up-Right
                    if edgeImg[(row + UR[0]) * width + (col + UR[1])]:
                        if edgeImg[row * width + (col + UR[1])]:
                            edgeImg[row * width + (col + UR[1])] = 0
                            pixels[count].r = row
                            pixels[count].c = col + UR[1]
                            count += 1


