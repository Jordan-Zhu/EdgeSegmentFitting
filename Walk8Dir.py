# ------------------------------------------------------------------------------
# Name:        Walk8Dir
# Purpose:     Create edge segments by predicting the next edge, using the last
#              8 directions to make a prediction for the next.
# ------------------------------------------------------------------------------

import Queue
import numpy as np


UP_LEFT = 1
UP = 2
UP_RIGHT = 3
RIGHT = 4
DOWN_RIGHT = 5
DOWN = 6
DOWN_LEFT = 7
LEFT = 8


class IterableQueue:
    def __init__(self, source_queue):
        # This instance's source_queue is the one passed in.
        self.source_queue = source_queue

    def add(self, val):
        # Pop one element off the queue to free space.
        if self.source_queue.full():
            self.source_queue.get_nowait()

        # Add a value to the queue.
        self.source_queue.put(val)

    # This iterator wraps the queue and yields until the queue
    # is empty, then returns.
    def __iter__(self):
        while True:
            try:
                yield self.source_queue.get_nowait()
            except Queue.Empty:
                return

    @staticmethod
    def get_cardinal_dir(analysis_dir):
        count = np.zeros((2,), dtype=np.int)

        # We want to find the side that is most likely to be an edge.
        # So these lists contain each direction of one the sides since
        # we only need one complete side and the other direction
        # will be everything else.
        if analysis_dir == LEFT or analysis_dir == RIGHT:
            check_dir = [UP, DOWN, LEFT, DOWN_LEFT, UP_LEFT, RIGHT]
        elif analysis_dir == UP or analysis_dir == DOWN:
            check_dir = [LEFT, RIGHT, UP, UP_LEFT, UP_RIGHT, DOWN]

        # Determine the most likely next direction.
        for e in IterableQueue(q):
            # Skip if it's UP or DOWN / LEFT or RIGHT.
            if e == check_dir[0] or e == check_dir[1]:
                continue

            if e == check_dir[2] or e == check_dir[3] or e == check_dir[4]:
                count[0] += 1
            else:
                count[1] += 1

        # Return the direction with higher count.
        if count[0] >= count[1]:
            return check_dir[2]
        else:
            return check_dir[5]

    @staticmethod
    def get_diagonal_dir(analysis_dir):
        count = np.zeros((2,), dtype=np.int)

        # Sides to check for each diagonal.
        if analysis_dir == UP_LEFT:
            check_dir = [UP, LEFT]
        elif analysis_dir == UP_RIGHT:
            check_dir = [UP, RIGHT]
        elif analysis_dir == DOWN_RIGHT:
            check_dir = [DOWN, RIGHT]
        else:
            check_dir = [DOWN, LEFT]

        # Compare to find the strongest side.
        for e in IterableQueue(q):
            if e == check_dir[0]:
                count[0] += 1
            elif e == check_dir[1]:
                count[1] += 1

        # Return the one with higher count.
        if count[0] >= count[1]:
            return check_dir[0]
        else:
            return check_dir[1]

    def compute_next_dir(self, analysis_dir):
        # Value to be returned.
        comp_dir = 0

        cardinal_dir = frozenset([LEFT, RIGHT, UP, DOWN])
        diagonal_dir = frozenset([UP_LEFT, UP_RIGHT, DOWN_RIGHT, DOWN_LEFT])

        if analysis_dir in cardinal_dir:
            comp_dir = self.get_cardinal_dir(analysis_dir)
        elif analysis_dir in diagonal_dir:
            comp_dir = self.get_diagonal_dir(analysis_dir)

        return comp_dir


if __name__ == "__main__":
    q = Queue.Queue(8)
    IterableQueue(q).add(1)
    # q.put(1)
    q.put(2)
    q.put(3)
    q.put('hi')
    q.put(5)
    q.put(6)
    q.put(7)
    q.put(8)
    print '=============='
    if q.full():
        print 'Queue full, getting first element', q.get()
    q.put(6)
    # print q
    print 'Get', q.get()

    for n in IterableQueue(q):
        print(n)

    # Walking pixel downstairs, ask the prediction engine left or right.
    # Test case i.e., down, down-left, down-left, down, down, down, down

