#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import hjson
import sys


def printAllGroups (matchObj, varName):
  if matchObj:
    groups = matchObj.groups()
    size = len(groups)
    idx = 0
    data = {}
    for group in groups:
      print "idx = " + str(idx) + " : " + group
      data[varName + str(idx)] = group
      idx += 1
    print str(data)
    print "matchObj.group() : ", matchObj.group()
    for idx in range(size):
      print "matchObj.group(" + str(idx) + ") : ", matchObj.group(idx)
  else:
    print "No match!!"


def processMain ():
  base = os.path.dirname(os.path.abspath(__file__))#'/home/jmramoss/almacen/ORLAS/resources/'

  infileAddr = os.path.join(base, 'gthemes.svd')
  if len(sys.argv) > 1:
    infileAddr = sys.argv[1]
    if not infileAddr.startswith(os.sep):
      infileAddr = os.path.join(base, infileAddr)
  #print infileAddr
  infile = open(infileAddr, 'r')
  obj = hjson.load(infile, use_decimal=True)
  #print obj

  clipsFolder = os.path.join(base, 'clips')
  backgroundFolder = os.path.join(clipsFolder, 'backgrounds')
  regexBackground = obj['tgenerator']['background']
  print 'regexBackground = ' + regexBackground
  files = os.listdir(backgroundFolder)
  for f in files:
    expr = regexBackground + ".svg"
    print 'expr = ' + expr
#if re.search(my_regex, subject, re.IGNORECASE):
#    matchObj = re.match(r'(.*)type(.*).svg', f, re.M|re.I)
    matchObj = re.search(expr, f, re.M|re.I)
    if matchObj:
      print 'file = ' + f
    printAllGroups(matchObj, 'background')

if __name__ == '__main__':
  processMain()


  

'''
line = "Cats are smarter than dogs"

matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)
if matchObj:
  groups = matchObj.groups()
  size = len(groups)
  idx = 0
  data = {}
  for group in groups:
    print "idx = " + str(idx) + " : " + group
    data['var' + str(idx)] = group
    idx += 1
  print str(data)

  print "matchObj.group() : ", matchObj.group()
  print "matchObj.group(0) : ", matchObj.group(0)
  print "matchObj.group(1) : ", matchObj.group(1)
  print "matchObj.group(2) : ", matchObj.group(2)
else:
  print "No match!!"
'''
