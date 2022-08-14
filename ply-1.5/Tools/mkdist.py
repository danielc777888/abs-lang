#!/usr/local/bin/python

# This script builds a PLY distribution.
# Usage : mkdist.py dirname 

import sys
import string

try:
   dirname = sys.argv[1]
except:
   print "Usage: mkdist.py directory"
   sys.exit(0)

# If directory exists, remove it
import os
print "Removing ", dirname
os.system("rm -rf "+dirname)

# Do a CVS export on the directory name

print "Checking out PLY"
os.system("cvs export -D now -d "+dirname+ " PLY")

print "Blowing away .cvsignore files"
os.system("find "+dirname+" -name .cvsignore -exec rm {} \\;");

# Build the tar-ball
os.system("tar -cf "+string.lower(dirname)+".tar "+dirname)
os.system("gzip "+string.lower(dirname)+".tar")

