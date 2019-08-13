#!/usr/bin/env python

import csv, json, operator, os, sys
import xml.etree.ElementTree as ET

composerJsonPath = 'composer.json'
languageXmlPath = 'language.xml'

if not os.path.exists(composerJsonPath):
  # File does not exists
  print "File " + composerJsonPath + " not found"
  sys.exit(1)

if not os.path.exists(languageXmlPath):
  # File does not exists
  print "File " + languageXmlPath + " not found"
  sys.exit(1)

file = open(composerJsonPath, "r")
composerJsonContent = file.read()
file.close()

composerTypeData = json.loads(composerJsonContent)['type']
if composerTypeData != "magento2-language":
  # It's not a language package
  print "This is not a language package, type: " + composerTypeData
  sys.exit(1)

xml = ET.parse(languageXmlPath)
languageCode = xml.getroot().find('code').text

languageCsvPath = languageCode + '.csv'

if not os.path.exists(languageCsvPath):
  # File does not exists
  print "File " + languageCsvPath + " not found"
  sys.exit(1)

cleanData = []
with open(languageCsvPath) as f:
    rawData = csv.reader(f, delimiter=',')
    for rawRow in rawData:
        if len(rawRow) == 0:
            # Empty line
            continue;
        if rawRow[0][:1] == "#":
            # Commented line
            continue;
        if len(rawRow) < 4:
            # Wtf is this
            print "Incorrect line: \"" + ','.join(rawRow) + "\""
            print "At least 4 columns are expected"
            sys.exit(1)
        if (rawRow[2] not in ["module", "theme"]):
            # 3rd column incorrect
            print "Incorrect line: \"" + ','.join(rawRow) + "\""
            print "3rd column has to be \"module\" or \"theme\", current value: " + rawRow[2]
            sys.exit(1)
        cleanData.append(rawRow)
    f.close()

cleanData = sorted(cleanData, key=operator.itemgetter(2,3,0,1))

with open(languageCsvPath, 'wb') as f:
    currentPackage = ""
    writer = csv.writer(f)
    for row in cleanData:
        rowPackage = row[2].capitalize() + " " + row[3]
        if rowPackage != currentPackage:
            if currentPackage != "":
                writer.writerow([])
            currentPackage = rowPackage
            writer.writerow(["## " + currentPackage + " ##"])
        writer.writerow(row)
    f.close()
