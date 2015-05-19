import numpy as np
import cv2
import sys
import math
import os
import Queue

NUM_MATCHES = 3

'''returns the top matches of potential faces
params:
  picture-picture file(jpg, png, and other cv2 formats)
  x_coord-x coordinate of where we are looking for faces
  y_coord-y coordinate of where we are looking for faces
'''
def get_top_matches(picture, x_coord, y_coord, display_rect = False,
                    scale_factor=1.1,min_neighbors=2):
  # controls the number of matches that the code returns
  
  def find_distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
  
  # coordinates of the image here are from the upper left, with 
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
  
  img = cv2.imread(picture)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  gray = cv2.equalizeHist(gray)
  faces = face_cascade.detectMultiScale(gray, scale_factor, min_neighbors)
  
  #Create priority queue with no max size
  best_matches = Queue.PriorityQueue(0)
  
  #find best_matches
  for (x,y,w,h) in faces:
    if display_rect:
      cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
  
    # compare to center of rectangle
    distance = find_distance(x_coord,y_coord,x+w/2.0,y+h/2.0)
    # insert tuple into queue -- the distance is used for ordering,
    #   since tuples are compared lexicographically
    best_matches.put((distance, (x,y,w,h)))
  if display_rect:
    cv2.imwrite("boxes.jpg", img) 
  matches = queue_to_list(best_matches, NUM_MATCHES)
  
  result = []
  write_matches(matches, result, img, cv2)
  return result
  
      
## changes priority queue to a list
def queue_to_list(q, list_size):
  # get a list of matches out of the queue
  matches = []
  for i in range(NUM_MATCHES):
    try:
      match = q.get_nowait()
      matches.append(match)
    except Queue.Empty:
      break
  return matches


# Takes a list of matches, saves image files for them,
#  appends the image file name and the associated distance
#  to a result list
def write_matches(matches, result_list, img, cv2):
  for i in range(len(matches)):
    dist = matches[i][0]
    x,y,w,h = matches[i][1]
    crop_img = img[y:(y+h),x:(x+w)]
    cv2.imwrite("crop%d.jpg"%i, crop_img)
    # Distance might taken into account later
    # Faces are returned as a dictionary
    result_list.append({'path':os.path.abspath("crop%d.jpg"%i),
                        'distance':dist})
  if len(matches) == 0:
    print "no matches found"




