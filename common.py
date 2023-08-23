import os
import sys
from sys import platform
import json
import subprocess

from .docker import from_env
from .docker.types import DeviceRequest


def getInterpreter(backend):
    # Gets a path to a Python interpreter
    if backend == 'python':
        # Open Python config
        pythonconfig = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'python.json')
        with open(pythonconfig, 'r') as f:
            data = json.load(f)
        path = data['path']
        # Appends a system dependent path part
        if platform == "linux" or platform == "linux2":
            interpreter = os.path.join(path, 'bin', 'python')
        elif platform == "darwin":
            interpreter = os.path.join(path, 'bin', 'python')
        elif platform == "win32":
            interpreter = os.path.join(path, 'Scripts', 'python.exe')
    elif backend == 'conda':
        # Open Python config
        condaconfig = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'conda.json')
        with open(condaconfig, 'r') as f:
            data = json.load(f)
        path = data['path']
        env = data['env']
        if env == '':
            interpreter = path
        else:
            interpreter = os.path.join(path, 'envs', env)
        # Appends a system dependent path part
        if platform == "linux" or platform == "linux2":
            interpreter = os.path.join(interpreter, 'python')
        elif platform == "darwin":
            interpreter = os.path.join(interpreter, 'python')
        elif platform == "win32":
            interpreter = os.path.join(interpreter, 'python.exe')
    elif backend == 'docker':
        interpreter = '/app/venv/bin/python'
    else:
        interpreter = ''
    return interpreter
    
    
def getEnv(interpreter):
    # Changes default QGIS env variables
    my_env = os.environ.copy()
    path = os.path.dirname(interpreter)
    my_env["PATH"] = path + os.pathsep + os.path.join(path, 'Library')
    if platform == "linux" or platform == "linux2":
        my_env["PATH"] = path + os.pathsep + '/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin'
    elif platform == "darwin":
        my_env["PATH"] = path + os.pathsep + '/usr/sbin:/usr/bin:/sbin:/bin'
    elif platform == "win32":
        my_env["PATH"] = path + os.pathsep + r'C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;'
    my_env.pop('PYTHONHOME')
    return my_env


def getScript(script, backend):
    # Gets path to a script in scripts folder
    if backend == 'docker':
        scriptpath = '/mnt/scripts/' + script
    else:
        scriptsdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mount')
        scriptpath = os.path.join(scriptsdir, script)
    return scriptpath
    

def getInputLayer(layer, tempdir, backend):
    # Gets path to a file in temp dir
    if backend == 'python' or backend == 'conda':
        layer = os.path.join(tempdir, os.path.basename(layer))
    elif backend == 'docker':
        layer = '/mnt/temp/' + os.path.basename(layer)
    else:
        layer = os.path.join(tempdir, os.path.basename(layer))
        feedback.pushWarning('Something wrong with backend')
    return layer
    

def runCommand(cmd, backend, interpreter, tempdir, feedback):
    # Runs a command
    if backend == 'python' or backend == 'conda':
        feedback.pushInfo('Running command in ' + backend)
        my_env = getEnv(interpreter)
        #rasterio sometimes throws a strange error that does not affect anything but spams to stout
        ignore = ['Traceback (most recent call last)', 'in defenv', 'local._env.start()', 'UnicodeDecodeError', '_env.log_error']
        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, env=my_env)
            while True:
                output = process.stdout.readline().decode().strip()
                if process.poll() is not None:
                    break
                if output and not any([x in output for x in ignore]):
                    feedback.pushInfo(output)
            rc = process.poll()
        except Exception as e:
            feedback.pushWarning(str(e))
            feedback.pushWarning('Running command failed')     
    elif backend == 'docker':
        client = from_env()
        feedback.pushInfo('Creating Docker container')
        try:
            scriptsdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mount')
            container = client.containers.run('moskovchenkomike/ml4qgis:0.1', 
                                            command=cmd,
                                            detach=True, auto_remove=True,
                                            device_requests=[DeviceRequest(capabilities=[['gpu']])],
                                            volumes={scriptsdir: {'bind': '/mnt/scripts/', 'mode': 'rw'}, tempdir: {'bind': '/mnt/temp/', 'mode': 'rw'}})
            for line in container.logs(stream=True):
                feedback.pushInfo(line.decode().strip())
            #result = container.exec_run(cmd)
            container.wait(condition = 'removed')
        except Exception as e:
            feedback.pushWarning(str(e))
            feedback.pushWarning('Running container failed')                                
    else:
        feedback.pushWarning('Something wrong with backend')
