from django.shortcuts import render
from django.http import JsonResponse
import pyedflib
import numpy as np
import os
from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

global file_path
file_path = "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\media\\chb01_01.edf"

@csrf_exempt #per far effettuare richieste POST senza autenticazione
def manageParam(request):
    # p = request.GET.get("par1")
    # p=0
    
    if request.method == 'POST':
        channel = request.POST.get("channel", 0)
    if request.method == 'GET':
        channel = request.GET.get("channel", 0)

    # data = {"par1": p}
    # response = JsonResponse(data)
    return getJson(channel)

def getJson(channel):
    print(f"il file che sto leggendo {file_path}")
    file = read_file(file_path)
    channel = int(channel)
    print(f'canale: {channel}')
    name = ""
    n = file.getNSamples()[channel]
    valori = np.zeros(n)
    valori = file.readSignal(channel)[:30].tolist()
    
    data = {"nome":name, "valori": valori}
    response = JsonResponse(data)
    return response


def read_file(file):
    f = pyedflib.EdfReader(file)
    # n = f.signals_in_file
    # label = f.getSignalLabels()
    # sigbufs = np.zeros((n, f.getNSamples()[0]))
    # for i in np.arange(n):
    #     sigbufs[i, :] = f.readSignal(i)
    # print(sigbufs)
    return(f)

@csrf_exempt
def upload_file(request):
    if request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        global file_path
        file_path = os.getcwd() + uploaded_file_url
        print(f'nuovopath {file_path}')
    return manageParam(request)