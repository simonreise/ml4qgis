import sys
import os
import pathlib
import shutil
import glob

import remote_sensing_processor as rsp


tempdir = sys.argv[1].strip('"').strip("'")
xdir = os.path.join(tempdir, 'x')
inputLayers = glob.glob(xdir + '/*')
outdir = os.path.join(tempdir, 'output')
samples_file = os.path.join(outdir, 'samples.pickle')
xouts = [os.path.join(outdir, 'x_train.h5'), os.path.join(outdir, 'x_val.h5'), os.path.join(outdir, 'x_test.h5')]
youts = [os.path.join(outdir, 'y_train.h5'), os.path.join(outdir, 'y_val.h5'), os.path.join(outdir, 'y_test.h5')]
inputY = sys.argv[2].strip('"').strip("'")
inputTileSize = sys.argv[3]
inputClassification = sys.argv[4]
inputShuffle = sys.argv[5]
inputTrainSize = sys.argv[6]
if inputTrainSize == 'None' or inputTrainSize == None:
    inputTrainSize = 3
else:
    inputTrainSize = int(inputTrainSize)
inputValSize = sys.argv[7]
if inputValSize == 'None' or inputValSize == None:
    inputValSize = 1
else:
    inputValSize = int(inputValSize)
inputTestSize = sys.argv[8]
if inputTestSize == 'None' or inputTestSize == None:
    inputTestSize = 1
else:
    inputTestSize = int(inputTestSize)
inputXNodata = sys.argv[9]
if inputXNodata == 'None' or inputXNodata == None:
    inputXNodata = None
else:
    inputXNodata = int(inputXNodata)
inputYNodata = sys.argv[10]
if inputYNodata == 'None' or inputYNodata == None:
    inputYNodata = None
else:
    inputYNodata = int(inputYNodata)
inputXDtype = sys.argv[11]
if inputXDtype == 'None' or inputXDtype == None:
    inputXDtype = None
else:
    inputXDtype = inputXDtype
inputYDtype = sys.argv[12]
if inputYDtype == 'None' or inputYDtype == None:
    inputYDtype = None
else:
    inputYDtype = inputYDtype

rsp.segmentation.generate_tiles(inputLayers, inputY, tile_size=int(inputTileSize), classification=bool(int(inputClassification)), shuffle=bool(int(inputShuffle)), samples_file=samples_file, split=[inputTrainSize, inputValSize, inputTestSize], x_outputs=xouts, y_outputs=youts, x_dtype=inputXDtype, y_dtype=inputYDtype, x_nodata=inputXNodata, y_nodata=inputYNodata)