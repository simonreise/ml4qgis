import os
from pathlib import Path
import glob
import shutil
import shlex

from qgis.core import QgsVectorFileWriter

from .setup import check, getTempdir, cleanTempdir
from .common import getInterpreter, getScript, getInputLayer, runCommand


def seg_generate_tiles(backend, inputX, inputY, inputTileSize, inputClassification, inputShuffle, inputTrainSize, inputValSize, inputTestSize, inputXNodata, inputYNodata, inputXDtype, inputYDtype, outputDest, feedback):
    #copying data to temp dir
    tempdir = getTempdir(feedback)
    cleanTempdir(tempdir, feedback)
    feedback.pushInfo('Copying data to ' + str(tempdir))
    os.mkdir(os.path.join(tempdir, 'x'))
    for i in inputX:
        shutil.copy(i, os.path.join(tempdir, 'x'))
    feedback.setProgress(int(5))
    
    shutil.copy(inputY, tempdir)
    inputY = getInputLayer(inputY, tempdir, backend)
    feedback.setProgress(int(10))
    
    #creating output folder
    os.mkdir(os.path.join(tempdir, 'output'))
    
    ready, started = check(backend, feedback)
    feedback.setProgress(int(15))
    
    if ready and started:
        feedback.pushInfo('Starting tiles generation')
        interpreter = getInterpreter(backend)
        script = getScript('seg_generate_tiles.py', backend)
        if backend == 'docker':
            td = '/mnt/temp/'
        else:
            td = tempdir
        
        cmd = [interpreter, '-u', script, \
                shlex.quote(td), shlex.quote(inputY), str(inputTileSize), str(int(inputClassification)), \
                str(int(inputShuffle)),  str(inputTrainSize), str(inputValSize), str(inputTestSize),\
                str(inputXNodata), str(inputYNodata), str(inputXDtype), str(inputYDtype)]
        runCommand(cmd, backend, interpreter, tempdir, feedback)
        feedback.setProgress(int(90))

        feedback.pushInfo('Copying result to ' + outputDest)
        results = glob.glob(os.path.join(tempdir, 'output') + '/*')
        for result in results:
            shutil.copy(result, outputDest)
        feedback.setProgress(int(95))
        
        cleanTempdir(tempdir, feedback)
    feedback.setProgress(int(100))
    
    
def seg_train(backend, inputXTrain, inputYTrain, inputXVal, inputYVal, model, backbone, inputCheckpoint, inputWeights, inputEpochs, inputBatchSize, inputLessMetrics, inputLR, inputMultiprocessing, outputDest, feedback):
    #copying data to temp dir
    tempdir = getTempdir(feedback)
    cleanTempdir(tempdir, feedback)
    feedback.pushInfo('Copying data to ' + str(tempdir))
    os.mkdir(os.path.join(tempdir, 'x_train'))
    for i in inputXTrain:
        shutil.copy(i, os.path.join(tempdir, 'x_train'))
    os.mkdir(os.path.join(tempdir, 'y_train'))
    for i in inputYTrain:
        shutil.copy(i, os.path.join(tempdir, 'y_train'))
    os.mkdir(os.path.join(tempdir, 'x_val'))
    if not inputXVal == ['']:
        for i in inputXVal:
            shutil.copy(i, os.path.join(tempdir, 'x_val'))
    os.mkdir(os.path.join(tempdir, 'y_val'))
    if not inputYVal == ['']:
        for i in inputYVal:
            shutil.copy(i, os.path.join(tempdir, 'y_val'))
    
    if inputCheckpoint is not None and inputCheckpoint != '':
        shutil.copy(inputCheckpoint, tempdir)
        inputCheckpoint = getInputLayer(inputCheckpoint, tempdir, backend)
    feedback.setProgress(int(10))

    #creating output folder
    os.mkdir(os.path.join(tempdir, 'output'))
    out_name = os.path.basename(outputDest)
    
    ready, started = check(backend, feedback)
    feedback.setProgress(int(15))
    
    if ready and started:
        feedback.pushInfo('Starting model training')
        interpreter = getInterpreter(backend)
        script = getScript('seg_train.py', backend)
        if backend == 'docker':
            td = '/mnt/temp/'
        else:
            td = tempdir
        
        cmd = [interpreter, '-u', script, \
                shlex.quote(td), str(model), str(backbone), shlex.quote(str(inputCheckpoint)), \
                shlex.quote(str(inputWeights)), str(inputEpochs), str(inputBatchSize), \
                str(int(inputLessMetrics)), str(inputLR), str(int(inputMultiprocessing)), \
                shlex.quote(str(out_name))]
        runCommand(cmd, backend, interpreter, tempdir, feedback)
        feedback.setProgress(int(90))

        feedback.pushInfo('Copying result to ' + outputDest)
        shutil.copytree(os.path.join(tempdir, 'output'), os.path.dirname(outputDest), dirs_exist_ok = True)
        feedback.setProgress(int(95))
        
        cleanTempdir(tempdir, feedback)
    feedback.setProgress(int(100))


def seg_test(backend, inputXTest, inputYTest, inputModel, inputBatchSize, inputMultiprocessing, feedback):
    #copying data to temp dir
    tempdir = getTempdir(feedback)
    cleanTempdir(tempdir, feedback)
    feedback.pushInfo('Copying data to ' + str(tempdir))
    os.mkdir(os.path.join(tempdir, 'x_test'))
    for i in inputXTest:
        shutil.copy(i, os.path.join(tempdir, 'x_test'))
    os.mkdir(os.path.join(tempdir, 'y_test'))
    for i in inputYTest:
        shutil.copy(i, os.path.join(tempdir, 'y_test'))
    shutil.copy(inputModel, tempdir)
    inputModel = getInputLayer(inputModel, tempdir, backend)
    feedback.setProgress(int(10))
    
    ready, started = check(backend, feedback)
    feedback.setProgress(int(15))
    
    if ready and started:
        feedback.pushInfo('Starting model testing')
        interpreter = getInterpreter(backend)
        script = getScript('seg_test.py', backend)
        if backend == 'docker':
            td = '/mnt/temp/'
        else:
            td = tempdir
        
        cmd = [interpreter, '-u', script, \
                shlex.quote(td),  shlex.quote(str(inputModel)), str(inputBatchSize), \
                str(int(inputMultiprocessing)) ]
        runCommand(cmd, backend, interpreter, tempdir, feedback)
        feedback.setProgress(int(90))
        
        cleanTempdir(tempdir, feedback)
    feedback.setProgress(int(100))
    

def seg_map(backend, inputLayers, inputReference, inputModel, inputSamplesFile, inputBatchSize, inputNodata, inputMultiprocessing, outputDest, feedback):
    #copying data to temp dir
    tempdir = getTempdir(feedback)
    cleanTempdir(tempdir, feedback)
    feedback.pushInfo('Copying data to ' + str(tempdir))
    layers = []
    for i in inputLayers:
        shutil.copy(i, tempdir)
        layers.append(getInputLayer(i, tempdir, backend))
    shutil.copy(inputReference, tempdir)
    inputReference = getInputLayer(inputReference, tempdir, backend)
    shutil.copy(inputModel, tempdir)
    inputModel = getInputLayer(inputModel, tempdir, backend)
    shutil.copy(inputSamplesFile, tempdir)
    inputSamplesFile = getInputLayer(inputSamplesFile, tempdir, backend)
    outfile = getInputLayer(outputDest, tempdir, backend)
    feedback.setProgress(int(10))
    
    ready, started = check(backend, feedback)
    feedback.setProgress(int(15))
    
    if ready and started:
        feedback.pushInfo('Starting model training')
        interpreter = getInterpreter(backend)
        script = getScript('seg_map.py', backend)
        
        cmd = [interpreter, '-u', script, \
                shlex.quote(inputReference), shlex.quote(inputModel), shlex.quote(inputSamplesFile), \
                str(inputNodata), str(inputBatchSize), str(int(inputMultiprocessing)), \
                shlex.quote(str(outfile))] + [shlex.quote(str(i)) for i in layers]
        runCommand(cmd, backend, interpreter, tempdir, feedback)
        feedback.setProgress(int(90))

        feedback.pushInfo('Copying result to ' + outputDest)
        shutil.copy(outfile, os.path.dirname(outputDest))
        feedback.setProgress(int(95))
        
        cleanTempdir(tempdir, feedback)
    feedback.setProgress(int(100))