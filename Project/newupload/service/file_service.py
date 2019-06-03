import os
from django.shortcuts import redirect
import pyedflib
import numpy as np
import datetime
import pandas as pd
from django.core.files.storage import FileSystemStorage
import shutil


# [check extension file if .edf, .txt, .pdf]
def extension_recognise(filePath):
    info, ex = os.path.splitext(filePath)

    if(ex == '.edf'):
        return read_edf_file
    # elif(ex == '.txt'):
    #     return redirect('')
    # elif(ex == '.csv'):
    #     return redirect('')
    else:
        raise ValueError("File inserito non supportato")


def readFile(file_path, channel, start=0, len=None):
    fun = extension_recognise(file_path)
    values, timeScale = fun(file_path, channel, start, len)
    return values, timeScale


def read_edf_file(filePath, channel, start=0, len=None):
    file = pyedflib.EdfReader(filePath)
    channel = int(channel)
    start = int(start)
    timeScale = None
    if(len != None):
        len = int(len)
        freq = file.samplefrequency(channel)
        second = 1/freq
        startTime = file.getStartdatetime() + datetime.timedelta(seconds=start*second)
        timeScale = pd.date_range(startTime, freq = f"{second}S", periods=len).tolist()
    
    valori = file.readSignal(channel, start=start, n=len).tolist()
    file._close
    return valori, timeScale



def file_info(filePath):
    file = pyedflib.EdfReader(filePath)
    startDate = file.getStartdatetime()
    fileDuration = file.getFileDuration()
    channels = len(file.getSignalLabels())
    sampleFrequency = file.getSampleFrequency(0)
    channelLabels = np.empty(channels)
    # nSignals = np.empty(channels).tolist()
    channelLabels = file.getSignalLabels()
    
    nSignals = file.getNSamples().tolist()[0]

    data = {
        "file": filePath, 
        "startDate": startDate,
        "fileDuration": fileDuration,
        "channels": channels,
        "sampleFrequency": sampleFrequency,
        "nSignals": nSignals,
        "channelLabels": channelLabels,
    }
    return data



def handleFile(request, subFolder):
    if len(request.FILES) == 0:
            return ("", {"error": "No file uploaded"}, 400)
    elif request.FILES.get('myfile', False):
        fs = FileSystemStorage()
        myfile = request.FILES['myfile']
        filename = fs.save(os.path.join(subFolder, myfile.name), myfile)
        filename = os.path.relpath(filename, subFolder)
        file_path = os.path.join(fs.base_location, subFolder, filename)
        try:
            extension_recognise(file_path)
        except:
            return ("", {"error": "File not supported"}, 415)
        response = file_info(file_path)
        return (filename, response, 200)
    else:
        return ("", {"error": "no myfile field"}, 400)


def cleanFolder(subFolder):
    fs = FileSystemStorage()
    dir = os.path.join(fs.base_location, subFolder)
    # files = os.listdir(dir)
    for r, directories, files in os.walk(dir):
        for f in files:
            os.remove(os.path.join(dir, f))
        for d in directories:
            shutil.rmtree(os.path.join(dir, d), ignore_errors = True)
    