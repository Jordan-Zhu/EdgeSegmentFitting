import scipy.io as sio
import numpy as np

def loadmat(mat):
    data = sio.loadmat(mat)
    listings = list(data)

    # Outputs array of arrays if matrix is a cell array.
    # Otherwise it will output a usual array.
    if listings[0] == '__version__':
        mat = data[listings[1]]
    else:
        mat = np.asarray(data[listings[0]], dtype=np.float)

    return mat

if __name__ == '__main__':
    data = sio.loadmat('Unit_Tests/listpointc.mat')

    print loadmat('Unit_Tests/listpointc.mat').shape
