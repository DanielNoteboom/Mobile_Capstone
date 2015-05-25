import sys
from PIL import Image

from face import facial_detection

if len(sys.argv) > 1:
  img = sys.argv[1]
else:
  img = 'img1.jpg'

if len(sys.argv) > 2:
  scale_factor = float(sys.argv[2])
else:
  scale_factor = 1.2

if len(sys.argv) > 3:
  min_neighbors = int(sys.argv[3])
else:
  min_neighbors = 4

#   run facial detetction on arguments passed in

facial_detection(img, 0,0,True, scale_factor, min_neighbors)

#  we save the images with rectangles to 'boxes.jpg' in face.py
  
image = Image.open('boxes.jpg')
image.show()





