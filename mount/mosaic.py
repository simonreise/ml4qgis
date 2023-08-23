import sys
import os
import pathlib
import shutil
import glob

import remote_sensing_processor as rsp


tempdir = sys.argv[1].strip('"').strip("'")
indir = os.path.join(tempdir, 'input')
inputLayers = glob.glob(indir + '/*')
outdir = os.path.join(tempdir, 'output')
#inputLayers = sys.argv[1]
#layers = inputLayers.strip("[]'").strip('"').split(',')
#inputLayers = []
#for i in layers:
#    inputLayers.append(i.strip('" ').strip("'"))
#inputLayer = os.path.join('/mnt/temp', inputLayer)
inputFill = sys.argv[2]
inputFillDistance = sys.argv[3]
if inputFillDistance == 'None' or inputFillDistance == None:
    inputFillDistance = None
else:
    inputFillDistance = int(inputFillDistance)
inputNodata = sys.argv[4]
if inputNodata == 'None' or inputNodata == None:
    inputNodata = None
else:
    inputNodata = int(inputNodata)
inputReference = sys.argv[5].strip('"').strip("'")
if 'None' in inputReference:
    inputReference = None
else:
    inputReference = inputReference
inputResampling = sys.argv[6]
if inputResampling == 'None':
    inputResampling = 'average'
inputNodataOrder = sys.argv[7]
inputKeepAllChannels = sys.argv[8]
inputClip = sys.argv[9].strip('"').strip("'")
if 'None' in inputClip:
    inputClip = None
else:
    inputClip = inputClip
outputCrs = sys.argv[10].strip('"').strip("'")
if outputCrs == '"None"' or outputCrs == 'None' or outputCrs == "'None'":
    outputCrs = None

rsp.mosaic(inputLayers, outdir, fill_nodata = bool(int(inputFill)), fill_distance = inputFillDistance, clipper = inputClip, nodata = inputNodata, reference_raster = inputReference, nodata_order = bool(int(inputNodataOrder)), keep_all_channels = bool(int(inputKeepAllChannels)), crs = outputCrs, resample = inputResampling)