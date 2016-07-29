
import numpy as np
import scipy.io as sio

from merge_lines import merge_lines
from sioloadmat import loadmat

if __name__ == '__main__':
    line_in = loadmat('linefeature.mat')
    listpt = loadmat('listpointc.mat')
    print line_in.shape

    merge_lines(line_in, listpt, thresh=10, imgsize=640*480)
    print 'done'