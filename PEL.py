

import numpy as np
import Queue

import time, random

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