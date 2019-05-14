#!/usr/bin/env python

import argparse, json, os, re, sys

parser = argparse.ArgumentParser(description='Devops Py Composer Validation.')
parser.add_argument('argv', metavar='argv', nargs='+', help='Composer file')
args = parser.parse_args()

if len(args.argv) != 1 :
  # Argv is missing
  print "Usage: python " + __file__ + " ./composer.json"
  sys.exit(1)

composerJsonPath = args.argv[0];

if not os.path.exists(composerJsonPath):
  # File does not exists
  print "File " + composerJsonPath + " not found"
  sys.exit(1)

file = open(composerJsonPath, "r")
composerJsonContent = file.read()
file.close()

composerData = json.loads(composerJsonContent)
composerRequireData = composerData.get('require', [])

for package,version in composerRequireData.iteritems():
  if not re.search('^(~|\^)?[0-9]+\.[0-9]+\.[0-9]+', version):
    print "Incorrect version for " + package + ": " + version
    sys.exit(1)
