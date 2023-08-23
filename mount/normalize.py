import sys
import os
import pathlib
import glob
import shutil

import remote_sensing_processor as rsp


inputLayer = sys.argv[1].strip('"').strip("'")
#inputLayer = os.path.join('/mnt/temp', inputLayer)
inputMin = sys.argv[2]
if inputMin == 'None' or inputMin == None:
    inputMin = None
else:
    inputMin = float(inputMin)
inputMax = sys.argv[3]
if inputMax == 'None' or inputMax == None:
    inputMax = None
else:
    inputMax = float(inputMax)
outputLayer = sys.argv[4].strip('"').strip("'")

rsp.normalize(inputLayer, outputLayer, minimum = inputMin, maximum = inputMax)