# MAXLINEDEV - Finds max deviation from a line in an edge contour.
#
# Function finds the point of maximum deviation from a line joining the
# endpoints of an edge contour.
#
# Usage: maxlinedev(x, y)
# 
#
# Arguments:
#          x, y   - arrays of x,y  (row, col) indicies of connected pixels 
#                   on the contour.
# Returns:
#          maxdev = Maximum deviation of contour point from the line
#                     joining the end points of the contour (pixels).
#

# Pseudo-code. Not tested to work.
# Issues: function takes in one value for each argument, yet MATLAB code has it so that it will be run from array index 0 to length - 1.
# num_pts is one instance, where it uses the length of x, as if for all x.

def maxlinedev(x, y):
  num_pts = size of array
  
  if(num_pts == 1 || num_pts == 0) {
    print 'error: contour of length 0 or 1.'
    maxdev = 0
    dist_contour = 1
  }
  
  endpt_dist = sqrt((x[0] - x[num_pts - 1])^2 + (y[0] - y[num_pts - 1]^2)
  
  if(endpt_dist > epsilon) {
    	# Eqn of line joining end pts (x1 y1) and (x2 y2) can be parameterised by
    	#    
    	#    x*(y1-y2) + y*(x2-x1) + y2*x1 - y1*x2 = 0
    	#
    	# (See Jain, Rangachar and Schunck, "Machine Vision", McGraw-Hill
    	# 1996. pp 194-196)
    # Compute the parameters
    y1my2 = y[0] - y[num_pts - 1]
    x2mx1 = x[num_pts - 1] - x[0]
    C = y[num_pts - 1] * x[0] - y[0] * x[num_pts - 1]
    
    dist_contour = abs(x * y1my2 + y * m2mx1 + C) / endpt_dist
  }
  else {
    # End points are coincident, so calculate distances from first point.
    dist_contour = sqrt((x - x[0])^2 + (y-y[0])^2)
  }
  
  # Set endpt_dist to 1 so that normalized error can be used.
  endpt_dist = 1
  
  maxdev = dist_contour
  # Return the distance from line segment for each contour point.
  return maxdev
