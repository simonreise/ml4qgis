import sys
import os
import pathlib
import shutil
import glob

import remote_sensing_processor as rsp


if __name__ == '__main__':
    tempdir = sys.argv[1].strip('"').strip("'")
    x_train = glob.glob(os.path.join(tempdir, 'x_train') + '/*')
    y_train = glob.glob(os.path.join(tempdir, 'y_train') + '/*')
    x_val = glob.glob(os.path.join(tempdir, 'x_val') + '/*')
    y_val = glob.glob(os.path.join(tempdir, 'y_val') + '/*')
    if x_val == []:
        x_val = None
    if y_val == []:
        y_val = None
    outdir = os.path.join(tempdir, 'output')
    model = sys.argv[2].strip('"').strip("'")
    backbone = sys.argv[3].strip('"').strip("'")
    inputCheckpoint = sys.argv[4].strip('"').strip("'")
    if 'None' in inputCheckpoint or inputCheckpoint == '':
        inputCheckpoint = None
    else:
        inputCheckpoint = inputCheckpoint
    inputWeights = sys.argv[5].strip('"').strip("'")
    if inputWeights == '':
        inputWeights = None
    inputEpochs = sys.argv[6]
    inputBatchSize = sys.argv[7]
    inputLessMetrics = sys.argv[8]
    inputLR = sys.argv[9]
    inputMultiprocessing = sys.argv[10]
    out_name = sys.argv[11].strip('"').strip("'")
    out_name = os.path.join(outdir, out_name)

    rsp.segmentation.train(x_train, y_train, x_val, y_val, out_name, model = model, backbone = backbone, checkpoint = inputCheckpoint, weights = inputWeights, epochs=int(inputEpochs), batch_size=int(inputBatchSize), less_metrics=bool(int(inputLessMetrics)), lr=float(inputLR), multiprocessing = bool(int(inputMultiprocessing)))