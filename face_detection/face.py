import numpy as np
import cv2
import sys
import math
def find_distance(x1,y1,x2,y2):
  return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

if len(sys.argv) != 4:
  print "Usage: python face.py PICTURE X-COORD Y-COORD"
  sys.exit(0)
picture = sys.argv[1]
x_coord = int(sys.argv[2])
y_coord = int(sys.argv[3])
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

img = cv2.imread(picture)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)
faces = face_cascade.detectMultiScale(gray, 1.1, 0)
print faces
#assume for now the rectangles don't overlap
closest_distance = -1
closest = (-1,-1,-1,-1)
for (x,y,w,h) in faces:
  print x
  print y
  print w
  print h
  distance = find_distance(x_coord,y_coord,x,y)
  if distance < closest_distance or closest_distance == -1:
    closest_distance = distance
    closest = (x,y,w,h)
    
x,y,w,h = closest
print img.shape
print img.ndim
print img
crop_img = img[y:(y+h),x:(x+w)]
print type(crop_img)
print type(img)
cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
roi_gray = gray[y:y+h, x:x+w]
roi_color = img[y:y+h, x:x+w]
cv2.imwrite("saved.jpg", crop_img)

cv2.imshow('img',img)
cv2.waitKey(0)
c2.destroyAllWindows()

