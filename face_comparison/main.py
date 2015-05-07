import sys
from compare import compare

from subprocess import call, Popen, PIPE
from os import listdir
import sys
import Queue
import os.path

#controls the number of matches that the code will return
NUM_MATCHES = 3

def compare( test, cDir ):
    if os.path.isfile(test):
        comparisons = listdir(cDir)

        matches = Queue.PriorityQueue(0)
        for img in comparisons:
            compOutput = Popen(["br", "-algorithm", "FaceRecognition", "-compare", test, cDir + "/" + img],
                stdout=PIPE, stderr=PIPE)
            data = compOutput.communicate()
            index = data[0].strip()
            matches.put((-float(index), cDir + "/" + img))

        hits = []
        for i in range(NUM_MATCHES):
            try:
                match = matches.get_nowait()
                hits.append(match)
            except Queue.Empty:
                break
        return hits

        #outfile = open("face_compare_info.txt", "w")

        #outfile.write(str(len(hits)) + "\n")
        #for hit in hits:
        #    index = -hit[0]
        #    name  = hit[1]
        #    outfile.write("%s %s\n" % (name, str(index)))
    else:
        print "Test image " + test + " not found"
        return None


if len(sys.argv) != NUM_MATCHES:
    print "Usage: python main.py IMAGE_PATH COMPARISON_DIRECTORY"
    sys.exit(0)
else:
    matches = compare(sys.argv[1], sys.argv[2])
    print matches
# turn into single function
# return a array of tuples with the image name and correlation
        