import pyedflib
import numpy as np
import sys
import math
sys.path.insert(0, '../newupload')

# from service.file_service import *
# from service.statisticService import *

global file_path
file_path = "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\media\\chb01_01.edf"


def createListFile(split):
    c = 0
    for i in split:
        a = str(c)
        np.savetxt("test" + a + ".txt", i)
        c = c+1
       # print(i)

# prende in input i secondi in cui inizia la scarica e ritorna a quale segnale
#  inizia la scarica

def obtainValue(timeStart, timeStop):
    if (timeStart >= timeStop):
        raise Exception("start > end wtf")
    numberOfStart = timeStart*256
    numberStop = timeStop*256
    numberOfSignals = numberStop-numberOfStart
    return numberOfStart, numberStop, numberOfSignals


def overlapping(a, w, o):
    if(a.size < w):
        return np.empty((1,w))
    sh = (a.size - w + 1, w)
    st = a.strides * 2
    view = np.lib.stride_tricks.as_strided(a, strides=st, shape=sh)[0::o]
    return view
    # print("overlapping")
    # for i in view:
    #     print(i)
    # print(view)

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

# prende i valori compresi nella sezione di Seizure e fa l'overlapping su quella
# zona restiuendo un vettore con le


# def seizureSignals(channel, timeStart, timeStop):
#     start, stop, len = obtainValue(timeStart, timeStop)
#     f = pyedflib.EdfReader(file_path)
#     signals = f.readSignal(channel, start, len)
#     x = np.array(signals)
#     return x


def getSignals(file_path, channel, start=0, len=None):
    f = pyedflib.EdfReader(file_path)
    signals = f.readSignal(channel, start, len)
    x = np.array(signals)
    f._close()
    return x


def spliteArray(signals, sizeWindow):
    x = np.array(signals)
    split = np.array_split(x, sizeWindow)
    return split


def main():

    channel = 0
    windowSize = 100
    overl = 10
    startSeizureSignal, stopSeizureSignal, len = obtainValue(100 , 200)

    seizure = getSignals(file_path, channel=0, start=startSeizureSignal, len=len)
    # prova = np.array([1,2,3,4,5,6,7,8,9,0])
    # overlapSeizure = myOverlapping(prova, 9, 1)
    overlapSeizure = myOverlapping(seizure, windowSize, overl)

    nSeizurewWindows = overlapSeizure.shape[0]
    valuesPre = getSignals(file_path, channel = channel, start = 0, len=startSeizureSignal)
    valuesPost = getSignals(file_path, channel = channel, start= stopSeizureSignal, len = 921600-stopSeizureSignal)
   # add control in order to not consider all values
    windowsPre = myOverlapping(valuesPre, windowSize, windowSize)
    windowsPost = myOverlapping(valuesPost, windowSize, windowSize)

    print("lunghezza pre", windowsPre.shape[0])
    print("lunghezza post", windowsPost.shape[0])

    if(windowsPre.shape[0] < (nSeizurewWindows/2)):
        nonSeizure = np.concatenate((windowsPre, windowsPost[:(nSeizurewWindows-windowsPre.shape[0])]))
    elif(windowsPost.shape[0] < (nSeizurewWindows/2)):
        nonSeizure = np.concatenate((windowsPre[:(nSeizurewWindows-windowsPost.shape[0])], windowsPost))
    else:
        nonSeizure = np.concatenate((windowsPre[:int(nSeizurewWindows/2)], windowsPost[:int(nSeizurewWindows/2)]))
    
    print(f"nonseizure {nonSeizure.shape}\nseizure{overlapSeizure.shape}")

if __name__ == '__main__':
    main()

