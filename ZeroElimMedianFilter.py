import numpy as np


def ZeroElimMedianFilter(img):
    rows = img.shape[0]
    cols = img.shape[1]

    adjmap = np.zeros_like(img)
    # Needs hhf_pad
    # And is itself a dependency for zeroElimMedianHoleFill