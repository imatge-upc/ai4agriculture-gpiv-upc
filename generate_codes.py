"""
Usage:
  generate_codes.py <dataDir> [--dictBase=<db>] [--markerSize=<ms>] [--numCodes=<nc>] [--numMarkers=<nm>] [--outDir=<od>]
  generate_codes.py -h | --help
  -----------------------------
  This script reads am ARUCO dictionary in 'dataDir' and creates images for various marker ids. 
  The markers ids are generated randomly
Options:
  --dictBase=<db>            Base name for marker dictionary [default: CUSTOM_ARUCO_MARKERS_DICT]
  --markerSize=<ms>          Marker size [default: 7]
  --numCodes=<nc>            Number of codes [default: 4096]
  --numMarkers=<nm>          Number of markers to generate [default: 10]
  --outDir=<od>              Output directory [default: .]
"""

import cv2
from cv2 import aruco
import os
import sys
from docopt import docopt
import random
import pickle
import numpy as np


if __name__ == '__main__':
    # read args
    args = docopt(__doc__)

    data_dir    = args['<dataDir>']
    dict_base   = args['--dictBase']

    marker_size = int(args['--markerSize'])
    num_codes   = int(args['--numCodes'])
    num_markers = int(args['--numMarkers'])
    out_dir     = args['--outDir']

    dict_file = '{dd}/{dict_base}_{ms}x{ms}_{nc}.pkl'.format(dd=data_dir, dict_base=dict_base, ms=marker_size, nc = num_codes)


    if os.path.isfile(dict_file):
        print ('Loading existing dictionary: {}'.format(dict_file))
        with open(dict_file, 'rb') as fd:
            cdic_serializable = pickle.load(fd)

            cdic = aruco.Dictionary_create(5,3) # Create a small (i.e. fast) marker dictionary because I do not know how to create an empty dict.
            cdic.markerSize = cdic_serializable['markerSize']
            cdic.maxCorrectionBits = cdic_serializable['maxCorrectionBits']
            cdic.bytesList = cdic_serializable['bytesList']
    else:
        print ('Dictionary file {} not found'.format(dict_file))
        sys.exit()
        
    #list_codes = [1, 100, 1000, 1965, 2001, 2019, 3003, 4004] # Change at will
    #list_codes = [4057, 3883,2883, 1711, 812, 351, 1, 0] # Change at will
    list_codes = np.random.randint(low = 0, high = num_codes - 1, size = num_markers) 

    marker_size_in_cm  = 8
    resolution_inch_cm = 300
    num_pixels = int(round((marker_size_in_cm / 2.54) * resolution_inch_cm))
    print ('Num pixels : ', num_pixels)
    
    #for code in list_codes:
    for code in range(0,num_markers):
        img = aruco.drawMarker(cdic, code, num_pixels)
        code_name = '{od}/{dict_base}_{ms}x{ms}_{nm}_code_{cn:05d}.png'.format(od=out_dir, dict_base=dict_base, ms=marker_size, nm = num_codes, cn=code)
        cv2.imwrite(code_name, img)
