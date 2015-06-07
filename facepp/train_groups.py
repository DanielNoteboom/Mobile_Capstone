from facepp import API
from facepp import File
import os
import sys
API_KEY = 'e700b63583b24090f4827a851469eaea'
API_SECRET = 'DcksQWqJfvukmXEhQFMbjgcRPltZKiyo'
SERVER = 'http://api.us.faceplusplus.com/'
LOCAL_DIRECTORY='../face_comparison'
api = API(API_KEY,API_SECRET,srv=SERVER)

'''Adds the class to the dataset
params:
  group: group name to add to api
  classdir: directory that contains class pictures
Convention: group==classdir'''
def update_group(group, classdir):
  print "entering update_group"
  if group != classdir:
    print "ERROR: group should equal classdir"
    sys.exit(1)
  if contains_group(group):
    print "group already created"
  else:
    global LOCAL_DIRECTORY
    directory = LOCAL_DIRECTORY + '/' + classdir
    api.group.create(group_name=group)
    for person in os.listdir(directory):

      if contains_person(person):
        print "person already in dataset"
      elif person[0] != '.':
        print "adding new person " + person
        api.person.create(person_name=person)
        sub_dir = directory + '/' + person
        for pic in os.listdir(sub_dir):
          pic = sub_dir + '/' + pic
          print "picture"
          print pic
          if pic[-3:] == "jpg":
            face = api.detection.detect(img = File(pic))
            if len(face['face']) > 0:
              face_id = face['face'][0]['face_id']
              api.person.add_face(person_name=person, face_id=face_id)
              print "found face in " + pic
            else:
              print "couldn't find face in " + pic
        api.group.add_person(group_name=group,person_name=person)
        '''else:
        print "adding existing person"'''
   
      
    api.train.identify(group_name=group)
    print "trained group " + group

'''Find whether person is already added to the dataset
params:
  person-person checking to see whether it's arlready added'''
def contains_person(person_name):
  people = api.info.get_person_list()
  for person in people['person']:
    if person['person_name'] == person_name:
      return True
  return False;

'''Delete group from dataset
params:
  group-group to delete from the dataset'''
def delete(group):
  directory = LOCAL_DIRECTORY + '/' + group
  for person in os.listdir(directory):
    api.person.delete(person_name=person)
    print "deleted person " + person
  api.group.delete(group_name=group)
  print group + " deleted"

'''Get comparison results for an image of a person compared to the group
params:
  group-group to look for recognition in
  url-Image of person to compare to group'''
def compare(group, url):
  result = api.recognition.identify(group_name=group, img=File(url))
  print result
  print 'The person with highest confidence:', \
          result['face'][0]['candidate'][0]['person_name']


'''Find whether group name is already added to dataset
params:
  group_name-group to check if it's already added'''
def contains_group(group_name):
  groups = api.info.get_group_list()
  for group in groups['group']:
    if group_name == group['group_name']:
      return True
  return False

'''List all the groups in the api'''
def list_groups():
  groups = api.info.get_group_list()
  print "Group List:"
  for group in groups['group']:
    print group['group_name']

'''Helper method to print usage'''
def usage():
  print "\nUSAGE python train_groups.py CREATE_CLASS|DELETE_CLASS|TRAIN|COMPARE|GET_CLASSES}\n"
  print "CREATE_CLASS {class_name(directory name relative to face_comparison)}"
  print "DELETE_CLASS {class_name}"
  print "COMPARE {class_name} {picture}"
  print "GET_CLASSES"

'''Check whether the arguments are correct'''
def checkArgs():
  first_arg=sys.argv[1]

  if first_arg == 'CREATE_CLASS':
    if len(sys.argv) < 3:
      print "USAGE python train_groups.py CREATE_CLASS {class_name}" 
    class_dir = sys.argv[2]
    #follow the convention of naming the group what the directory is named 
    group_name = class_dir
    update_group(group_name, class_dir)
  elif first_arg=="COMPARE":
    if len(sys.argv) < 4:
      print "USAGE python train_groups.py COMPARE {group_name} {picture}"
    group_name = sys.argv[2]
    picture = sys.argv[3]
    compare(group_name, picture)
  elif first_arg=="DELETE_CLASS":
    if len(sys.argv) < 3:
      print "USAGE python train_groups.py DELETE_CLASS {group_name}"
    group_name = sys.argv[2]
    delete(group_name)
  elif first_arg=="GET_GROUPS":
    list_groups()

  else:
    usage()
    


if __name__ == '__main__':
  if len(sys.argv) < 2 or len(sys.argv) > 4:
    usage()
    sys.exit(0)
  checkArgs()

