import os
from pathlib import Path
import glob
import shutil
import json
import subprocess

from .common import getInterpreter, getEnv
from .docker import from_env
from .docker.types import DeviceRequest


def check(backend, feedback):
    if backend == 'python':
        ready, started = pythoncheck(feedback)
    elif backend == 'conda':
        ready, started = condacheck(feedback)
    elif backend == 'docker':
        ready, started = dockercheck(feedback)
    else:
        ready, started = False, False
    return ready, started


def pythoncheck(feedback):
    feedback.pushInfo('Checking if python config is valid')
    interpreter = getInterpreter('python')
    scriptsdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mount')
    cmd = interpreter + ' ' + str(os.path.join(scriptsdir, 'rsp_check.py'))
    my_env = getEnv(interpreter)
    try:
        result = subprocess.run(cmd, capture_output=True, shell=True, env=my_env)
        if 'True' in result.stdout.decode():
            feedback.pushInfo('Python venv is ready')
            ready = True
            started = True
            feedback.pushInfo('Checking if system supports CUDA')
            cmd = interpreter + ' ' + str(os.path.join(scriptsdir, 'gpu_check.py'))
            try:
                result = subprocess.run(cmd, capture_output=True, shell=True, env=my_env)
                if 'True' in result.stdout.decode():
                    feedback.pushInfo("Found CUDA compatible GPU")
                else:
                    feedback.pushWarning('No GPU found. Several scripts can run very slow')
            except:
                feedback.pushWarning("Wrong venv directory or RSP is not installed in the specified env")
                ready = False
                started = False
        else:
            feedback.pushWarning("Wrong venv directory or RSP is not installed in the specified env")
            ready = False
            started = False
    except:
        feedback.pushWarning("Wrong venv directory or RSP is not installed in the specified env")
        ready = False
        started = False
    return ready, started
    
    
    
def python_install(path, feedback):
    pythonconfig = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'python.json')
    with open(pythonconfig, 'r') as f:
        data = json.load(f)
    databackup = data.copy()
    data['path'] = str(path)
    with open(pythonconfig, 'w') as f:
        json.dump(data, f)
    ready, started = check('python', feedback)
    if not ready:
        feedback.pushWarning('Python setup not working. Restoring previous setup')
        with open(pythonconfig, 'w') as f:
            json.dump(databackup, f)
    

def condacheck(feedback):
    feedback.pushInfo('Checking if conda config is valid')
    interpreter = getInterpreter('conda')
    scriptsdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mount')
    cmd = interpreter + ' ' + str(os.path.join(scriptsdir, 'rsp_check.py'))
    my_env = getEnv(interpreter)
    try:
        result = subprocess.run(cmd, capture_output=True, shell=True, env=my_env)
        if 'True' in result.stdout.decode():
            feedback.pushInfo('Conda is ready')
            ready = True
            started = True
            feedback.pushInfo('Checking if system supports CUDA')
            cmd = cmd + ' ' + str(os.path.join(scriptsdir, 'gpu_check.py'))
            try:
                result = subprocess.run(cmd, capture_output=True, shell=True, env=my_env)
                if 'True' in result.stdout.decode():
                    feedback.pushInfo("Found CUDA compatible GPU")
                else:
                    feedback.pushWarning('No GPU found. Several scripts can run very slow')
            except:
                feedback.pushWarning("Conda is not in the specified directory or RSP is not installed in the specified env")
                ready = False
                started = False
        else:
            feedback.pushWarning("Conda is not in the specified directory or RSP is not installed in the specified env")
            ready = False
            started = False
    except:
        feedback.pushWarning("Conda is not in the specified directory or RSP is not installed in the specified env")
        ready = False
        started = False
    return ready, started
    
    
    
def conda_install(path, env, feedback):
    condaconfig = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conda.json')
    with open(condaconfig, 'r') as f:
        data = json.load(f)
    databackup = data.copy()
    data['path'] = str(path)
    data['env'] = str(env)
    with open(condaconfig, 'w') as f:
        json.dump(data, f)
    ready, started = check('conda', feedback)
    if not ready:
        feedback.pushWarning('Conda setup not working. Restoring previous setup')
        with open(condaconfig, 'w') as f:
            json.dump(databackup, f)
    
    
def dockercheck(feedback):
    try:
        feedback.pushInfo('Checking if docker is installed and started')
        client = from_env()
        started = True
    except Exception as e:
        feedback.pushWarning(str(e))
        feedback.pushWarning('Docker is not installed or stopped, please install or start it')
        ready = False
        started = False
    
    if started:
        feedback.pushInfo('Checking if docker image is present')
        try:
            images = client.images.get('moskovchenkomike/ml4qgis:0.1')
            feedback.pushInfo('Docker image is present')
            ready = True 
        except Exception as e:
            #feedback.pushWarning(str(e))
            feedback.pushWarning('Docker image not found. Maybe it is not built')
            ready = False
        
        if ready:
            feedback.pushInfo('Checking if system supports CUDA')
            try:
                scriptsdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mount')
                gpu = client.containers.run('moskovchenkomike/ml4qgis:0.1', 
                                            command='/bin/sh',
                                            tty=True, detach=True, auto_remove=True,
                                            device_requests=[DeviceRequest(capabilities=[['gpu']])],
                                            volumes={scriptsdir: {'bind': '/mnt/scripts/', 'mode': 'rw'},})
                result = gpu.exec_run('/app/venv/bin/python /mnt/scripts/gpu_check.py')
                gpu.stop()
                
                if 'True' in str(result):
                    feedback.pushInfo("Found CUDA compatible GPU")
                else:
                    feedback.pushWarning('No GPU found. Several scripts can run very slow')
            except Exception as e:
                feedback.pushWarning(str(e))
                feedback.pushWarning('No GPU found. Several scripts can run very slow')
                
    return ready, started
    
def docker_install(feedback):
    # fix for docker-credential-desktop not installed or not available in PATH
    dconfig = str(Path.home()) + '/.docker/config.json'
    try:
        os.rename(dconfig, dconfig.replace('config.json', 'tempname.json'))
    except:
        pass
    
    ready, started = check('docker', feedback)
    
    if started:         
        client = from_env()
            
        images = client.images.list()
        feedback.pushInfo('Searching for older versions of docker image')
        for image in images:
            if image.tags is list and 'moskovchenkomike/ml4qgis' in image.tags[0]:
                if image.tags[0] != 'moskovchenkomike/ml4qgis:0.1':
                    feedback.pushInfo('Found obsolete image ' + image)
                    client.images.remove(image)
        feedback.setProgress(int(20))
        
        if not ready:
            # check if cuda image exist
            try:
                client.images.get('nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04')
                cudaexist = True
            except Exception as e:
                cudaexist = False
            
            dockerfiledir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'build')
            feedback.pushInfo('Start building docker image')
            
            
            
            try:
                client.images.build(path = dockerfiledir, tag = 'moskovchenkomike/ml4qgis:0.1',
                                    rm = True, forcerm = True, nocache = True)
                feedback.pushInfo('Docker image built successfully')
            except Exception as e:
                feedback.pushWarning('Building docker image failed')
                feedback.pushWarning(str(e))
            
            feedback.setProgress(int(70))
            
            feedback.pushInfo('Pruning intermediate dangling images')
            if cudaexist == False:
                try:
                    client.images.remove('nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04')
                except Exception as e:
                    feedback.pushWarning('Pruning failed')
                    feedback.pushWarning(str(e))
            try:
                client.images.prune(filters = {'dangling': True})
                feedback.pushInfo('Pruning successful')
            except Exception as e:
                feedback.pushWarning('Pruning failed')
                feedback.pushWarning(str(e))
            feedback.setProgress(int(90))
            
            check('docker', feedback)
    
    # fix for docker-credential-desktop not installed or not available in PATH
    try:
        os.rename(dconfig.replace('config.json', 'tempname.json'), dconfig)
    except:
        pass
    feedback.setProgress(int(100))
    
    return None
    
    
def getTempdir(feedback = None):
    tempconfig = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tempdir.json')
    with open(tempconfig, 'r') as f:
        data = json.load(f)
    tempdir = data["tempdir"]
    if os.path.isdir(tempdir):
        if feedback:
            feedback.pushInfo('Uses temporary directory ' + tempdir)
    else:
        defaulttempdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp')
        if feedback:
            if tempdir == "":
                feedback.pushInfo('Temporary directory not set. Using default temporary directory ' + defaulttempdir)
            else:
                feedback.pushInfo('Temporary directory not available. Using default temporary directory ' + defaulttempdir)
        tempdir = defaulttempdir
    return tempdir


def cleanTempdir(tempdir, feedback = None):
    feedback.pushInfo('Cleaning temp folder')
    files = glob.glob(tempdir + '/*')
    for f in files:
        try:
            shutil.rmtree(f)
        except OSError:
            os.remove(f)