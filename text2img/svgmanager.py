#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import copy
import io
import lxml.etree as ET
import hjson
import sys
import tempfile
#import argparse

from PIL import Image

from lxml import etree, objectify

class SvgManager:
  def __init__(self, fileXml, repository=None, resources=None):
    if not os.path.isfile(fileXml):
      raise Exception('File "' + fileXml + '" IS NOT EXISTS')
    self.fileXml = fileXml
    self.repository = repository
    self.resources = resources

#    self._adaptXml()
    parser = etree.XMLParser(remove_blank_text=True, ns_clean=True, no_network=True, load_dtd=False, dtd_validation=False, recover=True)
    self.tree = etree.parse(self.fileXml, parser)
#    xml = u'<?xml version="1.0" standalone="no"?>\n' + u'<hola></hola>'
#    self.tree = etree.parse(io.BytesIO(xml))
    #self.tree = etree.XML(xml)
    self.root = self.tree.getroot()
#    self.root.attrib.pop('xmlns:svg')
    #self.root.attrib.pop('id')
#    print "------"
#    print self.root.nsmap
#    print "------"
    self.currentNode = self.root
#    self.tree.register_namespace('xlink', 'http://www.w3.org/TR/xlink/')
#    self.namespaces = {'dc':'http://purl.org/dc/elements/1.1/', 'cc':'http://creativecommons.org/ns#', 'rdf':'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 
#  'svg':'http://www.w3.org/2000/svg', 'ns':'http://www.w3.org/2000/svg', 'sodipodi':'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd', 
#  'inkscape':'http://www.inkscape.org/namespaces/inkscape'}
    self.namespaces = self.root.nsmap
  
  def _adaptXml (self):
    print "hola"

  def getRoot (self):
    return self.root

  def getTree (self):
    return self.tree

  def save (self):
    result = None
    objectify.deannotate(self.root, cleanup_namespaces=True)
    self.tree.write(fileXml, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    result = self
    return result

  '''
    http://janmi.com/a4-en-pixeles/
    https://megustalapapeleria.com/2013/10/28/cuantos-pixeles-tiene-un-a4/
    https://megustalapapeleria.com/2013/12/07/cuantos-pixeles-tiene-un-a3/

    300mm x 200mm = 11,81i x 7,87i
     440ppp -> 5196 px x 3463 px

    1 pulgada = 25'40mm
    A4=210mm x 297mm= 8,2677 pulgadas x 11,6929 pulgadas
    72dpi -> 595,2744 x 841,8888

    A3, Din A-3, Dinatres, atres, mide en centimetros: 29,7cm x 42,0cmm o en milimetros: 297mm x 420mm
      Un A-3 a 72 ppp (pixeles por pulgada)    842 x 1191
      Un A-5 a 150 ppp (pixeles por pulgada)   1754 x 2480
      Un A-5 a 300 ppp (pixeles por pulgada)   3508 x 4961
    A4, Din A-4, Dinacuatro, mide 21×29,7cm
      Un A-4 a 72 ppp    595 x 842
      Un A-4 a 150 ppp   1240 x 1754
      Un A-4 a 300 ppp   2480 x 3508
    A4
      A4 -> 21×29,7 cm -> 72dpi ->595x842px
      A4 -> 21×29,7 cm -> 300dpi ->2479x3508px
    DIN-A4:
      300dpi -> 2480x3508 px (SUFICIENTE PARA IMPRESIÓN EN PAPEL)
      96dpi -> 794x1123 px
      72dpi -> 595x842 px (TAMAÑO WEB, SCREEN)
  '''

  def saveAs (self, target):
    result = None
    #print 'saveAs ' + self.fileXml
    if not target.startswith("/"):
      target = os.path.dirname(self.fileXml) + "/" + target
      #print ">>>>>>>>>>>>>>> " + target
    #print 'saveAs target = ' + target
    if os.path.isfile(target):
      os.remove(target)
    objectify.deannotate(self.root, cleanup_namespaces=True)
    self.tree.write(target, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    result = SvgManager(target, repository=self.repository, resources=self.resources)
    return result

  def previewAsPng (self, output):
    if not output.startswith("/"):
      output = os.path.dirname(self.fileXml) + "/" + output
      #print ">>>>>>>>>>>>>>> " + output
    os.system("inkscape --export-png=" + output + " -w 842 -h 595 --export-dpi=72 " + " " + self.fileXml + ' >> /dev/null')

  def saveAsPng (self, output):
    if not output.startswith("/"):
      output = os.path.dirname(self.fileXml) + "/" + output
      #print ">>>>>>>>>>>>>>> " + output
    os.system("inkscape --export-png=" + output + " " + self.fileXml + ' >> /dev/null')

  def saveAsPngA4 (self, output):
    if not output.startswith("/"):
      output = os.path.dirname(self.fileXml) + "/" + output
      #print ">>>>>>>>>>>>>>> " + output
    os.system("inkscape --export-png=" + output + " -w 5145 -h 3638 --export-dpi=440 " + self.fileXml + ' >> /dev/null')

  def saveAsPng30x20 (self, output):
    if not output.startswith("/"):
      output = os.path.dirname(self.fileXml) + "/" + output
      #print ">>>>>>>>>>>>>>> " + output
    os.system("inkscape --export-png=" + output + " -w 5196 -h 3463 --export-dpi=440 " + self.fileXml + ' >> /dev/null')

  def saveAsJpg30x20 (self, output):
    png = output + '.png'
    self.saveAsPng30x20(png)
    quality = ' -quality 100'
    quality = ''
    os.system('convert' + quality + ' -compress lossless ' + png + ' ' + output)
    if os.path.isfile(output) and os.path.isfile(png):
      os.remove(png)

  def previewAsJpg (self, output):
    png = output + '.png'
    self.previewAsPng(png)
    quality = ' -quality 100'
    quality = ''
    os.system('convert' + quality + ' -compress lossless ' + png + ' ' + output)
    if os.path.isfile(output) and os.path.isfile(png):
      os.remove(png)

  def saveAsJpg (self, output):
    png = output + '.png'
    self.saveAsPng(png)
    quality = ' -quality 100'
    quality = ''
    os.system('convert' + quality + ' -compress lossless ' + png + ' ' + output)
    if os.path.isfile(output) and os.path.isfile(png):
      os.remove(png)

  def saveAsJpgA4 (self, output):
    png = output + '.png'
    self.saveAsPngA4(png)
    quality = ' -quality 100'
    quality = ''
    os.system('convert' + quality + ' -compress lossless ' + png + ' ' + output)
    if os.path.isfile(output) and os.path.isfile(png):
      os.remove(png)

  def getCurrentNode (self):
    return self.currentNode

  def setCurrentNode (self, currentNode):
    self.currentNode = currentNode

  def find (self, xpath):
    result = None
    result = self.currentNode.find(xpath, namespaces=self.namespaces)
    return result

  def findAll (self, xpath):
    result = None
    result = self.currentNode.findall(xpath, namespaces=self.namespaces)
    return result

  def setAttr (self, node, attrName, attrValue):
    node.set(attrName, attrValue)

  def pprint (self, node):
    print(etree.tostring(node, pretty_print=True))

  def debug (self, name, node):
    print "################# " + name + " (begin)"
    print(etree.tostring(node, pretty_print=True))
    print "################# " + name + " (end)"

  def findObject (self, type, label):
    result = None
    result = self.find(".//ns:" + type + "[@inkscape:label='" + label + "']")
    return result

  def findByType (self, type):
    result = None
    result = self.find(".//" + type + "")
    return result

  def findByName (self, name):
    result = None
    result = self.find(".//*" + "[@inkscape:label='" + "#%" + name + "']")
    return result

  def firstChild (self, node):
    result = None
    count = 1
    for item in node.iter():
      if count == 0:
        result = item
        break
      count = count - 1
    return result

  def firstChildType (self, node, type):
    result = None
    for item in node.iter():
      tagIdx = item.tag.index('}')
      tag = item.tag[(tagIdx+1):] if tagIdx > -1 else item.tag
      if tag == type:
        result = item
        break
    return result

  def getId (self): 
    result = None
    node = self.findByType("dc:identifier")
    result = node.text
    return result

  def getDescription (self): 
    result = None
    node = self.findByType("dc:description")
    result = node.text if node is not None else None
    return result

  def setImg (self, id, image, mode=None):
    basename = os.path.basename(image)
    #print 'image = ' + image
    #print 'basename = ' + basename
    #print self.fileXml

    #/home/jmramoss/almacen/ORLAS/resources/clips/student.svg
    #print os.path.dirname(self.fileXml)
    folder = os.path.dirname(self.fileXml)
    #folder = '/home/jmramoss/almacen/ORLAS/resources/'
    folder = self.resources if self.resources is not None else os.path.dirname(os.path.abspath(__file__))
    #print 'folder images = ' + folder
    absimg = image
    if not absimg.startswith(os.sep):
      absimg = os.path.join(folder, image)
    #print 'absimg = ' + absimg
    eImage = self.findByName(id)
    eImage.set('{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}absref', absimg)
    eImage.set('{http://www.w3.org/1999/xlink}href', absimg)
    if mode == 'preserve':
      svgImgWidth = float(eImage.get('width'))
      svgImgHeight = float(eImage.get('height'))
      svgImgRatio = svgImgWidth / svgImgHeight
      if os.path.isfile(absimg):
        im = Image.open(absimg)
        imWidth, imHeight = im.size
        imRatio = float(imWidth) / float(imHeight)
        if abs(imRatio - svgImgRatio) > 0.001:
          #print 'img Width = ' + str(svgImgWidth)
          #print 'img Height = ' + str(svgImgHeight)
          preserveWidth = svgImgWidth / imRatio
          preserveHeight = svgImgHeight * imRatio
          newWidth = svgImgWidth
          newHeight = svgImgHeight
          if preserveWidth < svgImgHeight:
            newWidth = svgImgWidth
            newHeight = preserveWidth
          elif preserveHeight < svgImgWidth:
            newWidth = preserveHeight
            newHeight = svgImgHeight
          #print 'real img Width = ' + str(imWidth)
          #print 'real img Height = ' + str(imHeight)
          #print 'newWidth = ' + str(newWidth)
          #print 'newHeight = ' + str(newHeight)
          eImage.set('width', str(newWidth))
          eImage.set('height', str(newHeight))

  def padText (self, text, size):
    result = text
    lengthText = len(text)
    if (lengthText > 0 and lengthText < size):
      diffSize = size - lengthText
      if diffSize > 1:
        #result = ' ' * int((diffSize / 2)) + result
        result = (' ' * (diffSize - 1)) + result
    return result

  def setText (self, id, text, transform=None):
    eNode = self.findByName(id)
    #.//ns:" + type + 
    #eSpan = eNode.find('.//tspan', namespaces=self.namespaces)
    #eSpan = svg.firstChild(eNode)
    eSpan = self.firstChildType(eNode, 'tspan')
    eSpan = eSpan if eSpan is not None else self.firstChild(eNode)
    #eSpan.text = u'text'
    toXml = text.decode('utf-8')
    if transform == 'upper':
      toXml = toXml.upper()
    elif transform == 'capitalize':
      toXml = toXml.capitalize()
    elif transform == 'lower':
      toXml = toXml.lower()
    elif transform == 'swapcase':
      toXml = toXml.swapcase()
    elif transform == 'title':
      toXml = toXml.title()
    eSpan.text = toXml
    #eSpan.text = text

  def setPadText (self, id, text, size, transform=None):
    padText = self.padText(text, size)
    #print 'padText = ' + padText
    self.setText(id, padText)

  def removeById (self, id):
    #print 'removeById = ' + id
    eNode = self.find(".//*[@id='" + id + "']")
    eNode.getparent().remove(eNode)

  def remove (self, name):
    eNode = self.findByName(name)
    eNode.getparent().remove(eNode)

  def remove_namespace(self, namespace):
    ns = u'{%s}' % namespace
    nsl = len(ns)
    for elem in self.tree.getiterator():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]

  def crop (self, img):
    fullpath = os.path.join(self.resources, img)
    import cropfaces
    cropFaces = cropfaces.CropFaces()
    cropFaces.crop1Head(fullpath, 'NEAR')
    print 'cropping img -> ' + fullpath

  def embedSVG (self, name, fileRes):
    svg = SvgManager(fileRes, repository=self.repository, resources=self.resources)
    self.remove_namespace('svg')

    eRootTarget = self.getRoot()
    #eRoot.cleanup_namespaces(eRoot)
    #xmlns:svg="http://www.w3.org/2000/svg"
    #del eRoot.attrib['xmlns:svg']
    '''
    for key in eRoot.attrib:
      print 'aaaa ' + key + ' -> ' + eRoot.get(key)
    
    nsmap = dict(eRoot.nsmap)
    if 'svg' in nsmap:
      print "-hola-"
      del nsmap['svg']
    print nsmap
    #eRoot.nsmap = nsmap
    
    print eRoot.nsmap
    '''
    eRootRes = svg.getRoot()

    '''
654,996
201,268
654,995875206
373.78436
factor = min(373.78436/376.65723, 201.2685/115.74002) = 1,74
scale = 1 / factor
realsize = (376.65723*factor, 115.74002*factor) = (654,995875206, 201,2685)
diffSize = realsize - viewbox = (140,605757603, 0)
translateY = screen.height - res.height = 936.62218
translateX = diffsize.width / factor = 80,855738464
    '''

    resWidth = float(eRootRes.get('width'))
    resHeight = float(eRootRes.get('height'))
    resViewBox = eRootRes.get('viewBox')
    resArrayViewBox = resViewBox.split(' ')
    resViewBoxWidth = float(resArrayViewBox[2])
    resViewBoxHeight = float(resArrayViewBox[3])
    resFactorWidth = resViewBoxWidth/resWidth
    resFactorHeight = resViewBoxHeight/resHeight
    resFactor = max(resFactorWidth, resFactorHeight)
    resRealSizeWidth = resWidth*resFactor
    resRealSizeHeight = resHeight*resFactor
    resDiffSizeWidth = resRealSizeWidth - resViewBoxWidth
    resDiffSizeHeight = resRealSizeHeight - resViewBoxHeight

    screenWidth = float(eRootTarget.get('width'))
    screenHeight = float(eRootTarget.get('height'))
    screenViewBox = eRootTarget.get('viewBox')
    screenArrayViewBox = screenViewBox.split(' ')
    screenViewBoxWidth = float(screenArrayViewBox[2])
    screenViewBoxHeight = float(screenArrayViewBox[3])

    #scale = min(resWidth/resViewBoxWidth, resHeight/resViewBoxHeight)
    scale = 1.0/resFactor
    #print 'resWidth = ' + str(resWidth)
    #print 'resHeight = ' + str(resHeight)
    #print 'resViewBox = ' + str(resViewBox)
    #print 'scale = ' + str(scale)
    translateY = +(screenHeight - resHeight)
    #translateY = 0
    #print 'translateY = ' + str(translateY)

    translateX = 0
    translateX = (resDiffSizeWidth / resFactor) / 2
    #print 'translateX = ' + str(translateX)
    #print 'translateY = ' + str((resDiffSizeHeight / resFactor))

    #eRoot.set('hola', 'vau')
    #ePeriquito = ET.Element('periquito')
    #eRoot.insert(1, ePeriquito)
    #eRoot.append(copy.deepcopy(eRoot[1]))
    
    listDefs = svg.findAll('.//{http://www.w3.org/2000/svg}defs')
    for eDefs in listDefs:
      eRootTarget.insert(1, eDefs)
    listG = svg.findAll(".//*[@inkscape:groupmode='layer']")
    listTarget = self.findAll(".//*[@inkscape:groupmode='layer']")
    ePivot = listTarget[0] if len(listTarget) > 0 else eRootTarget
    #ePivot.set('transform', 'translate(0, ' + str(translateY) + ')' + ' ' + 'scale(' + str(scale) + ')')

    rect = self.find(".//*[@id='" + name + "']")
    rectX = float(rect.get('x'))
    rectY = float(rect.get('y'))
    rectWidth = float(rect.get('width'))
    rectHeight = float(rect.get('height'))

    #print 'rectX = ' + str(rectX)
    #print 'rectY = ' + str(rectY)
    #print 'rectWidth = ' + str(rectWidth)
    #print 'rectHeight = ' + str(rectHeight)

    scaleRectWidth = rectWidth / resWidth
    scaleRectHeight = rectHeight / resHeight
    scaleRect = min(scaleRectWidth, scaleRectHeight)
    #print 'scaleRect = ' + str(scaleRect)
    #285,714 | 722,857 -> 1.6539531443 -> 472,558 | 507,376
    #scaleRect = 1.0

    newWidth = scaleRect * resWidth
    newHeight = scaleRect * resHeight

    diffWidth = rectWidth - newWidth
    diffHeight = rectHeight - newHeight

    for eG in listG:
      eG.attrib.pop('id')
      eG.attrib.pop('{http://www.inkscape.org/namespaces/inkscape}label')
      eG.attrib.pop('{http://www.inkscape.org/namespaces/inkscape}groupmode')
      #inkscape:label="Capa 1" inkscape:groupmode="layer" id="layer1"
      toAdd = eG
      #toAdd = eG[0] if len(eG) == 1 else eG
      oldTransform = eG.get('transform')
      oldTransform = '' if oldTransform is None else ' ' + oldTransform
      #print 'oldTransform = ' + oldTransform
      eG.set('transform', 'translate(' + str(translateX) + ', ' + str(translateY) + ')' + ' ' + 'scale(' + str(scale) + ')' + oldTransform)

      oldTransform = eG.get('transform')
      oldTransform = '' if oldTransform is None else ' ' + oldTransform
      eG.set('transform', 'scale(' + str(scaleRect) + ')' + oldTransform)

      oldTransform = eG.get('transform')
      oldTransform = '' if oldTransform is None else ' ' + oldTransform
      #eG.set('transform', 'translate(285.71429, 138.07643)' + oldTransform)
      #px = (rectX - screenWidth) + rectWidth
      #px = rectX + ((1-scaleRect) * rectX)
      px = rectX
      px = px + (diffWidth/2.0)

      py = (rectY - screenHeight) + rectHeight
      #py = py + (-1)*((1 - scaleRect) * py)
      py = py - (screenViewBoxHeight * (scaleRect - 1))
      py = py - (diffHeight/2.0)
      
      eG.set('transform', 'translate(' + str(px) + ', ' + str(py) + ')' + oldTransform)
      
      rect.addprevious(toAdd)
      #ePivot.append(toAdd)
    
    if True and not (rect is None):
      rect.getparent().remove(rect)
    
    #self.saveAs('/home/jmramoss/almacen/ORLAS/resources/drawing2.svg')

  def removeFile (self):
    if os.path.isfile(self.fileXml):
      os.remove(self.fileXml)

  def transform (self, data):
    result = None
    #print 'start: transforming ' + self.fileXml
    #print data
    desc = self.getDescription()
    if desc is not None:
      svg = self
      #exec(desc, {}, {svg:self, data:data})
      #exec(desc, {}, {svg:self})
      #exec(desc, {}, {svg:self, data:'hola'})
      exec(desc)
    #print 'end: transforming ' + self.fileXml

  def setPart (self, name, part, data):
    #folder = '/home/jmramoss/almacen/ORLAS/resources/clips'
    folder = self.repository if self.repository is not None else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clips2')
    #print 'folder>>>>>>>>>>>>> ' + folder
    #print 'h1'
    partFile = os.path.join(folder, part)
    #print 'h2 partFile = ' + partFile
    svgPart = SvgManager(partFile, repository=self.repository, resources=self.resources)
    #print 'h3 = ' + partFile
    svgPart.transform(data)
    #print 'h4'
    #partOutFile = folder + 'test_' + part
    partOutFile = os.path.join(os.path.dirname(partFile), 'test_' + os.path.basename(partFile))
    #print 'h5 partOutFile = ' + partOutFile
    svgPart2 = svgPart.saveAs(partOutFile)
    #print 'h6'
    self.embedSVG(name, partOutFile)
    #print 'h7'
    svgPart2.removeFile()

  @staticmethod
  def generate (args):
    base = os.path.dirname(os.path.abspath(__file__))#'/home/jmramoss/almacen/ORLAS/resources/'

    infileAddr = os.path.join(base, 'base.svd')
    if len(args) > 1:
      infileAddr = args[1]
      if not infileAddr.startswith(os.sep):
        infileAddr = os.path.join(base, infileAddr)
    #print infileAddr

    #infile = open('/home/jmramoss/almacen/ORLAS/resources/base.svd', 'r')
    infile = open(infileAddr, 'r')
    obj = hjson.load(infile, use_decimal=True)
    #print '>>>>>>>>>>> obj.title = ' + obj['title']
    #print '>>>>>>>>>>> obj.subtitle = ' + obj['subtitle']


    themesfile = None
    #print 'themesfile = ' + themesfile
    '''
    if len(args) > 2:
      themesfile = args[2]
      if not themesfile.startswith(os.sep):
        themesfile = os.path.join(base, themesfile)
    '''

    themesfile = obj['themes'] if 'themes' in obj else themesfile
    themesfile = themesfile if themesfile is not None else os.path.join(base, 'themes.svd')#open('/home/jmramoss/almacen/ORLAS/resources/themes.svd', 'r')

    inthemes = open(themesfile, 'r')
    themes = hjson.load(inthemes, use_decimal=True)


    homedir = os.path.expanduser("~")
    outputdir = os.path.join(homedir, 'text2img_output')
    if not os.path.exists(outputdir):
      os.makedirs(outputdir)

    templates = []
    templates = obj['templates'] if 'templates' in obj else templates
    #if len(templates) <= 0:
    #  folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clips')

    repository = None
    '''
    if len(args) > 3:
      repository = args[3]
    '''
    repository = obj['repository'] if 'repository' in obj else repository
    repository = repository if repository is not None else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clips')
   
    resources = None
    resources = obj['resources'] if 'resources' in obj else resources
    resources = resources if resources is not None else os.path.dirname(os.path.abspath(infileAddr))

    for template in templates:
      templateUrl = template['template']
      #print 'templateUrl = ' + templateUrl
      basename = os.path.basename(templateUrl)
      dirname = os.path.dirname(templateUrl)
      setThemes = (template['themes'] if 'themes' in template and len(template['themes']) > 0 else themes.keys())
      for key in setThemes:
        svgFile = os.path.join(repository, templateUrl)
        #print 'svgFile = ' + svgFile
        svg = SvgManager(svgFile, repository=repository, resources=resources)
        obj['theme'] = themes[key]
        svg.transform(obj)
        tmpfile = tempfile.mkstemp(suffix='.svg', prefix='' + key + '_', dir=outputdir)[1]
        print 'tmpfile = ' + tmpfile
  #      outfile = os.path.join(base, dirname, 'test_' + key + '_' + basename)
        #outfile = os.path.join(base, 'test_' + key + '_' + basename)
        svg2 = svg.saveAs(tmpfile)
        #print os.path.basename(tmpfile)
        '''
        filePng = os.path.splitext(tmpfile)[0] + '.png'
        print 'filePng = ' + filePng
        #svg2.saveAsPngA4(filePng)
        svg2.saveAsPng(filePng)
        if os.path.isfile(filePng) and os.path.isfile(tmpfile):
          os.remove(tmpfile)
        '''
        print 'tmpfile = ' + tmpfile
        fileJpg = os.path.splitext(tmpfile)[0] + '.jpg'
        print 'fileJpg = ' + fileJpg
        #svg2.saveAsJpgA4(fileJpg)
        #svg2.saveAsJpg(fileJpg)
        fileJpg = os.path.join(outputdir, fileJpg)
        svg2.previewAsJpg(fileJpg)
        if False and os.path.isfile(fileJpg) and os.path.isfile(tmpfile):
          os.remove(tmpfile)
  
#import cairosvg
#cairosvg.svg2png(url="/home/jmramoss/almacen/ORLAS/resources/orla1.svg", write_to="/home/jmramoss/almacen/ORLAS/resources/orla1.png")
#cairosvg.svg2png(url="/home/jmramoss/almacen/ORLAS/resources/clips/school.svg", write_to="/home/jmramoss/almacen/ORLAS/resources/school.png")

#/home/jmramoss/almacen/ORLAS/text2img/text2img
#print os.path.dirname(os.path.abspath(__file__))
#python -c "import sys; import svgmanager; svgmanager.SvgManager.generate(sys.argv)"
if __name__ == '__main__':
  SvgManager.generate(sys.argv)
