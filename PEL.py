

import numpy as np
import Queue

import time, random

UP_LEFT =    1
UP =         2
UP_RIGHT =   3
RIGHT =      4
DOWN_RIGHT = 5
DOWN =       6
DOWN_LEFT =  7
LEFT =       8

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
        if(self._noItems < self.qsize):
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
        compare = np.zeros((2,), dtype = np.int)

        # Sides to check for each diagonal.
        if analysisDir == UP_LEFT:
            checkDir = {UP, LEFT}
        elif analysisDir == UP_RIGHT:
            checkDir = {UP, RIGHT}
        elif analysisDir == DOWN_RIGHT:
            checkDir = {DOWN, RIGHT}
        else:
            checkDir = {DOWN, LEFT}

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
        global nextDir
        # Check the sets to determine the type of direction.
        cardinalDir = frozenset([LEFT, RIGHT, UP, DOWN])
        diagonalDir = frozenset([UP_LEFT, UP_RIGHT, DOWN_RIGHT, DOWN_LEFT])

        if analysisDir in cardinalDir:
            nextDir = self.getCardinalDir(analysisDir)
        elif analysisDir in diagonalDir:
            nextDir = self.getDiagonalDir(analysisDir)

        return nextDir

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
            if row <= 0 or row >= height - 1:
                return count
            if col <= 0 or col >= width:
                return count

            rows = edgeImg.shape[0]
            cols = edgeImg.shape[1]
            count += 1

            # Add the current direction to the queue.
            Q.add(dir)

            if dir == UP_LEFT:
                nextDir = Q.computeNextDir(UP_LEFT)

                # Up-Left?
                if edgeImg[(row - UR[0]) * width + (col + UR[1])]:
                    if nextDir == UP:
                        # Up?
                        if edgeImg[(row - U[0]) * width + (col + U[1])]:
                            pixels[count].row = row - 1
                        #







# Algorithm:
#
# ==== Step 2: EdgeSegment Creation with 8-Directional Walk ====
# Define 8 movement directions.
#
# Next direction prediction engine.
# Create Queue with size 8 to push in last 8 directions and it
# makes a prediction for the next direction.
#
# Queue has functions Add and ComputeNextDir.
#
# Queue starts with noItems and rear set to zero.
# 'noItems' counts the number of items. We can use this to iterate
# through the Queue.
# 'rear' is for adding a direction to the Queue. Keep this pushing
# new elements to the Queue by resetting it to zero when it gets
# greater than the QSIZE.
#
# ------- Functions --------
# Add(int dir)
# Adds direction to the queue
# if rear becomes larger than QSIZE, reset rear = 0
# if noItems is less than QSIZE, noItems++
# --- end-Add ---
#
# ComputeNextDir(int analysisDir)
# Allow computer to pick the direction point.
# Hold the computed path in an array size 2. This will determine
# the direction to take.
# 1. If the direction is LEFT or RIGHT,
#    - Go through the Queue, 0 to i < noItems
#    - If the Queue has directions that are neither, continue looping.
#    - Add to LEFT (0) or RIGHT (1) every time one of those occurs in the Queue.
#    - Whichever position has a higher score, return that direction.
# 2. Else if direction is UP or DOWN,
#    - Go through the Queue, 0 to i < noItems
#    - If dir is LEFT or RIGHT, continue looping.
#    - Add c[0] whenever UP, UP_LEFT, or UP_RIGHT occur.
#    - Else add c[1], hence one of the DOWN directions.
#    - Whichever position has a higher score, return that direction.
#      (This should probably be made into it's own function since each move uses it.)
# We have specific cases for when direction is diagonal.
# 3. Else if direction is UP_LEFT,
#    - Go through the Queue, 0 to i < noItems
#    - If Q has UP, c[0]++, else if Q has LEFT, c[1]++.
#    - Determine which one to return, c[0] >= c[1], return UP. Else return LEFT.
# 4. Direction is UP_RIGHT,
#    - Go through the Queue, 0 to i < noItems
#    - If Q has UP, c[0]++, else if Q has RIGHT, c[1]++.
#    - Determine which one to return, c[0] >= c[1], return UP. Else return RIGHT.
# 5. Direction is DOWN_RIGHT,
#    - Go through the Queue, 0 to i < noItems
#    - If Q has DOWN, c[0]++, else if Q has RIGHT, c[1]++.
#    - Determine which one to return, c[0] >= c[1], return DOWN. Else return RIGHT.
# 4. Else direction is DOWN_LEFT,
#    - Go through the Queue, 0 to i < noItems
#    - If Q has DOWN, c[0]++, else if Q has LEFT, c[1]++.
#    - Determine which one to return, c[0] >= c[1], return DOWN. Else return LEFT.
# These diagonals could also be made into a separate function, with args
# for diagonal, and absolute one and absolute two (eg. UP_RIGHT, UP, RIGHT, noItems, C).
# --- end-ComputeNextDir ---
#
# ------ 8 Directional Walk with Prediction ------
# This is used by PELWalk8Dirs.
#
# Walk8Dirs(edgeImg, width, height, int rows, int cols, int dir, Pixels)
#
# Define Queue as Q.
# count = 0. Counts the number of pixels in forming an edge segment.
# edgeImg[r* width + c] = 0. Not sure what this does, but it's used later on.
#
# Base cases. If rows or columns are out of bounds.
# if r <= 0 or r >= height - 1; return count
# if c <= 0 or c >= width - 1; return count
#
# pixels[count].r = r
# pixels[count].c = c
# count++
#
# Add the current direction to Queue.
# Q.Add(dir)
#
#

