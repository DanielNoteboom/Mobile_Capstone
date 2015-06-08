from subprocess import call, Popen, PIPE
from os import listdir
import sys
import Queue
import os.path
import cv2

#controls the number of matches that the code will return
NUM_MATCHES = 3

def compare_multi( test_dir, train_dir):
  if not os.path.isdir(test_dir):
    print "Invalid test directory " + cDir
    return None
  if not os.path.isdir(train_dir):
    print "Invalid training directory " + cDir
    return None

  results = {}
  ct = 0
  correct = 0
  correct_or_close = 0
  identities = os.listdir(test_dir)
  for identity in identities:
    images = os.listdir(test_dir+'/'+identity)
    for image in images:
      res = compare(os.path.abspath(test_dir+'/'+identity+'/'+image), train_dir)
      if res[0]['id'] == identity:
        correct += 1
        correct_or_close += 1
      if res[1]['id'] == identity or res[2]['id'] == identity:
        correct_or_close += 1
      results[str(identity)+str(image)] = res
      ct += 1
  print "Fraction correct = " + str(correct/float(ct))
  print "Fraction close   = " + str(correct_or_close/float(ct))
  return results


# returns an array with the top NUM_MATCHES comparison match
# @params
#   test    the image file to be identified
#   cDir    the directory containing subdirectories of test images
def compare( test, cDir ):

  if not os.path.isfile(test):
    print "Invalid test image " + test
    return None

  if not os.path.isdir(cDir):
    print "Invalid directory " + cDir
    return None
  
  eigen_matches = get_eigen_matches(cDir, runOpenBR(test, cDir))
  return matchInfo(eigen_matches)

def runOpenBR( test, cDir ):
  # OpenBR recursively compares across all images in subdirectories
  compOutput = Popen(["br", "-algorithm", "FaceRecognition", "-compare", 
                      test, cDir], stdout=PIPE, stderr=PIPE)
  data = compOutput.communicate()
  # data is contained in fist index of output
  dataArray = str(data[0]).split()
  scores = []
  indices = range(len(dataArray))
  for i in indices[2::2]:
    try:
      scores.append(float(dataArray[i]))
    except ValueError:
      pass # nondeterministic pipe output from openbr
  return scores

def get_eigen_matches( cDir, scores ):
  matches = Queue.PriorityQueue(0)
  extCtr = 0 # index in the large array
  comparisons = listdir(cDir)
  # only works because both OpenBR and python recurse thru dirs alphanumerically
  for identity in comparisons:
    if os.path.isdir(cDir + "/" + identity):
      idScores = []
      max = 0.0

      # aggregate all scores for a given id
      images = listdir(cDir + "/" + identity)
      numImages = len(images)
      bestImage = 0
      for i in range(numImages):
        if extCtr < len(scores):
          score = scores[extCtr]
          extCtr += 1
          if score > max:
            max = score
            bestImage = i
          idScores.append(score)
        else: # add "harmless" mean value if out of range. TODO best approach?
          if len(idScores) != 0:
            idScores.append(sum(idScores)/float(len(idScores)))
          else:
            idScores.append(0)
      if idScores:
        matches.put((-sum(idScores)/numImages, -sorted(idScores)[numImages/2], #average, median
        #matches.put((-sorted(idScores)[numImages/2], -sum(idScores)/numImages, #median, average
                    {
                      'id': identity,
                      'match_path': os.path.abspath(cDir + "/" + identity + "/" + images[bestImage])
                    }))
  return matches

def matchInfo( matches ):
  hits = []
  for i in range(NUM_MATCHES):
      try:
          hit = matches.get_nowait()
          hits.append({
            'match_path': hit[2]['match_path'], 
            'id': hit[2]['id'], 
            'median': -hit[1],
            'average': -hit[0]
            #'median': -hit[0],
            #'average': -hit[1]
          })
      except Queue.Empty:
        return None
  return hits

def getMatchesBySubDirectory(cDir, comparisons): #tooSlow
  matches = Queue.PriorityQueue(0)
  for identity in comparisons:
    if os.path.isdir(cDir + "/" + identity):  
      cImages = listdir(cDir + "/" + identity)
      aggregateIndex = 0
      compOutput = Popen(["br", "-algorithm", "FaceRecognition", "-compare", 
                          test, cDir + "/" + identity],
                          stdout=PIPE, stderr=PIPE)
      data = compOutput.communicate()
      dataArray = str(data[0]).split()
      source = str(data[1]).split()[9].split("/")[1]
      for i in range(len(dataArray)):
        if i % 2 == 0 and i != 0:
          aggregateIndex += float(dataArray[i].strip())
      matches.put((-aggregateIndex, os.path.abspath(cDir + "/" + identity)))

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print "Usage: python compare.py COMPARISON_DIRECTORY IMAGE_PATH|TEST_DIR_PATH"
    sys.exit(0)
  else:
    if os.path.isdir(sys.argv[2]):
      matches = compare_multi(sys.argv[2], sys.argv[1])
      for test in matches.keys():
        print test + ": "
        i = 1
        for match in matches[test]:
          print str(i) + ": " + match['id']
          i += 1
    elif os.path.isfile(sys.argv[2]):
      matches = compare(sys.argv[2], sys.argv[1])
      print matches
