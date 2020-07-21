

import cv2
import os
import sys
from docopt import docopt
import numpy as np
from fpdf import FPDF


codes_dir             = 'data/codes_8x8_512'
out_dir               = 'data/codes_8x8_512'

dict_name             = 'CUSTOM_ARUCO_MARKERS_DICT_8x8_512'
num_codes             = 512
code_width_in_cm      = 8
border_in_cm          = 1

codes_per_page_width  = 2
codes_per_page_height = 2

pixels_per_cm         = 118.11  # Equivalent to 300 ppi

codes_per_page = codes_per_page_width * codes_per_page_height

border_pixels = int(round(pixels_per_cm * border_in_cm))
code_pixels   = int(round(code_width_in_cm * pixels_per_cm))
total_pixels  = code_pixels + 2 * border_pixels

codes_page_ima = np.zeros((codes_per_page_height * total_pixels, codes_per_page_width * total_pixels), dtype=np.uint8)
codes_page_ima.fill(255)

page_counter = 0

for ii in range(num_codes):
    
    code_file_name = '{}/{}_code_{:05d}.png'.format(codes_dir, dict_name, ii)
    code_ima = cv2.imread(code_file_name, 0)

    pos_x = ii  %  codes_per_page_width
    pos_y = (ii // codes_per_page_width) % codes_per_page_height
    
    pos_x_pix = pos_x * total_pixels + border_pixels
    pos_y_pix = pos_y * total_pixels + border_pixels

    codes_page_ima[pos_y_pix:pos_y_pix + code_pixels, pos_x_pix:pos_x_pix + code_pixels] = code_ima

    if ii == 0:
        code_str = 'Front'
    elif ii == 511:
        code_str = 'Back'
    else:
        code_str = str(ii)
    
    cv2.putText(codes_page_ima, code_str, (pos_x_pix+code_pixels//2 - 10, pos_y_pix+code_pixels + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)

    print (ii, pos_y, pos_x)
    
    if (ii+1) % codes_per_page == 0:
        page_name_jpg = '{}/{}_codes_page_{:04d}.png'.format(out_dir, dict_name, page_counter)
        cv2.imwrite(page_name_jpg, codes_page_ima)

        page_counter = page_counter + 1
        codes_page_ima.fill(255)

        page_name_pdf = '{}/{}_codes_page_{:04d}.pdf'.format(out_dir, dict_name, page_counter)
        pdf = FPDF('P','mm','A4')
        pdf.add_page()
        pdf.image(page_name_jpg,5,5,200,200)
        pdf.output(page_name_pdf)
        
