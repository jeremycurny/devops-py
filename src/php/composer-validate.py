#!/usr/bin/env python

import json, os, re, sys

if len (sys.argv) != 2 :
  # Argv is missing
  print "Usage: python " + __file__ + " ./composer.json"
  sys.exit(1)

if not os.path.exists(sys.argv[1]):
  # File does not exists
  print "File " + sys.argv[1] + " not found"
  sys.exit(1)

file = open(sys.argv[1], "r")
composerJsonContent = file.read()
file.close()

composerData = json.loads(composerJsonContent)
composerRequireData = composerData.get('require', [])

for package,version in composerRequireData.iteritems():
  if not re.search('^(~|\^)?[0-9]+\.[0-9]+\.[0-9]+', version):
    print "Incorrect version for " + package + ": " + version
    sys.exit(1)
