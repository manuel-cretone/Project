from django.shortcuts import render
from django.http import JsonResponse
import pyedflib
import numpy as np
import os
from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect


# import sys
# sys.path.insert(0, '../service')
from .service.file_service import *
from .service.statisticService import *


global file_path
# file_path = "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\media\\chb01_01.edf"


@csrf_exempt
def upload_file(request):
    if request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        global file_path
        file_path = absolute_path(uploaded_file_url)
    return file_info(file_path)

def file_info(filePath):
    file = pyedflib.EdfReader(filePath)
    channels = np.empty(100)
    lenght = np.empty(100)
    channels = file.getSignalLabels()
    lenght = file.getNSamples().tolist()
    print(channels)
    print(lenght)
    data = {
        "file": filePath, 
        "channels": channels,
        "lenght": lenght
    }
    return JsonResponse(data)

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
    return readFile(channel, start, len)


def readFile(channel, start, len):
    fun = extension_recognise(file_path)
    valori = fun(file_path, channel, start, len)
    hist, bins = counts_occurrences(valori, 1.5)
    # print(hist)
    data = {"file": file_path, "canale": channel, "inizio":start, "dimensione":len,"valori": valori}
    response = JsonResponse(data)
    return response


