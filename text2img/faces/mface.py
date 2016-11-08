#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://scikit-image.org/docs/dev/auto_examples/edges/plot_active_contours.html#sphx-glr-auto-examples-edges-plot-active-contours-py

import numpy as np
import cv2
import sys

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face2_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
profile_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

arg1=1.3
arg2=5

srcImg = 'example1.jpg'
srcImg = sys.argv[1] if len(sys.argv) > 1 else srcImg

img = cv2.imread(srcImg)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('img',gray)
faces = face_cascade.detectMultiScale(gray, arg1, arg2)
for (x,y,w,h) in faces:
    print 'Face : (' + str(x) + ', ' + str(y) + ') - (' + str(x+w) + ', ' + str(y+h) + ')'
    print 'Size: (' + str(w) + ', ' + str(h) + ')'
    incx = int(0.65*((w+h)/2.0)/2.0)
    incy = int(0.85*((w+h)/2.0)/2.0)
    cv2.rectangle(img,(x-incx,y-incy),(x+w+incx,y+h+incy),(255,0,0),2)
    #roi_gray = gray[y:y+h, x:x+w]
    #roi_color = img[y:y+h, x:x+w]

#eyes = eye_cascade.detectMultiScale(gray, arg1, arg2)
#for (ex,ey,ew,eh) in eyes:
#    print 'Eyes : (' + str(ex) + ', ' + str(ey) + ') - (' + str(ex+ew) + ', ' + str(ey+eh) + ')'
#    cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

faces = profile_cascade.detectMultiScale(gray, arg1, arg2)
for (x,y,w,h) in faces:
    print 'Profile : (' + str(x) + ', ' + str(y) + ') - (' + str(x+w) + ', ' + str(y+h) + ')'
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

faces = face2_cascade.detectMultiScale(gray, arg1, arg2)
for (x,y,w,h) in faces:
    print 'Face2 : (' + str(x) + ', ' + str(y) + ') - (' + str(x+w) + ', ' + str(y+h) + ')'
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)


cv2.imwrite('messigray.png',img)

#cv2.imshow('img',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

