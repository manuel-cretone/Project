from django.shortcuts import render
import pyedflib
import numpy as np
import os as os
import io
from django.http import HttpResponse
# Create your views here.

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from . import upload_service

# def simple_upload(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         path = os.getcwd() + uploaded_file_url
#         file = pyedflib.EdfReader(path)
#         return readFileInfo(request, file)
#     else:
#         return render(request, 'index.html')

def simple_upload(request):
    if request.method == 'POST':
        global file
        global label
        global signal
        upload, file, signal, label = upload_service.upload_file(request)
        print(signal)
        return render(request, 'loaded1.html', {
            'uploaded_file_url': upload,
            'signal': signal,
            'label': label
        })
    return render(request, 'index.html')


def stampa(request):
    if request.method == 'POST':
        a = request.POST['select']
        print(int(a))
        label = file.getSignalLabels()
        segnali = chart(int(a))
        return render(request, 'loaded1.html', {'label': label, 'segnali':segnali})
    else:
        label = file.getSignalLabels()
        return render(request, 'index.html', {'label': label})

def chart(channel):
    # n = f.signals_in_file
    # print(channel)
    #sigbufs = np.zeros((n, f.getNSamples()[0]))
    # for i in np.arange(n):
    #     sigbufs[i, :] = f.readSignal(i)
    sigbufs = file.readSignal(channel, start=0, n= 1000)
    segnali = [0] *1000
    for i in range(1000):
        segnali[i] = sigbufs[i]
    return segnali
    # return render(request, 'loaded1.html', {'sigbufs': segnali})
    # return render(request, 'loaded.html', context=context)


# def readFileInfo(request, file):

#     if request.method == "POST":
#         a = request.POST.get('chn_list')
#         print(a)
#     # signal_labels = file.getSignalLabels()
#     # etichette = [0] *100
#     # selezione = request.POST.get('chn_list')
#     # for i in range(100):
#     #     # segnali[i] = int(sigbufs[i])
#     #     etichette[i] = signal_labels[i]
#     # render(request, 'loaded1.html', {'signal_label': etichette})
#     # channel = request.POST['chn_list']
#     # print(selezione)
#     return chart(request, file, 0)





# def index(request, file):

#     f = pyedflib.EdfReader(file)
#     n = f.signals_in_file
#     print("SIGNALS =>")
#     # print(n)
#     signal_read = f.getSignalHeaders()
#     m = f.getDigitalMaximum()
#     total_signal = f.readSignal(0, 0, 1000)

#     signal_labels = f.getSignalLabels()
#     time = f.samples_in_datarecord
#     """f.samples_in_datarecord"""
#     sigbufs = np.zeros((n, f.getNSamples()[0]))
#     for i in np.arange(n):
#         sigbufs[i, :] = f.readSignal(i)

#         print(sigbufs)
#     context = {
#         'file': sigbufs,
#         'signal': signal_labels,
#         'read': signal_read,
#         'm': m,
#         'total_signal': total_signal,
#         'time': time
#     }

#     return render(request, 'loaded.html', context=context)


# def setPlt(path):
#     f = pyedflib.EdfReader(path)
    
#     n = f.signals_in_file
#     signal_labels = f.getSignalLabels()
#     sigbufs = np.zeros((n, f.getNSamples()[0]))
#     fig = plt.figure()
#     rows = 4
#     cols = 2
#     seconds = 60
#     for i in np.arange(rows * cols):
#         sigbufs[i, :] = f.readSignal(i)
#         axes = fig.add_subplot(rows, cols, i+1)
#         axes.set_title(signal_labels[i])
#         axes.plot(sigbufs[i, :256*seconds], linewidth=0.5)


# def pltToSvg():
#     buf = io.BytesIO()
#     plt.savefig(buf, format='svg', bbox_inches='tight')
#     s = buf.getvalue()
#     buf.close()
#     return s


# def get_svg(path):
#     setPlt(path)  # create the plot
#     svg = pltToSvg()  # convert plot to SVG
#     plt.cla()  # clean up plt so it can be re-used
#     response = HttpResponse(svg, content_type='image/svg+xml')
#     return response


# from random import randint
# from django.views.generic import TemplateView
# from chartjs.views.lines import BaseLineChartView


# class LineChartJSONView(BaseLineChartView):
#     def get_labels(self):
#         """Return 7 labels for the x-axis."""
#         return ["January", "February", "March", "April", "May", "June", "July"]

#     def get_providers(self):
#         """Return names of datasets."""
#         return ["Central", "Eastside", "Westside"]

#     def get_data(self):
#         """Return 3 datasets to plot."""

#         return [[75, 44, 92, 11, 44, 95, 35],
#                 [41, 92, 18, 3, 73, 87, 92],
#                 [87, 21, 94, 3, 90, 13, 65]]

# line_chart = TemplateView.as_view(template_name='line_chart.html')
# line_chart_json = LineChartJSONView.as_view()



# def ch(request):
#     return render(request, 'loaded1.html')


