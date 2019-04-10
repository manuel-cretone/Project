from django.shortcuts import render
import pyedflib

import numpy as np
import matplotlib.pyplot as plt
import os as os

from . import upload_service
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
        signal = upload_service.read_file(path)

        return render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url,
            'signal': signal
        })
    return render(request, 'index.html')


# def index(request):

    # f = pyedflib.EdfReader()
    # n = f.signals_in_file
    # sigbufs = np.zeros((n, f.getNSamples()[0]))
    # for i in np.arange(n):
    #     sigbufs[i, :] = f.readSignal(i)

    #     print(sigbufs)
    # context = {
    #     'file': sigbufs
    # }

    # return render(request, 'loaded.html', context=context)
