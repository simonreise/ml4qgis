import sys
import os
import pathlib
import shutil
import glob

import remote_sensing_processor as rsp


if __name__ == '__main__':
    inputReference = sys.argv[1].strip('"').strip("'")
    inputModel = sys.argv[2].strip('"').strip("'")
    inputSamplesFile = sys.argv[3].strip('"').strip("'")
    inputNodata = sys.argv[4]
    if inputNodata == 'None' or inputNodata == None:
        inputNodata = None
    else:
        inputNodata = int(inputNodata)
    inputBatchSize = sys.argv[5]
    if inputBatchSize == 'None' or inputBatchSize == None:
        inputBatchSize = None
    else:
        inputBatchSize = int(inputBatchSize)
    inputMultiprocessing = bool(int(sys.argv[6]))
    outputDest = sys.argv[7].strip('"').strip("'")
    layers = [i.strip('"').strip("'") for i in sys.argv[7:]]

    rsp.segmentation.generate_map(layers, inputReference, inputModel, outputDest, samples_file = inputSamplesFile, nodata = inputNodata, batch_size = inputBatchSize, multiprocessing = inputMultiprocessing)