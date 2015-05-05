from subprocess import call, Popen, PIPE
from os import listdir
import sys
import Queue
import os.path

#controls the number of matches that the code will return
NUM_MATCHES = 3

if len(sys.argv) != 3:
	print "Usage: python main.py IMAGE_PATH COMPARISON_DIRECTORY"
	sys.exit(0)

#test = raw_input("Enter test image name (must be in same directory): ")
test = sys.argv[1]
if os.path.isfile(test):
        #cDir = raw_input("Enter comparison directory: ")
        cDir = sys.argv[2]
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
        		hits.append(match[1])
        		print match
        	except Queue.Empty:
        		break

        #outfile = open("face_compare_info.txt", "w")

        #size = len(hits)
        #outfile.write(str(size)) + "\n")
		#for i in range(size):
else:
	print "Test image " + test + " not found"
	sys.exit(0)
        