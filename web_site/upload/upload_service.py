from django.shortcuts import render
import pyedflib
import numpy as np
import os as os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt


def read_file(file):
    f = pyedflib.EdfReader(file)
    n = f.signals_in_file

    sigbufs = np.zeros((n, f.getNSamples()[0]))
    for i in np.arange(n):
        sigbufs[i, :] = f.readSignal(i)
    print(sigbufs)
    return(sigbufs)
