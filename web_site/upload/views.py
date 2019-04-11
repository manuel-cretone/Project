import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from django.http import HttpResponse

from matplotlib import pylab
from django.shortcuts import render
import pyedflib
from django.shortcuts import render
import urllib
import json
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime as dt
import pdb
import random
import numpy as np
import matplotlib.pyplot as plt
import os as os

from . import upload_service
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def simple_upload(request):
    if request.method == 'POST':
        upload, signal = upload_service.upload_file(request)
        print(signal)
        return render(request, 'index.html', {
            'uploaded_file_url': upload,
            'signal': signal
        })
    return render(request, 'index.html')


def setPlt(file):
    f = pyedflib.EdfReader(
        '/Users/manuelcretone/Desktop/Project/web_site/media/prova.edf')

    n = f.signals_in_file
    signal_labels = f.getSignalLabels()
    sigbufs = np.zeros((n, f.getNSamples()[0]))
    fig = plt.figure()
    rows = 4
    cols = 2
    seconds = 60
    for i in np.arange(rows * cols):
        sigbufs[i, :] = f.readSignal(i)
        axes = fig.add_subplot(rows, cols, i+1)
        axes.set_title(signal_labels[i])
        axes.plot(sigbufs[i, :256*seconds], linewidth=0.5)


def pltToSvg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s


def get_svg(request):
    setPlt()  # create the plot
    svg = pltToSvg()  # convert plot to SVG
    plt.cla()  # clean up plt so it can be re-used
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response

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
