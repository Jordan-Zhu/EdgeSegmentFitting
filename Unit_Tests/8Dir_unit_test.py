
import Queue
import numpy as np
import Walk8Dir

if __name__ == '__main__':
    q = Queue.Queue(8)
    w = Walk8Dir.IterableQueue(q)
    # q = Queue.Queue(8)
    # w.IterableQueue(q)

    # down, down-left, down-left, down, down, down, down
    # dir = ['DOWN', 'DOWN_LEFT', 'DOWN_LEFT', 'DOWN', 'DOWN', 'DOWN', 'DOWN']
    dir = [6, 7, 7, 6, 6, 6, 6]
    for n in xrange(0, len(dir)):
        w.add(dir[n])

    # Walking down the the pixel downstairs is empty.
    # There are two alternatives: down-left or down-right.
    # Ask prediction engine guide left or right.
    print w.compute_next_dir(8)
    # assert w.compute_next_dir(8) == 7
