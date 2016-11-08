#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import copy
import io
import lxml.etree as ET
import hjson
import sys
import tempfile
#import xml.etree.ElementTree as ET
#tree = ET.parse('/home/jmramoss/almacen/plantillas_collage/test/dibujo.svg')
#root = tree.getroot()
#root.set('updated', 'yes')
#ET.dump(root)

#import uuid
#unique_filename = uuid.uuid4()
#print unique_filename

#tree.write('/home/jmramoss/almacen/plantillas_collage/test/dibujo.output.svg')

from lxml import etree, objectify

class Clip:
  def __init__ (self):
    self.title = None
    self.description = None
    self.image = None
    self.date = None
    self.clips = None

  def getTitle (self):
    return self.title

  def setTitle (self, newValue):
    self.title = newValue

  def getDescription (self):
    return self.description

  def setDescription (self, newValue):
    self.description = newValue

  def getImage (self):
    return self.image

  def setImage (self, newValue):
    self.image = newValue

  def getDate (self):
    return self.date

  def setDate (self, newValue):
    self.date = newValue

  def getClips (self):
    return self.clips

  def setClips (self, newValue):
    self.clips = newValue

  def getClipsSize (self):
    result = 0
    result = 0 if self.clips is None else len(self.clips)
    return result

  def addClip (self, clip):
    if not (clip is None):
      if self.clips is None:
        self.clips = []
      self.clips.append(clip)

  def delClip (self, clip):
    result = False
    if (clip is not None) and (self.clips is not None):
      try:
        self.clips.remove(clip)
        result = True
      except:
        result = False
    return result

  def isLeaf (self):
    return (self.getClipsSize() <= 0)

  def isMulti (self):
    return (self.getClipsSize() > 0)

  def hasTitle (self):
    value = '' if self.title is None else self.title.strip()
    return (len(value) > 0)

  def hasDescription (self):
    value = '' if self.description is None else self.description.strip()
    return (len(value) > 0)

  def hasDate (self):
    value = '' if self.date is None else self.date.strip()
    return (len(value) > 0)

  def hasImage (self):
    value = '' if self.image is None else self.image.strip()
    return (len(value) > 0)

  def hasClips (self):
    value = [] if self.title is None else self.clips
    return (len(value) > 0)



class ClipGenerator:
  def __init__ (self):
    pass

  def buildFromFolder (self, folder, groupSize=4, title=None, description=None):
    result = None
    result = Clip()
    result.setTitle(title)
    result.setDescription(description)

    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    print files
    clip = None
    for f in files:
      if clip is None or clip.getClipsSize() >= groupSize:
        clip = Clip()
        result.addClip(clip)
      img = Clip()
      imagePath = os.path.join(folder, f)
      img.setImage(imagePath)
      clip.addClip(img)

    return result


'''
svg = SvgManager('/home/jmramoss/almacen/plantillas_collage/test/dibujo.svg')
#root = svg.getRoot()
#svg.setAttr(root, 'updated2', 'yes')

#print '{0}, {1}, {2}'.format('a', 'b', 'c')


id = svg.getId()
if (id == "title"):
  for x in range(0, 30):
    transformTitle(svg, u"> Item " + str(x + 1), "file_" + str(x + 1))

'''


def transformTitle (svg, title, output):
  desc = svg.getDescription()
  data = {'title': title}
  exec(desc)
#  eTitle = svg.findByName('title')
#  eSpan = svg.firstChild(eTitle)
#  eSpan.text = title
  svg2 = svg.saveAs(output + ".svg")
  svg2.saveAsPng(output + ".png")
  if os.path.isfile(svg2.fileXml):
    os.remove(svg2.fileXml)

def transformCollage (svg, output):
  for x in range(1, 7):
    svg.setImg("frame" + str(x) + "_image", "/home/jmramoss/almacen/plantillas_collage/test/file_" + str(x) + ".png")

  svg2 = svg.saveAs(output + ".svg")
  svg2.saveAsPng(output + ".png")
#  if os.path.isfile(svg2.fileXml):
#    os.remove(svg2.fileXml)

def transformClip (svg, clip, idx):
  desc = svg.getDescription()
  exec(desc)
  svg2 = svg.saveAs("venga_" + str(idx) + ".svg")
  svg2.saveAsPng("venga_" + str(idx) + ".png")
  if True and os.path.isfile(svg2.fileXml):
    os.remove(svg2.fileXml)


#  index = 1
#  for item in clip.getClips():
#    svg.setImg("frame" + str(index) + "_image", item.getImage())
#    index = index + 1
#  for i in range(clip.getClipsSize() + 1, 6 + 1):
#    svg.remove("frame" + str(i))

'''
svg = SvgManager('/home/jmramoss/almacen/ORLAS/resources/drawing.svg')
svg.embedSVG('rectangulo1', '/home/jmramoss/almacen/ORLAS/resources/res1.svg')
svg.embedSVG('rectangulo2', '/home/jmramoss/almacen/ORLAS/resources/res1.svg')
svg.embedSVG('rectangulo3', '/home/jmramoss/almacen/ORLAS/resources/res1.svg')
'''


'''
import re

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

'''
svg = SvgManager('/home/jmramoss/almacen/ORLAS/resources/clips/header.svg')
svg.transform(obj)
svg2 = svg.saveAs("/home/jmramoss/almacen/ORLAS/resources/clips/test_header.svg")
#svg2.saveAsPng("venga_" + str(idx) + ".png")
'''

'''
for key in themes.keys():
  svg = SvgManager('/home/jmramoss/almacen/ORLAS/resources/clips/orla.svg')
  obj['theme'] = themes[key]
  svg.transform(obj)
  svg2 = svg.saveAs("/home/jmramoss/almacen/ORLAS/resources/clips/test_orla.svg")
  svg2.saveAsPngA4('test_orla_' + key + '.png')
'''

'''
svg = SvgManager('/home/jmramoss/almacen/ORLAS/resources/clips/female_student.svg')
student = obj['students'][0]
print student
svg.transform(student)
svg2 = svg.saveAs("/home/jmramoss/almacen/ORLAS/resources/clips/test_female_student.svg")
'''

'''
gen = ClipGenerator()
clip = gen.buildFromFolder('/home/jmramoss/almacen/plantillas_collage/test/files', 4, u"Título", u"Descripción")
clipIdx = 1
for item in clip.getClips():
  svg = SvgManager('/home/jmramoss/almacen/plantillas_collage/test/animales1.svg')
  transformClip(svg, item, clipIdx)
  clipIdx = clipIdx + 1
  


#svg = SvgManager('/home/jmramoss/almacen/plantillas_collage/test/animales1.svg')
#transformCollage(svg, 'test')
'''

