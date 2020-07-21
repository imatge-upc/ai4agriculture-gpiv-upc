import cv2
from cv2 import aruco
import matplotlib.pyplot as plt
import pickle
import glob
import os


# Directory of the images with markers
images_dir = 'images/vineyard_test2'

# Directory with the ARUCO dictionary
data_dir = 'data'
dict_file = '{}/CUSTOM_ARUCO_MARKERS_DICT_8x8_512.pkl'.format(data_dir)

parameters =  aruco.DetectorParameters_create()


if os.path.isfile(dict_file):
    print ('Loading existing dictionary')
    with open(dict_file, 'rb') as fd:
          cdic_serializable = pickle.load(fd)

    cdic = aruco.Dictionary_create(5,3)
    cdic.markerSize = cdic_serializable['markerSize']
    cdic.maxCorrectionBits = cdic_serializable['maxCorrectionBits']
    cdic.bytesList = cdic_serializable['bytesList']
else:
    print ('creating new dictionary')
    cdic = aruco.Dictionary_create(512, 8)

    cdic_serializable = {}
    cdic_serializable['markerSize']=cdic.markerSize
    cdic_serializable['maxCorrectionBits'] = cdic.maxCorrectionBits
    cdic_serializable['bytesList'] = cdic.bytesList
    
    with open(dict_file, 'wb') as fd:
          pickle.dump(cdic_serializable, fd)


# List with all images to process
images_list = sorted(glob.glob('{}/*.jpg'.format(images_dir)))


for name in images_list:

    print (name)
    ima = cv2.imread(name)
    gray = cv2.cvtColor(ima, cv2.COLOR_BGR2GRAY)
    h,w = ima.shape[0:2]


    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, cdic, parameters=parameters)
    #rvec, tvec,_ = aruco.estimatePoseSingleMarkers(corners[0], 0.08, mtx, dist)

    print (ids)
    
    frame_markers = aruco.drawDetectedMarkers(ima, corners, ids)

    if ids is not None:
        for ii,id in enumerate(ids):
            print (id,frame_markers.shape)

            frame_markers = cv2.putText(frame_markers, str(id), (w-500, 130+ii*130), cv2.FONT_HERSHEY_SIMPLEX, 4, (0,0,255), 12)

    cv2.imwrite('{}_out.jpg'.format(os.path.splitext(name)[0]), frame_markers)
    cv2.imshow(str(id), cv2.resize(frame_markers,(w//4,h//4)))
    if cv2.waitKey() == 27: # ESC hit                                                                                                
        break
    cv2.destroyWindow(str(id))


