from face import get_top_matches
import sys

if len(sys.argv) != 2:
  "Usage: python practice.py IMAGE_FILE"
matches = get_top_matches(sys.argv[1], 0, 0)
print matches
