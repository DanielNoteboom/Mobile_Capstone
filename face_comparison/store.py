from os import listdir
import sys
import os.path
import shutil

#controls the number of matches that the code will return
IMAGE_DIR = "c1"

# stores the parameter image in the comparison folder
# @param image  the image path to be copied
# @param id     the id of the image
def add_training_data( image, id ):
  id.replace(" ", "_")
  identities = listdir(IMAGE_DIR)
  if id in identities:
    images = listdir(IMAGE_DIR + "/" + id)
    shutil.copyfile(image, os.path.join(IMAGE_DIR + "/" + id, str(len(images)+1)+".jpg"))
  else:
    print id + " does not exist in our records!"
    sys.exit(0)

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print "Usage: python store.py IMAGE_PATH IMAGE_ID"
    sys.exit(0)
  else:
    add_training_data(sys.argv[1], sys.argv[2])
