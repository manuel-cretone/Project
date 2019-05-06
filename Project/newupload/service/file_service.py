import os
from django.shortcuts import redirect
# import sys
# sys.path.insert(0, '../newupload')
# import newupload as newupload
import pyedflib
import numpy as np
# from newupload import views 
import datetime
import pandas as pd


# def absolute_path(file):
#     path = os.getcwd() + file
#     return path


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
    len = int(len)
    valori = np.zeros(len)
    valori = file.readSignal(channel, start, len).tolist()
    
    freq = file.samplefrequency(channel)
    second = 1/freq
    startTime = file.getStartdatetime() + datetime.timedelta(seconds=start*second)
    # startTime = startTime.strftime('%y-%m-%d-%H-%M-%S')
    # print(f"INII{startTime}")
    # endTime = startTime + datetime.timedelta(second=second*len)
    # timeScale = np.linspace(startTime, endTime, num=len, endpoint=False).tolist()

    timeScale = pd.date_range(startTime, freq = f"{second}S", periods=len).tolist()
    file._close
    return valori, timeScale



def file_info(filePath):
    file = pyedflib.EdfReader(filePath)
    startDate = file.getStartdatetime()
    fileDuration = file.getFileDuration()
    channels = len(file.getSignalLabels())
    channelLabels = np.empty(channels)
    nSignals = np.empty(channels)
    channelLabels = file.getSignalLabels()
    nSignals = file.getNSamples().tolist()

    data = {
        "file": filePath, 
        "startDate": startDate,
        "fileDuration": fileDuration,
        "channels": channels,
        "channelLabels": channelLabels,
        "nSignals": nSignals,

    }
    return data