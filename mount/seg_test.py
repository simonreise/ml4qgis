import sys
import os
import pathlib
import shutil
import glob

import remote_sensing_processor as rsp


if __name__ == '__main__':
    tempdir = sys.argv[1].strip('"').strip("'")
    x_test = glob.glob(os.path.join(tempdir, 'x_test') + '/*')
    y_test = glob.glob(os.path.join(tempdir, 'y_test') + '/*')
    inputModel = sys.argv[2].strip('"').strip("'")
    inputBatchSize = sys.argv[3]
    inputMultiprocessing = sys.argv[4]


    rsp.segmentation.test(x_test, y_test, model = inputModel, batch_size=int(inputBatchSize), multiprocessing = bool(int(inputMultiprocessing)))