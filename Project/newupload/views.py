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
import itertools



from .service.file_service import *
from .service.statistic_service import *
from .service.dataset_service import *
from .service.train_service import *

global file_path
file_path = None
# global channels

global user_model


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
            global file_path
            file_path = os.path.join(fs.base_location, subFolder, filename)
            print(file_path)
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
        channel, start, length = readParams(request)
        info = file_info(file_path)
        sampleFrequency = info["sampleFrequency"]
        start = int(start) * sampleFrequency
        length = int(length) * sampleFrequency
        print(start, " ", length)
        values, timeScale = readFile(file_path, channel, start, length)
        
        # nSignals = info["nSignals"]
        data = {
            "file": file_path,
            "canale": channel,
            "inizio":start,
            "dimensione":length,
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
        _, start, length = readParams(request)
        info = file_info(file_path)
        sampleFrequency = info["sampleFrequency"]
        start = int(start) * sampleFrequency
        length = int(length) * sampleFrequency
        channels = info["channels"]
        data = {"inizio":start,
                "dimensione":length
                }
        window = []
        for i in range(channels):
            try:
                values, timeScale = readFile(file_path, i, start, length)
                window.append(values)
            except Exception as e:
                print("err", e)
                break
        # nChannels = int(len(window))
        data["nChannels"] = channels
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
        train_method = int(request.GET.get("train_method", 0))
        fs = FileSystemStorage()
        dataset_list= getDatasetList(fs.base_location)
        try:
            if(train_method == 1):
                #training con mix di file
                acc = k_fold_train(user_model, dataset_list, num_epochs)
                method = "k-fold training"
            else:
                #training con mix di windows
                acc = k_win_train(user_model, dataset_list, num_epochs)
                method = "k-window training"
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status = 400)
        

        #NB ACCURACY DELL'ULTIMA EPOCA!!!!!
        response = {
            "num_epochs": num_epochs,
            "method": method,
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
        base_location = fs.base_location
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
            createDataset(filename, base_location, seizureStart, seizureEnd, windowSec, stride)

        #L'ISTANZA DI RETE VIENE CARICATA SU VARIABILE GLOBALE
        # -> creare file da mettere in cartella cnn
        global user_model
        try:
            user_model = ConvNet(channels, windowSec*sampleFrequency)
        except Exception as e:
            return JsonResponse(data={"error": str(e)}, status = 400)
            
        return JsonResponse(data={"model": "network model created"}, status = 200)


    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)




@method_decorator(csrf_exempt, name='dispatch')
class Predict(View):
    def get(self, request):
        windowSec = 30
        sampleFrequency = 256
        windowSize = windowSec * sampleFrequency
        channels = 23
        fs = FileSystemStorage()
        model = ConvNet(channels= channels, windowSize = windowSize)      
        model.load_state_dict(torch.load(os.path.join(fs.base_location, "cnn", "trained_model_20190525-133930.pth")))
        model = model.eval()

        all_signals= []
        for chn in range(channels):
            values_array, _ = readFile(file_path, chn)
            values_array = np.array(values_array)
            values_matrix = windowGenerator(values_array, windowSize)
            values_tensor = torch.tensor(values_matrix)
            all_signals.append(values_tensor)
        complete_tensor = combineAllTensor(all_signals)

        response = {
            "dim": str(complete_tensor.shape),
        }
        dataset = EvalDataset(complete_tensor)
        loader = DataLoader(dataset = dataset, 
                            batch_size=1,
                            shuffle=False)

        for i, data in enumerate(loader):
            result = model(data)
            _, predicted = torch.max(result.data, 1)
            response["sec"+str(i*windowSec)] = predicted.item()



        return JsonResponse(data = response, status=200)