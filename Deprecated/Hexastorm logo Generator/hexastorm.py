# Company: Hexastorm
# Author: Henri Starmans
# Date: 17-3-2017

from stl_tools import numpy2stl
from scipy.ndimage import gaussian_filter
from pylab import imread

img = 256 * imread("freecadlogo.png")
img = img[:,:,0]+1.*img[:,:,3]
img = gaussian_filter(img,2)
numpy2stl(img,'hexastorm.stl', scale=0.2, mask_val=5, solid=True)

