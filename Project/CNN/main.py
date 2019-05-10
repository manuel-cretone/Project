import pandas as pd
import pyedflib
import numpy as np
import sys
import math
sys.path.insert(0, '../newupload')

# from service.file_service import *
# from service.statisticService import *

global file_path
file_path = "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\media\\chb01_01.edf"


# def createListFile(name, split):
#     c = 0
#     for i in split:
#         a = str(c)
#         np.savetxt(name + a + ".txt", i)
#         c = c+1
def createListFile(array, target):
    df = pd.DataFrame(columns=['value', 'target'])
    for i in range(array.shape[0]):
        print("IIIIIIIIII")
        print(i)
        raw_data = {'value': array[i],
                    'target': target
                    }
        df = df.append(raw_data, ignore_index=True)

    print("Raw Data")
    print(df)
    print(df.shape)
    # df = pd.DataFrame(raw_data, columns=['value', 'target'])
    #df.to_csv('output.csv', index=False, header=True)
    return df
       # print(i)

# prende in input i secondi in cui inizia la scarica e ritorna a quale segnale
#  inizia la scarica

def obtainValue(timeStart, timeStop):
    if (timeStart >= timeStop):
        raise Exception("start > end?? wtf")
    numberOfStart = timeStart*256
    numberStop = timeStop*256
    numberOfSignals = numberStop-numberOfStart
    return numberOfStart, numberStop, numberOfSignals


# def overlapping(a, w, o):
#     if(a.size < w):
#         return np.empty((1,w))
#     sh = (a.size - w + 1, w)
#     st = a.strides * 2
#     view = np.lib.stride_tricks.as_strided(a, strides=st, shape=sh)[0::o]
#     return view


def myOverlapping(array, window, overlapping):
    if (overlapping < 1):
        raise Exception("overlapping must be integer > 1")
    if(array.size < window):
        return np.append(array, np.zeros(window - array.size)).reshape((1, window))
    a=0
    b=window
    result = array[:window]
    passi = math.ceil((array.size - window + 1)/overlapping)
    for p in range(passi-1):
        a = a + overlapping
        b = b + overlapping
        result = np.append(result, array[a:b])
    result = result.reshape((-1, window))

    return result


# def seizureSignals(channel, timeStart, timeStop):
#     start, stop, len = obtainValue(timeStart, timeStop)
#     f = pyedflib.EdfReader(file_path)
#     signals = f.readSignal(channel, start, len)
#     x = np.array(signals)
#     return x


def getSignals(file_path, channel, start=0, len=None):
    f = pyedflib.EdfReader(file_path)
    if (len == None):
        len = f.getNSamples()[channel] - start
    signals = f.readSignal(channel, start, len)
    x = np.array(signals)
    f._close()
    return x


# def spliteArray(signals, sizeWindow):
#     x = np.array(signals)
#     split = np.array_split(x, sizeWindow)
#     return split


def getDataset(file_path, channel, seizureStart, seizureEnd, windowSize, overlapping):
    startSeizureSignal, stopSeizureSignal, len = obtainValue(seizureStart , seizureEnd)
    seizure = getSignals(file_path, channel=0, start=startSeizureSignal, len=len)
    overlapSeizure = myOverlapping(seizure, windowSize, overlapping)
    nSeizurewWindows = overlapSeizure.shape[0]

    valuesPre = getSignals(file_path, channel = channel, start = 0, len=startSeizureSignal)
    valuesPost = getSignals(file_path, channel = channel, start= stopSeizureSignal, len = None)
      # add control in order to not consider all values
    windowsPre = myOverlapping(valuesPre, windowSize, windowSize)
    windowsPost = myOverlapping(valuesPost, windowSize, windowSize)
    
    if(windowsPre.shape[0] < (nSeizurewWindows/2)):
        nonSeizure = np.concatenate((windowsPre, windowsPost[:(nSeizurewWindows-windowsPre.shape[0])]))
    elif(windowsPost.shape[0] < (nSeizurewWindows/2)):
        nonSeizure = np.concatenate((windowsPre[:(nSeizurewWindows-windowsPost.shape[0])], windowsPost))
    else:
        nonSeizure = np.concatenate((windowsPre[:math.ceil(nSeizurewWindows/2)], windowsPost[:math.ceil(nSeizurewWindows/2)]))
    
    return overlapSeizure, nonSeizure

def main():

    channel = 0
    seizureStart = 100
    seizureEnd = 101
    windowSize = 50
    overlapping = 30

    seizureSignals, normalSignals = getDataset(file_path, channel, seizureStart, seizureEnd, windowSize, overlapping)
    print("seizure", seizureSignals.shape)
    print("normal", normalSignals.shape)
    # createListFile("seizure", seizureSignals)
    # createListFile("normal", normalSignals)
    df_seizure = createListFile(seizureSignals, 1)
    df_notSeizure = createListFile(seizureSignals, 0)
    df = df_seizure.append(df_notSeizure, ignore_index=True)
    df.to_csv('output.csv', index=False, header=True)

    data = pd.read_csv("output.csv")
    print(data)
    # train = pd.read_csv("train.csv")   
    # x_train = train["text"].values
    # y_train = train['target'].values


if __name__ == '__main__':
    main()

