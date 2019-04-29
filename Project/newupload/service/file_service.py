import os
from django.shortcuts import redirect
# import sys
# sys.path.insert(0, '../newupload')
# import newupload as newupload
import pyedflib
import numpy as np
from newupload import views 


def absolute_path(file):
    path = os.getcwd() + file
    return path


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



def read_edf_file(filePath, channel, start, len):
    file = pyedflib.EdfReader(filePath)
    channel = int(channel)
    start = int(start)
    len = int(len)
    valori = np.zeros(len)
    valori = file.readSignal(channel, start, len).tolist()
    file._close
    return(valori)