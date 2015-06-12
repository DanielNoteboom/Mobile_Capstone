import shutil
import os
import sys

# A potentially useful script to change the format of a folder
#   full of images.

# The target directory of this script should contain a
# number of photos of the form Firstname_Lastname__num.jpg

if len(sys.argv) < 2:
  print "Usage: python %s <target_dir>" % sys.argv[0]
  sys.exit(0)

target = sys.argv[1]
os.chdir(target)


for f in os.listdir('./'):
  name =  os.path.splitext(f)[0]
  # Skip hidden files
  if name[0] == '.' or name[0] == '_':
    continue

  if '__' in name:
    name, num = name.split('__')
  else:
    num = '1'

  if not os.path.exists(name):
    os.mkdir(name)
  shutil.move(f, name + '/' + num + '.jpg')



