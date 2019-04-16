from django.shortcuts import render
import pyedflib
import numpy as np
import os as os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# import matplotlib.pyplot as plt
from django import forms


def read_file(file):
    f = pyedflib.EdfReader(file)
    n = f.signals_in_file
    label = f.getSignalLabels()
    sigbufs = np.zeros((n, f.getNSamples()[0]))
    for i in np.arange(n):
        sigbufs[i, :] = f.readSignal(i)
    # print(sigbufs)
    return(f, sigbufs, label)


def upload_file(par):
    if par.FILES['myfile']:

        myfile = par.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        path = os.getcwd() + uploaded_file_url
        f, signal, label = read_file(path)

    return (upload_file, f, signal, label)
