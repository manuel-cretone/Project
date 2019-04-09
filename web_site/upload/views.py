from django.shortcuts import render
import pyedflib

import numpy as np
import os as os
# Create your views here.


def index(request):


path = os.path.expanduser(
    "‎⁨~/Senza titolo⁩/Users⁩/manuelcretone⁩⁨/Desktop⁩/Project⁩/⁨web_site⁩/upload⁩")
f = pyedflib.EdfReader(path
)
n = f.signals_in_file
 signal_labels = f.getSignalLabels()
  sigbufs = np.zeros((n, f.getNSamples()[0]))
   for i in np.arange(n):
        sigbufs[i, :] = f.readSignal(i)
        print(sigbufs)
    context = {
        'file': sigbufs
    }

    return render(request, 'index.html', context=context)


