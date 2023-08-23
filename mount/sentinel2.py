import sys
import os
import pathlib
import glob
import shutil

import remote_sensing_processor as rsp


inputLayer = sys.argv[1].strip('"').strip("'")
#inputLayer = os.path.join('/mnt/temp', inputLayer)
inputSen2Cor = sys.argv[2]
inputSuperRes = sys.argv[3]
inputCloudMask = sys.argv[4]
inputClip = sys.argv[5].strip('"').strip("'")
if 'None' in inputClip:
    inputClip = None
else:
    inputClip = inputClip
outputCrs = sys.argv[6].strip('"').strip("'")
if outputCrs == '"None"' or outputCrs == 'None' or outputCrs == "'None'":
    outputCrs = None

rsp.sentinel2(inputLayer, sen2cor = bool(int(inputSen2Cor)), superres = bool(int(inputSuperRes)), projection = outputCrs, cloud_mask = bool(int(inputCloudMask)), clipper = inputClip)