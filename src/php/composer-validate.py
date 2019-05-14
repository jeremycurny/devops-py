#!/usr/bin/env python

import argparse, json, os, re, sys

parser = argparse.ArgumentParser(description='Devops Py Composer Validation.')
parser.add_argument('--minor-syntax-forced-vendors', default=None, help='Vendors forced to have a minor update syntax package version (^)')
parser.add_argument('argv', metavar='argv', nargs='+', help='Composer file')
args = parser.parse_args()

composerJsonPath = args.argv[0];
print args.minor_syntax_forced_vendors

if args.minor_syntax_forced_vendors != None:
  minorSyntaxForcedVendors = args.minor_syntax_forced_vendors.split(',');
else:
  minorSyntaxForcedVendors = [];

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
