from facepp import API
from facepp import File
import os
import sys
import math
import Queue
import cv2
API_KEY = 'e700b63583b24090f4827a851469eaea'
API_SECRET = 'DcksQWqJfvukmXEhQFMbjgcRPltZKiyo'
SERVER = 'http://api.us.faceplusplus.com/'
api = API(API_KEY,API_SECRET,srv=SERVER)
NUM_MATCHES=3

'''returns the top matches of potential faces
params:
  picture-picture file
  x_coord-x coordinate of where we are looking for faces 
  y_coord-y coordinate of where we are looking for faces
 each result returned is a dictionary.'''
def facial_detection(img, x_coord, y_coord):
  face= api.detection.detect(img = File(img))

  def find_distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

  best_matches = Queue.PriorityQueue(0)

  for person in face['face']:
    distance = find_distance(x_coord,y_coord,float(person['position']['center']['x']), float(person['position']['center']['y']))
    best_matches.put((distance, person))
  matches = queue_to_list(best_matches, NUM_MATCHES)
  result=[]
  write_matches(matches, result, cv2.imread(img))
  return result



# Takes a list of matches, saves image files for them,
#  appends the image file name and the associated distance
#  to a result list
def write_matches(matches, result_list, img):
  for i in range(len(matches)):
    dist = matches[i][0]
    face = matches[i][1]
    height, width, depth = img.shape
    x_center = face['position']['center']['x'] * width * .01
    y_center = face['position']['center']['y'] * height * .01
    crop_width = width * face['position']['width'] * .01
    crop_height = height * face['position']['height'] * .01
    x = int(x_center - (crop_width / 2))
    y = int(y_center - (crop_height / 2))

    expansion = 0.6
    expand_w = crop_width*expansion
    expand_h = crop_height*expansion

    x1 = max(0, x - expand_w)
    x2 = min(width, x + crop_width + expand_w)
    y1 = max(0, y - expand_h)
    y2 = min(height, y + crop_height + expand_h)

    crop_img = img[y1:y2,x1:x2]
    cv2.imwrite("original%d.jpg"%i, img)
    cv2.imwrite("crop%d.jpg"%i, crop_img)
    result_list.append({'path':os.path.abspath("crop%d.jpg"%i), 'distance':dist, 'face':face, 'original_path':os.path.abspath("original%d.jpg"%i)})


##changes priority queue to a list with specified amount of matches
def queue_to_list(q, list_size):
  # get a list of matches out of the queue
  matches = []
  for i in range(list_size):
    try:
      match = q.get_nowait()
      matches.append(match)
    except Queue.Empty:
      break
  return matches
        


'''compare face to a class_name and return the facepp api results
params:
  face-face to compare to 
  class_name-class to compare face to
return:
  {top 3 matches as a dictionary with keys match_path, id, and score)'''
def compare(face, class_name):
  #follows the convention that class_name==group==directory with pictures
  #returns the comparison results for given face and classname
  result = api.recognition.identify(group_name=class_name, img=File(face['path']))
  print "compare result"
  print result
  return_list = []
  if len(result['face']) == 0:
    return []
  for i in range(len(result['face'][0]['candidate'])):
    name = result['face'][0]['candidate'][i]['person_name']
    score = result['face'][0]['candidate'][i]['confidence']

    return_list.append({'match_path': os.path.abspath("../face_comparison/" + 
      class_name + "/" + name + "/1.jpg"), 'id': name, 'score': score})
  return return_list
      
'''Adds face to facepp api
params:
  img: image of new face
  name: name of person to add face to'''
def add_face(img, name):
  face = api.detection.detect(img = File(img))
  face_id = face['face'][0]['face_id']
  api.person.add_face(person_name=name, face_id=face_id)

   
