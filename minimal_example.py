import cv2
import sys
import os
from cv2 import aruco
import pickle

''' 
This script reads an image with two Aruco markers: one to identify the tree and the second one to identify the orientation.
The image file is renamed using the tree number and orientation
'''

name = 'images/test_image.jpg'

parameters =  aruco.DetectorParameters_create()

# Load custom dictionary
dict_file = 'data/CUSTOM_ARUCO_MARKERS_DICT_8x8_512.pkl'

if os.path.isfile(dict_file):
    print ('Loading existing dictionary')
    with open(dict_file, 'rb') as fd:
          cdic_serializable = pickle.load(fd)

    cdic = aruco.Dictionary_create(5,3)
    cdic.markerSize = cdic_serializable['markerSize']
    cdic.maxCorrectionBits = cdic_serializable['maxCorrectionBits']
    cdic.bytesList = cdic_serializable['bytesList']
else:
    print ('ERROR: Could not read dictionary file!')
    sys.exit()

# Read test image
ima = cv2.imread(name)
gray = cv2.cvtColor(ima, cv2.COLOR_BGR2GRAY)
h,w = ima.shape[0:2]

corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, cdic, parameters=parameters)
print ('Markers found in image: ', ids)

if ids is None or len(ids) != 2:
    print ('ERROR: Incorrect number of markers detected. Two markers should appear in the image')
    sys.exit()

ids.sort()
orientation = None
code = -1

if ids[0][0] == 0:
    orientation = 'Front'
    code = ids[1][0]
if ids[1][0] == 511:
    if orientation is not None:
        print ('ERROR: Front and Back markers detected! Only one should appear in the image')
        sys.exit()
    else:
        orientation = 'Back'
        code = ids[0][0]

print (code,orientation)

if orientation is None:
    print ('ERROR: Wrong orientation. Valid orientation codes are 0 or 511')
    sys.exit()
    
if code == -1 or code == 0 or code == 511:
    print ('ERROR: Wrong code. Valid codes are in the range [1-510]')
    sys.exit()

# Rename image 
output_name = 'Tree_{:05d}_{}.jpg'.format(code,orientation)
cv2.imwrite(output_name, ima)
