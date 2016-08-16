
import numpy as np
import scipy.io as sio

# from merge_lines import merge_lines
from merge_lines_v2 import merge_lines
from sioloadmat import loadmat

if __name__ == '__main__':
    line_in = loadmat('linefeature.mat')
    listpt = loadmat('listpointc.mat')
    print 'Line feature shape', line_in.shape, 'list point shape ', listpt.shape
    # print 'List point: ', listpt

    # Possible fix for out of bounds error: instead of deleting lines, fill them with an
    # empty array as a placeholder.
    # merge_lines(line_in, listpt, thresh=10, imgsize=[640, 480])

    merge_lines(line_in, listpt, thresh=10, imgsize=[640, 480])
