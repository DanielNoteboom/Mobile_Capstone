from compare import compare
import sys
if len(sys.argv) != 2:
  print "Usage python practice.py IMAGE_FILE"
print compare(sys.argv[1], "c1")
