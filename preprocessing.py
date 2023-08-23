import os
from pathlib import Path
import glob
import shutil
import shlex

from qgis.core import QgsVectorFileWriter

from .setup import check, getTempdir, cleanTempdir
from .common import getInterpreter, getScript, getInputLayer, runCommand


def sentinel2(backend, inputLayer, inputSen2Cor, inputSuperRes, inputCloudMask, inputClip, outputCrs, outputDest, feedback):
    #copying archive to temp dir
    tempdir = getTempdir(feedback)
    #cleanTempdir(tempdir, feedback)
    feedback.pushInfo('Copying ' + inputLayer + ' to ' + str(tempdir))
    shutil.copy(inputLayer, tempdir)
    feedback.setProgress(int(5))
    
    #saving clipping layer to file
    if inputClip:
        feedback.pushInfo('Saving vector layer to file')
        clippath = os.path.join(tempdir, 'clip.gpkg')
        QgsVectorFileWriter.writeAsVectorFormat(inputClip, clippath, 'utf-8', driverName='GPKG')
        inputClip = 'clip.gpkg'
    else:
        inputClip = 'None'
    feedback.setProgress(int(10))
    
    #converting crs to wkt string
    if outputCrs.isValid():
        outputCrs = outputCrs.toWkt()
    else:
        outputCrs = 'None'
        
    ready, started = check(backend, feedback)
    feedback.setProgress(int(15))
    
    if ready and started:
        feedback.pushInfo('Starting Sentinel-2 preprocessing')
        interpreter = getInterpreter(backend)
        script = getScript('sentinel2.py', backend)
        inputLayer = getInputLayer(inputLayer, tempdir, backend)
        inputClip = getInputLayer(inputClip, tempdir, backend)
        
        cmd = [interpreter, '-u', script, \
            shlex.quote(inputLayer), str(int(inputSen2Cor)), \
            str(int(inputSuperRes)), str(int(inputCloudMask)), \
            shlex.quote(inputClip), shlex.quote(outputCrs)]
        runCommand(cmd, backend, interpreter, tempdir, feedback)
        feedback.setProgress(int(90))

        feedback.pushInfo('Copying result to ' + outputDest)
        resdir = glob.glob(tempdir + '/*/')[0]
        destdir = os.path.join(outputDest, Path(resdir).parts[-1])
        shutil.copytree(resdir, destdir)
        feedback.setProgress(int(95))
        
        cleanTempdir(tempdir, feedback)
    feedback.setProgress(int(100))
    
    
def landsat(backend, inputLayer, inputCloudMask, inputPansharpen, inputKeepPan, inputResampling, inputTemperature, inputClip, outputCrs, outputDest, feedback):
    #copying archive to temp dir
    tempdir = getTempdir(feedback)
    cleanTempdir(tempdir, feedback)
    feedback.pushInfo('Copying ' + inputLayer + ' to ' + str(tempdir))
    shutil.copy(inputLayer, tempdir)
    feedback.setProgress(int(5))
    
    #saving clipping layer to file
    if inputClip:
        feedback.pushInfo('Saving vector layer to file')
        clippath = os.path.join(tempdir, 'clip.gpkg')
        QgsVectorFileWriter.writeAsVectorFormat(inputClip, clippath, 'utf-8', driverName='GPKG')
        inputClip = 'clip.gpkg'
    else:
        inputClip = 'None'
    feedback.setProgress(int(10))
    
    #converting crs to wkt string
    if outputCrs.isValid():
        outputCrs = outputCrs.toWkt()
    else:
        outputCrs = 'None'
        
    ready, started = check(backend, feedback)
    feedback.setProgress(int(15))
    
    if ready and started:
        feedback.pushInfo('Starting Landsat preprocessing')
        interpreter = getInterpreter(backend)
        script = getScript('landsat.py', backend)
        inputLayer = getInputLayer(inputLayer, tempdir, backend)
        inputClip = getInputLayer(inputClip, tempdir, backend)
        
        cmd = [interpreter, '-u', script,\
                shlex.quote(inputLayer), str(int(inputCloudMask)),\
                str(int(inputPansharpen)), str(int(inputKeepPan)), \
                inputResampling, inputTemperature,  shlex.quote(inputClip), shlex.quote(outputCrs)]
        runCommand(cmd, backend, interpreter, tempdir, feedback)
        feedback.setProgress(int(90))

        feedback.pushInfo('Copying result to ' + outputDest)
        resdir = glob.glob(tempdir + '/*/')[0]
        destdir = os.path.join(outputDest, Path(resdir).parts[-1])
        shutil.copytree(resdir, destdir)
        feedback.setProgress(int(95))
        
        cleanTempdir(tempdir, feedback)
    feedback.setProgress(int(100))
    
    
def mosaic(backend, inputMultiBand, inputLayers, inputFill, inputFillDistance, inputClip, outputCrs, inputNodata, inputReference, inputResampling, inputNodataOrder, inputKeepAllChannels, outputDest, feedback):
    if inputMultiBand:
        #replacing file names with folder names
        folders = []
        for layer in inputLayers:
            folders.append(os.path.dirname(layer))
        folders = list(set(folders))
        inputLayers = folders
    else:
        #getting file names
        folders = []
        for layer in inputLayers:
            folders.append(layer)
        folders = list(set(folders))
        inputLayers = folders
    
    #copying data to temp dir
    tempdir = getTempdir(feedback)
    cleanTempdir(tempdir, feedback)
    feedback.pushInfo('Copying data to ' + str(tempdir))
    os.mkdir(os.path.join(tempdir, 'input'))
    for i in inputLayers:
        if inputMultiBand:
            shutil.copytree(i, os.path.join(tempdir, 'input', Path(i).parts[-1]))
        else:
            shutil.copy(i, os.path.join(tempdir, 'input'))
    feedback.setProgress(int(5))
    
    if inputReference:
        shutil.copy(inputReference, tempdir)
        inputReference = getInputLayer(inputReference, tempdir, backend)
    else:
        inputReference = 'None'
    
    #saving clipping layer to file
    if inputClip:
        feedback.pushInfo('Saving vector layer to file')
        clippath = os.path.join(tempdir, 'clip.gpkg')
        QgsVectorFileWriter.writeAsVectorFormat(inputClip, clippath, 'utf-8', driverName='GPKG')
        inputClip = 'clip.gpkg'
    else:
        inputClip = 'None'
    feedback.setProgress(int(10))
    
    #converting crs to wkt string
    if outputCrs.isValid():
        outputCrs = outputCrs.toWkt()
    else:
        outputCrs = 'None'
    
    #creating output folder
    os.mkdir(os.path.join(tempdir, 'output'))
    
    ready, started = check(backend, feedback)
    feedback.setProgress(int(15))
    
    if ready and started:
        feedback.pushInfo('Starting rasters merge')
        interpreter = getInterpreter(backend)
        script = getScript('mosaic.py', backend)
        inputClip = getInputLayer(inputClip, tempdir, backend)
        if backend == 'docker':
            td = '/mnt/temp/'
        else:
            td = tempdir
        
        cmd = [interpreter, '-u', script, \
                shlex.quote(td), str(int(inputFill)), str(int(inputFillDistance)), \
                str(inputNodata), shlex.quote(inputReference), inputResampling, \
                str(int(inputNodataOrder)), str(int(inputKeepAllChannels)),  shlex.quote(inputClip), \
                shlex.quote(outputCrs)]
        runCommand(cmd, backend, interpreter, tempdir, feedback)
        feedback.setProgress(int(90))

        feedback.pushInfo('Copying result to ' + outputDest)
        results = glob.glob(os.path.join(tempdir, 'output') + '/*.tif')
        for result in results:
            shutil.copy(result, outputDest)
        feedback.setProgress(int(95))
        
        cleanTempdir(tempdir, feedback)
    feedback.setProgress(int(100))
    
    
def normalize(backend, inputLayer, inputMin, inputMax, outputDest, feedback):
    #copying files to temp dir
    tempdir = getTempdir(feedback)
    cleanTempdir(tempdir, feedback)
    feedback.pushInfo('Copying ' + inputLayer + ' to ' + str(tempdir))
    shutil.copy(inputLayer, tempdir)
    feedback.setProgress(int(5))
        
    ready, started = check(backend, feedback)
    feedback.setProgress(int(15))
    
    if ready and started:
        feedback.pushInfo('Starting rasters min/max normalization')
        interpreter = getInterpreter(backend)
        script = getScript('normalize.py', backend)
        inputLayer = getInputLayer(inputLayer, tempdir, backend)
        outputLayer = getInputLayer(outputDest, tempdir, backend)
        
        cmd = [interpreter, '-u', script,\
                shlex.quote(inputLayer), str(inputMin), str(inputMax), shlex.quote(outputLayer)]
        runCommand(cmd, backend, interpreter, tempdir, feedback)
        feedback.setProgress(int(90))

        feedback.pushInfo('Copying result to ' + outputDest)
        result = os.path.join(tempdir, os.path.basename(outputDest))
        shutil.copy(result, os.path.dirname(outputDest))
        feedback.setProgress(int(95))
        
        cleanTempdir(tempdir, feedback)
    feedback.setProgress(int(100))   
 