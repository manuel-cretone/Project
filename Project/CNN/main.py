import pandas as pd
import pyedflib
import numpy as np
import sys
import math
sys.path.insert(0, '../newupload')
import torch
import torch.nn as nn
import torch.nn.functional as F
import os

# from service.file_service import *
# from service.statisticService import *

global file_path
file_path = "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\media\\chb01_01.edf"
global discard
discard = 256 * 60 * 5


# def createListFile(array, target):
#     df = pd.DataFrame(columns=['value', 'target'])
#     for i in range(array.shape[0]):
#         # print(i)
#         # raw_data = np.array(( array[i], target))
#         raw_data = {'value': array[i],
#                     'target': target
#                     }
#         df = df.append(raw_data, ignore_index=True)
#     return df

# prende in input i secondi in cui inizia la scarica e ritorna a quale segnale
#  inizia la scarica

def obtainValue(timeStart, timeStop):
    if (timeStart >= timeStop):
        raise Exception("start > end?? wtf")
    numberOfStart = timeStart*256
    numberStop = timeStop*256
    numberOfSignals = numberStop-numberOfStart
    return numberOfStart, numberStop, numberOfSignals



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



def getSignals(file_path, channel, start=0, len=None):
    f = pyedflib.EdfReader(file_path)
    if (len == None):
        len = f.getNSamples()[channel] - start
    signals = f.readSignal(channel, start, len)
    x = np.array(signals)
    f._close()
    return x


def getDataset(file_path, channel, seizureStart, seizureEnd, windowSize, stride):
    startSeizureSignal, stopSeizureSignal, len = obtainValue(seizureStart , seizureEnd)
    seizure = getSignals(file_path, channel=channel, start=startSeizureSignal, len=len)
    overlapSeizure = myOverlapping(seizure, windowSize, stride)
    nSeizurewWindows = overlapSeizure.shape[0]

    newStart = startSeizureSignal - discard
    newEnd = stopSeizureSignal + discard

    if(newStart<0 or newEnd > 921600):
        raise Exception("Overflow due to discard")

    windowsPre = getSignals(file_path, channel = channel, start = 0, len=newStart)
    windowsPost = getSignals(file_path, channel = channel, start= newEnd, len = None)
      # add control in order to not consider all values
    # windowsPre = myOverlapping(valuesPre, windowSize, windowSize)
    # windowsPost = myOverlapping(valuesPost, windowSize, windowSize)
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

def createDataset(filename, seizureStart, seizureEnd, windowSize, stride):
    
    os.mkdir(filename)
    for channel in range(23):
        try:
            seizureSignals, normalSignals = getDataset("./edf_files/"+filename+".edf", channel, seizureStart, seizureEnd, windowSize, stride)
            signals = np.concatenate((seizureSignals, normalSignals))
            df = pd.DataFrame(data = signals)
            df.to_csv("./"+filename+'/chn'+channel.__str__()+'.csv', index=False, header=False)
        except:
            print("file ignored: ", filename)
            pass
        
    target = np.concatenate((np.ones(seizureSignals.shape[0], dtype=np.int64), np.zeros(normalSignals.shape[0], dtype=np.int64)))
    df_target = pd.DataFrame(data=target)
    df_target.to_csv("./"+filename+'/target.csv', index=False, header=False)



def main():
    windowSize = 256*30
    stride = 10
    file_list = pd.read_csv("./edf_files/files.csv", header = 0, sep=";")
    for i in range(file_list.shape[0]):
        filename = file_list["file"][i]
        seizureStart = file_list["start"][i]
        seizureEnd = file_list["stop"][i]
        createDataset(filename, seizureStart, seizureEnd, windowSize, stride)


if __name__ == '__main__':
    main()

