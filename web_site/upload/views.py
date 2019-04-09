from django.shortcuts import render
import pyedflib

import numpy as np
import os as os
# Create your views here.


def index(request):

    f = pyedflib.EdfReader(
        './prova.edf')
    n = f.signals_in_file

    signal_read = f.getSignalHeaders()
    signal_labels = f.getSignalLabels()
    sigbufs = np.zeros((n, f.getNSamples()[0]))
    for i in np.arange(n):
        sigbufs[i, :] = f.readSignal(i)

        print(sigbufs)
    context = {
        'file': sigbufs,
        'signal': signal_labels,
        'read': signal_read
    }

    return render(request, 'index.html', context=context)
