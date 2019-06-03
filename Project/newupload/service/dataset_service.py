import os
import pandas as pd
import pyedflib
import numpy as np
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from .file_service import *
from django.core.files.storage import FileSystemStorage

global discard
discard = 256 * 60 * 5


def obtainValue(timeStart, timeStop, windowSizeSec, sampleFrequency):
    if (timeStart >= timeStop):
        raise Exception("start > end?? wtf")
    numberOfStart = timeStart*sampleFrequency
    numberStop = timeStop*sampleFrequency
    numberOfSignals = numberStop-numberOfStart
    windowSize = windowSizeSec*sampleFrequency
    return numberOfStart, numberStop, numberOfSignals, windowSize


def myOverlapping(array, window, stride):
    if (stride < 1):
        raise Exception("stride must be integer > 1")
    if(array.size < window):
        return np.append(array, np.zeros(window - array.size)).reshape((1, window))
    a=0
    b=window
    result = array[:window]
    passi = math.ceil((array.size - window + 1)/stride)
    for p in range(passi-1):
        a = a + stride
        b = b + stride
        result = np.append(result, array[a:b])
    result = result.reshape((-1, window))

    return result



def getDataset(file_path, channel, seizureStart, seizureEnd, windowSizeSec, stride, sampleFrequency, nSignals):
    startSeizureSignal, stopSeizureSignal, len,  windowSize = obtainValue(seizureStart , seizureEnd, windowSizeSec, sampleFrequency)
    seizure, _ = readFile(file_path, channel=channel, start=startSeizureSignal, len=len)
    overlapSeizure = myOverlapping(np.array(seizure), windowSize, stride)
    nSeizurewWindows = overlapSeizure.shape[0]

    newStart = startSeizureSignal - discard
    newEnd = stopSeizureSignal + discard

    if(newStart<0):
        newStart = 0
    if(newEnd > nSignals):
        newEnd = nSignals
    if(newStart<0 and newEnd > nSignals):
        raise Exception("Overflow due to discard")
    # print("st", newStart,"\nen", newEnd)
    windowsPre, _ = readFile(file_path, channel = channel, start = 0, len=newStart)
    windowsPost, _ = readFile(file_path, channel = channel, start= newEnd, len = None)
    windowsPre = np.array(windowsPre)
    windowsPost = np.array(windowsPost)

    len1 = math.floor(windowsPre.shape[0] / windowSize) * windowSize
    windowsPre = windowsPre[0:len1]
    len2 = math.floor(windowsPost.shape[0] / windowSize) * windowSize
    windowsPost = windowsPost[0:len2]

    windowsPre = windowsPre.reshape(-1,windowSize)
    windowsPost = windowsPost.reshape(-1,windowSize)
    
    if(windowsPre.shape[0] < (nSeizurewWindows/2)):
        nonSeizure = np.concatenate((windowsPre, windowsPost[:(nSeizurewWindows-windowsPre.shape[0])]))
    elif(windowsPost.shape[0] < (nSeizurewWindows/2)):
        nonSeizure = np.concatenate((windowsPre[:(nSeizurewWindows-windowsPost.shape[0])], windowsPost))
    else:
        nonSeizure = np.concatenate((windowsPre[:math.ceil(nSeizurewWindows/2)], windowsPost[:math.ceil(nSeizurewWindows/2)]))
    
    return overlapSeizure, nonSeizure


def createDataset(filename, seizureStart, seizureEnd, windowSizeSec, stride, sampleFrequency, nSignals, channels):
    fs = FileSystemStorage()
    os.mkdir(os.path.join(fs.base_location, "dataset",filename))
    for channel in range(channels):
        try:
            seizureSignals, normalSignals = getDataset(os.path.join(fs.base_location, "training", filename), channel, seizureStart, seizureEnd, windowSizeSec, stride, sampleFrequency, nSignals)
            signals = np.concatenate((seizureSignals, normalSignals))
            df = pd.DataFrame(data = signals)
            file = os.path.join(fs.base_location, "dataset", filename, "chn"+channel.__str__()+".pkl")
            # df.to_csv(file, index=False, header=False)
            df.to_pickle(file)
        except Exception as e:
            print(e)
            print("file ignored: ", filename)
            pass
        
    target = np.concatenate((np.ones(seizureSignals.shape[0], dtype=np.int64), np.zeros(normalSignals.shape[0], dtype=np.int64)))
    df_target = pd.DataFrame(data=target)
    df_target.to_pickle(os.path.join(fs.base_location, "dataset", filename,'target.pkl'))
    return seizureSignals.shape[0], normalSignals.shape[0]