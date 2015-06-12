import sys
import os
sys.path.insert(0, '..')
from facepp.face_plus_plus import facial_detection, compare, add_face
from facepp.train_groups import update_group


def analyze_results(directory):
  update_group(directory, directory)
  correct = 0
  total = 0
  top_three = 0
  for person in os.listdir(directory + "_test"):
    print "person"
    print person
    if os.path.isdir(directory + "_test/" + person):
      for face in os.listdir(directory + "_test/" + person):
        total += 1
        if face[-8:] != "DS_Store":
          print face
          faces = facial_detection(directory + "_test" + "/" + person + "/" +  face, 0, 0)
          if len(faces) != 1:
            print "There should be 1 and only 1 face in the picture"
            continue
          face = faces[0]
          matches = compare(face, directory)
          for j, match in enumerate(matches):
            if j == 0 and match['id'] == person:
              correct += 1
              top_three += 1
            elif match['id'] == person:
              top_three += 1
  print "results for " + str(total) + " faces"
  print str(correct) + "/" + str(total) + " or " + str((correct * 100.0)/total) + "% accuracy correct"
  print str(top_three) + "/" + str(total) + " or " + str((top_three * 100.0)/total) + "% accuracy for top three"
 




if __name__ == "__main__":
  if len(sys.argv) != 2:
    print "USAGE: results.py DIRECTORY_NAME"
    print  "DIRECTORY_NAME should also have another directory with the test images with _test appended"
  directory = sys.argv[1]
  analyze_results(directory)

