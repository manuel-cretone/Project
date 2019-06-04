from django.shortcuts import render
from django.http import JsonResponse
import pyedflib
import numpy as np
import os
import glob
from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.views import View
import pandas as pd
import torch
import torch.nn as nn
import shutil

import sys
sys.path.insert(0, '../CNN')


from .service.file_service import *
from .service.statistic_service import *
from .service.dataset_service import *
from .service.train_service import *

global file_path
file_path = None
global channels
global nSignals
global model


def readParams(request):
    channel = request.GET.get("channel", 0)
    start = request.GET.get("start", 0)
    length = request.GET.get("len", 30)
    return (channel, start, length)

#view per file upload
@method_decorator(csrf_exempt, name='dispatch')
class Upload(View):
    def post(self, request):
        subFolder = "up"
        cleanFolder(subFolder)
        filename, response, status = handleFile(request, subFolder)
        if(status==200):
            fs = FileSystemStorage()
            global file_path, channels, nSignals
            file_path = os.path.join(fs.base_location, subFolder, filename)
            print(file_path)
            channels = response["channels"]
            nSignal = response["nSignals"]
        return JsonResponse(response, status=status)
    
    def get(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)




@method_decorator(csrf_exempt, name='dispatch')
class UploadTraining(View):
    def post(self, request):
        subFolder = "training"
        filename, response, status = handleFile(request, subFolder)
        if(status==200):
            fs = FileSystemStorage()
            channels = response["channels"]
            nSignal = response["nSignals"]
            sampleFrequency = response["sampleFrequency"]

            seizureStart = request.POST.get("seizureStart", 0)
            seizureEnd = request.POST.get("seizureEnd", 0)

            if(seizureEnd < seizureStart):
                return JsonResponse(data={"error": "bad seizure parameters"}, status=400)

            df = pd.DataFrame(data={"filename": [filename], 
                                    "seizureStart": [seizureStart], 
                                    "seizureEnd": [seizureEnd],
                                    "channels": [channels],
                                    "nSignal": [nSignal],
                                    "sampleFrequency": [sampleFrequency],
                                    })
            file_list = os.path.join(fs.base_location, subFolder, "file_list.csv")
            with open(file_list,'a') as fd:
                df.to_csv(fd, header=False, index=False)
            response.update({"seizureStart": seizureStart, "seizureEnd": seizureEnd})
        return JsonResponse(response, status=status)
    
    def get(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)


#view per leggere i valori
@method_decorator(csrf_exempt, name='dispatch')
class Values(View):
    def get(self, request):
        channel, start, len = readParams(request)
        values, timeScale = readFile(file_path, channel, start, len)
        data = {
            "file": file_path,
            "canale": channel,
            "inizio":start,
            "dimensione":len,
            "valori": values,
            "timeScale": timeScale
        }
        response = JsonResponse(data, status = 200)
        return response

    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)


#view per ottenere una finestra con tutti i canali 
@method_decorator(csrf_exempt, name='dispatch')
class CompleteWindow(View):
    def get(self, request):
        global channels
        channel, start, lenght = readParams(request)
        data = {"inizio":start,
                "dimensione":lenght
                }
        window = []
        for i in range(channels):
            values, timeScale = readFile(file_path, channel, start, lenght)
            # data["chn"+str(i)] = values
            window.append(values)
        nChannels = int(len(window))
        data["nChannels"] = nChannels
        data["window"] = window
        data["timeScale"] = timeScale
        response = JsonResponse(data, status = 200)
        return response

    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)


#view per ottenere statistiche
class Statistics(View):
    def get(self, request):
        channel, start, length = readParams(request)
        values, timeScale = readFile(file_path, channel, start=0, len=None)
        
        data = getStatistic(values)
        response = JsonResponse(data, status = 200)
        return response

    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)


#view per ottenere istogramma valori
class Distribution(View):
    def get(self, request):
        channel, start, length = readParams(request)
        values, timeScale = readFile(file_path, channel, start=0, len=None)
        hist, bins = count_occurrences(values, 20) #esempio con parametro 2 
        data = {
            "hist": hist,
            "bins": bins
        }
        response = JsonResponse(data, status = 200)
        return response

    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)


class Train(View):
    def get(self, request):
        num_epochs = int(request.GET.get("epochs",1))

        dataset_list= getDatasetList()
        
        #specificare tipo di training
        dataset = ConcatDataset(dataset_list)
        acc = k_win_train(model, dataset, num_epochs)

        #NB ACCURACY DELL'ULTIMA EPOCA!!!!!
        response = {
            "num_epochs": num_epochs,
            "accuracy": acc
        }
        return JsonResponse(response, status=200)
        

    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)


class ConvertDataset(View):

    def get(self, request):
        windowSec = int(request.GET.get("windowSize", 1))
        stride = int(request.GET.get("stride", 1))
        
        #crea nuovo dataset (diviso in files pkl)
        fs = FileSystemStorage()
        file_list = pd.read_csv(os.path.join(fs.base_location, "training", "file_list.csv"), header = 0, sep=",")
        sf = None
        ch = None
        for i in range(file_list.shape[0]):
            filename = file_list["filename"][i]
            seizureStart = int(file_list["seizurestart"][i])
            seizureEnd = int(file_list["seizureEnd"][i])
            channels = file_list["channels"][i]
            nSignal = file_list["nSignal"][i]
            sampleFrequency = int(file_list["sampleFrequency"][i])
            
            if((sf != None and sampleFrequency != sf) or (ch!=None and channels != ch)):
                return JsonResponse(data={"error": "file must have same sample frequency and channels"}, status = 400)
            sf = sampleFrequency
            ch = channels
            
            if(windowSec > seizureEnd-seizureStart):
                return JsonResponse(data={"error": "bad window size parameter"}, status = 400)
            createDataset(filename, seizureStart, seizureEnd, windowSec, stride, sampleFrequency, nSignal, channels)

        #L'ISTANZA DI RETE VIENE CARICATA SU VARIABILE GLOBALE
        global model
        model = ConvNet(channels, windowSec*sampleFrequency)
            
        return JsonResponse(data={"model": "network model created"}, status = 200)


    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)


"""

@method_decorator(csrf_exempt, name='dispatch')
class Predict(View):
    def get(self, request):
        windowSize = 256*30
        nomeFile = "provanome/"
        windowsGenerator(nomeFile, windowSize)
        
        model = ConvNet()      
        model.load_state_dict(torch.load("C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\CNN\\trained_model_20190525-133930.pth"))
        model = model.eval()

        dataset = EvalDataset(nomeFile)
        train_loader = DataLoader(dataset=dataset,
                                batch_size=1,
                                shuffle=False)
        
        for i, data in enumerate(train_loader):
            result = model(data)
            _, predicted = torch.max(result.data, 1)
            print("finestra",i,": ",predicted)

        

#create a folder with one csv file for each channel
def windowsGenerator(file_name, windowSize):
    shutil.rmtree('./'+file_name, ignore_errors = True)
    os.mkdir(file_name)
    for channel in range(23):
        signals = getSignals(file_path, channel)
        #last seconds discarded
        length = math.floor(signals.size / windowSize) * windowSize
        signals = signals[:length]

        signals = signals.reshape((-1, windowSize))
        df = pd.DataFrame(data = signals)
        df.to_csv("./"+file_name+'/chn'+channel.__str__()+'.csv', index=False, header=False)



"""