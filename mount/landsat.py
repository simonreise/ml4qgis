import sys
import os
import pathlib
import shutil

import remote_sensing_processor as rsp

inputLayer = sys.argv[1].strip('"').strip("'")
#inputLayer = os.path.join('/mnt/temp', inputLayer)
inputCloudMask = sys.argv[2]
inputPansharpen = sys.argv[3]
inputKeepPan = sys.argv[4]
inputResampling = sys.argv[5]
if inputResampling == 'None':
    inputResampling = 'bilinear'
inputTemperature = sys.argv[6]
if inputTemperature == 'None':
    inputTemperature = 'k'
inputClip = sys.argv[7].strip('"').strip("'")
if 'None' in inputClip:
    inputClip = None
else:
    inputClip = inputClip
outputCrs = sys.argv[8].strip('"').strip("'")
if outputCrs == '"None"' or outputCrs == 'None' or outputCrs == "'None'":
    outputCrs = None

rsp.landsat(inputLayer, pansharpen = bool(int(inputPansharpen)), keep_pan_band = bool(int(inputKeepPan)), projection = outputCrs, cloud_mask = bool(int(inputCloudMask)), clipper = inputClip, resample = inputResampling, t = inputTemperature)