from django.shortcuts import render
import pyedflib

import numpy as np
import os as os
# Create your views here.


from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        path = os.getcwd() + uploaded_file_url
        print("PATH")
        print(path)

        
        render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url
        })
        return index(request, path)
    return render(request, 'index.html')


def index(request, file):

    f = pyedflib.EdfReader(file)
    n = f.signals_in_file
    print("SIGNALS =>")
    print(n)
    signal_read = f.getSignalHeaders()
    m = f.getDigitalMaximum()
    total_signal = f.readSignal(0, 0, 1000)

    signal_labels = f.getSignalLabels()
    time = f.samples_in_datarecord
    """f.samples_in_datarecord"""
    sigbufs = np.zeros((n, f.getNSamples()[0]))
    for i in np.arange(n):
        sigbufs[i, :] = f.readSignal(i)

        print(sigbufs)
    context = {
        'file': sigbufs,
        'signal': signal_labels,
        'read': signal_read,
        'm': m,
        'total_signal': total_signal,
        'time': time
    }

    return render(request, 'loaded.html', context=context)
