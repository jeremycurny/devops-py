#!/usr/bin/env python

import argparse, json, os, re, sys

parser = argparse.ArgumentParser(description='Devops Py Composer Validation.')
parser.add_argument('--patch-forced-vendors', default=[], help='Vendors forced to have a patch update package version (~)')
parser.add_argument('--minor-forced-vendors', default=[], help='Vendors forced to have a minor update package version (^)')
parser.add_argument('argv', metavar='argv', nargs='+', help='Composer file')
args = parser.parse_args()

composerJsonPath = args.argv[0]
minorForcedVendors = args.minor_forced_vendors
patchForcedVendors = args.patch_forced_vendors

if minorForcedVendors != []:
  minorForcedVendors = minorForcedVendors.split(',')

if patchForcedVendors != []:
  patchForcedVendors = patchForcedVendors.split(',')

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
  vendor=package.split('/')[0]
  if not re.search('^((~|\^)?[0-9]+\.[0-9]+\.[0-9]+)(\|((~|\^)?[0-9]+\.[0-9]+\.[0-9]+))*', version):
    print "Incorrect version for " + package + ": " + version
    sys.exit(1)
  if vendor in minorForcedVendors and not re.search('^\^', version):
    print "Minor update syntax should be used for vendor: " + vendor + " (" + package + ": " + version + ")"
    sys.exit(1)
  if vendor in patchForcedVendors and not re.search('^~', version):
    print "Patch update syntax should be used for vendor: " + vendor + " (" + package + ": " + version + ")"
    sys.exit(1)
