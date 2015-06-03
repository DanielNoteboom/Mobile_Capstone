from facepp import API
from facepp import File
import os
import sys
API_KEY = 'e700b63583b24090f4827a851469eaea'
API_SECRET = 'DcksQWqJfvukmXEhQFMbjgcRPltZKiyo'
SERVER = 'http://api.us.faceplusplus.com/'
LOCAL_DIRECTORY='../Mobile_Capstones/face_comparison/c1'
api = API(API_KEY,API_SECRET,srv=SERVER)
def add_all_faces(group):
  global LOCAL_DIRECTORY
  api.group.create(group_name=group)
  for person in os.listdir(LOCAL_DIRECTORY):
    print person
    api.person.create(person_name=person)
    sub_dir = LOCAL_DIRECTORY + '/' + person
    for pic in os.listdir(sub_dir):
      pic = sub_dir + '/' + pic
      face = api.detection.detect(img = File(pic))
      if len(face['face']) > 0:
        face_id = face['face'][0]['face_id']
        api.person.add_face(person_name=person, face_id=face_id)
        print "found face in " + pic
      else:
        print "couldn't find face in " + pic
    api.group.add_person(group_name=group,person_name=person)

def add_group(group):
  api.group.create(group_name=group)
  for person in os.listdir(LOCAL_DIRECTORY):
    api.group.add_person(group_name=group,person_name=person)
  

def train(group):
  api.train.identify(group_name=group)

def compare(group, url):
  result = api.recognition.identify(group_name=group, img=File(url))
  print result
  print 'The person with highest confidence:', \
          result['face'][0]['candidate'][0]['person_name']

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print "USAGE python faces.py CREATE_NEW|CREATE_GROUP|TRAIN|{url of image with respect to c1}"
    sys.exit(0)
  arg=sys.argv[1]
  group_name='person'
  if arg == "CREATE_NEW":
    add_all_faces(group_name)
  elif arg == 'CREATE_GROUP':
    add_group(group_name)
  elif arg == "TRAIN":
    train(group_name)
  else:
    compare(group_name, arg)
