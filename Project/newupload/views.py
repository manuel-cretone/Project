from django.shortcuts import render
from django.http import JsonResponse
import pyedflib
import numpy as np
import os
import glob
from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect


# import sys
# sys.path.insert(0, '../service')
from .service.file_service import *
from .service.statisticService import *


global file_path
file_path = None
# file_path = "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\media\\chb01_01.edf"


@csrf_exempt
def upload_file(request):
    if len(request.FILES) == 0:
        return JsonResponse({"error": "No file uploaded"}, status=400)
    elif request.FILES.get('myfile', False):
        fs = FileSystemStorage()
        dir = fs.base_location
        files = os.listdir(dir)
        for f in files:
            os.remove(os.path.join(dir, f))
        myfile = request.FILES['myfile']
        filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        # file_path = absolute_path(uploaded_file_url)
        global file_path
        file_path = os.path.join(dir, filename)
        print("path",file_path)
        try:
            extension_recognise(file_path)
        except:
            return JsonResponse({"error": "File not supported"}, status=415)
        return JsonResponse(file_info(file_path))
    else:
        return JsonResponse({"error": "no myfile field"}, status=400)

def file_info(filePath):
    file = pyedflib.EdfReader(filePath)
    startDate = file.getStartdatetime()
    fileDuration = file.getFileDuration()
    channels = len(file.getSignalLabels())
    channelLabels = np.empty(channels)
    nSignals = np.empty(channels)
    channelLabels = file.getSignalLabels()
    nSignals = file.getNSamples().tolist()

    # print(file.))
    
    data = {
        "file": filePath, 
        "startDate": startDate,
        "fileDuration": fileDuration,
        "channels": channels,
        "channelLabels": channelLabels,
        "nSignals": nSignals,

    }
    return data

@csrf_exempt #per far effettuare richieste POST senza autenticazione
def manageParam(request):
    if request.method == 'POST':
        channel = request.POST.get("channel", 0)
        start = request.POST.get("start", 0)
        len = request.POST.get("len", 30)
    if request.method == 'GET':
        channel = request.GET.get("channel", 0)
        start = request.GET.get("start", 0)
        len = request.GET.get("len", 30)
    # return readFile(channel, start, len)
    return readFile(channel, start, len)


def readFile(channel, start, len):
    fun = extension_recognise(file_path)
    valori = fun(file_path, channel, start, len)

    # print(hist)
    data = {"file": file_path, "canale": channel, "inizio":start, "dimensione":len,"valori": valori}
    response = JsonResponse(data)
    return response


def getStatistic(values):
    min = min_value(values)
    max = max_value(values)
    average = average_value(values)
    var = variance(values)
    stdev = stdev(values)
    hist, bins = counts_occurrences(values, 1.5)

    data = {
        "min" = min,
        "max" = max,
        "average" = average,
        "var" = var,
        "stdev" = stdev
    }

    return data