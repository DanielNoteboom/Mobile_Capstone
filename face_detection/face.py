import numpy as np
import cv2
import sys
import math
import Queue

# controls the number of matches that the code returns
NUM_MATCHES = 3

def find_distance(x1,y1,x2,y2):
  return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

if len(sys.argv) != 4:
  print "Usage: python face.py PICTURE X-COORD Y-COORD"
  sys.exit(0)
picture = sys.argv[1]
# coordinates of the image here are from the upper left, with 
x_coord = int(sys.argv[2])
y_coord = int(sys.argv[3])
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

img = cv2.imread(picture)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)
faces = face_cascade.detectMultiScale(gray, 1.1, 0)

#Create priority queue with no max size
best_matches = Queue.PriorityQueue(0)

#find best_matches
for (x,y,w,h) in faces:
  #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

  # compare to center of rectangle
  distance = find_distance(x_coord,y_coord,x+w/2.0,y+h/2.0)
  # insert tuple into queue -- the distance is used for ordering,
  #   since tuples are compared lexicographically
  best_matches.put((distance, (x,y,w,h)))


# get a list of matches out of the queue
matches = []
for i in range(NUM_MATCHES):
  try:
    match = best_matches.get_nowait()
    matches.append(match)
  except Queue.Empty:
    break

#  output the name(s) of the cropped images, and their distances, to a
#   a file. The first line of file indicates number of matches. This 
#   should normally be NUM_MATCHES, but could possibly be less if
#   there are fewer found. 
#  Format of each line:  <match_image_filename> <distance_of_match>

outfile = open("face_detect_info.txt","w")


outfile.write(str(len(matches)) + "\n")
for i in range(len(matches)):
  dist = matches[i][0]
  x,y,w,h = matches[i][1]
  crop_img = img[y:(y+h),x:(x+w)]
  cv2.imwrite("crop%d.jpg"%i, crop_img)
  outfile.write( "crop%d.jpg %s\n" % (i, str(dist)) )

    
if len(matches) == 0:
  print "no matches found"
