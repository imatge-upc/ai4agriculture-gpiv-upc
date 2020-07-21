"""
Usage:
  create_dictionary.py <outDir> [--dictBase=<db>] [--markerSize=<ms>] [--numCodes=<nc>] 
  create_dictionary.py -h | --help
Options:
  --dictBase=<db>            Base name for marker dictionary [default: CUSTOM_ARUCO_MARKERS_DICT]
  --markerSize=<ms>          Marker size [default: 7]
  --numCodes=<nc>            Number of codes [default: 4096]
"""

import sys
import os
import cv2
from cv2 import aruco
from docopt import docopt
import pickle


if __name__ == '__main__':
    # read args
    args = docopt(__doc__)
    out_dir = args['<outDir>']
    
    dict_base  = args['--dictBase']
    marker_size = int(args['--markerSize'])
    num_codes   = int(args['--numCodes'])

    dict_file = '{od}/{dict_base}_{ms}x{ms}_{nm}.pkl'.format(od = out_dir, dict_base=dict_base, ms=marker_size, nm = num_codes)
    
    print ('Creating new dictionary: {}'.format(dict_file))
    cdic = aruco.Dictionary_create(num_codes, marker_size)
        
    cdic_serializable = {}
    cdic_serializable['markerSize']=cdic.markerSize
    cdic_serializable['maxCorrectionBits'] = cdic.maxCorrectionBits
    cdic_serializable['bytesList'] = cdic.bytesList
    
    with open(dict_file, 'wb') as fd:
        print ('Saving dictionary as: {}'.format(dict_file))
        pickle.dump(cdic_serializable, fd)

