# ai4agriculture-gpiv-upc


This repository helps to identify vine-trees in a vineyard. Each marker encodes a number in the range  [0-512). By placing 
a marker in front of each tree, the tree gets identified by the corresponding code. Markers with codes 0 (Front) and 511 (Back) 
are reserved to determine the two sides of the vine trees.

The process is as follows: print each marker code [1-510] in data/codes_8x8_512 (the .png files) so that each code is 8x8 cm 
with a white border of at least 1 cm around the marker. For convenience, a set of pdf files with four markers each 
are provided as well in the same folder. Cut each marker and glue it over a cardboard piece (or similar) for stiffness. 
Glue this piece with the code at the top of a pole. All poles must have the same height and should have a mark at 20cm 
from the bottom to indicate the amount of the pole that will be buried on the ground. The goal is that all markers should be 
at the same height once installed. 

Place a pole with a marker in front of each tree, taking care so that the leaves do not occlude any part of the marker. 
Place a marker (code 0 or 511) flat on the ground next to the pole to indicate the tree side (Front or Back). The vertical
distance between the markers should be constant for all trees.

