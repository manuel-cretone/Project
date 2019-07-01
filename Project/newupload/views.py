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
import time
from .models import UserNet, UserFiles
from django.db.models import Max, Min



from .service.file_service import *
from .service.statistic_service import *
from .service.dataset_service import *
from .service.train_service import *

global file_path
file_path = None
# global channels

# global user_model
global model_chn
global model_winSec
global model_sampleFrequency


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
            # fs = FileSystemStorage()
            channels = response["channels"]
            nSignal = response["nSignals"]
            sampleFrequency = response["sampleFrequency"]

            seizureStart = request.GET.get("seizureStart", 0)
            seizureEnd = request.GET.get("seizureEnd", 0)

            if(seizureEnd < seizureStart):
                return JsonResponse(data={"error": "bad seizure parameters"}, status=400)

            record = UserFiles(
                name = filename,
                seizureStart = seizureStart,
                seizureEnd = seizureEnd,
                channels = channels,
                nSignal = nSignal,
                sampleFrequency = sampleFrequency
            )
            record.save()
            
            response["uploaded"] = []
            all_files = UserFiles.objects.all()
            for f in all_files:
                response["uploaded"].append(f.name)
            
            #TODO togliere csv e gestire con db
            # file_list = os.path.join(fs.base_location, subFolder, "file_list.csv")
            # with open(file_list,'a') as fd:
            #     df.to_csv(fd, header=False, index=False)
            # response.update({"seizureStart": seizureStart, "seizureEnd": seizureEnd})

            # f_list = pd.read_csv(os.path.join(fs.base_location, subFolder, "file_list.csv"), header = 0, sep=",")
            # #TODO modifica come metto in json lista file caricati ->penosa
            # response.update({"files": f_list.to_dict(orient="split")})

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
        user_model = ConvNet(model_chn, model_winSec*model_sampleFrequency)
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
            
            timestr = time.strftime("%Y%m%d-%H%M%S")
            mod_name = request.GET.get("name", 'trained_model_'+timestr+".pth")
            
            torch.save(user_model.state_dict(), os.path.join(fs.base_location, "usermodels", mod_name))
            
            # df = pd.DataFrame(data={"modelname": [mod_name],
            #             "channels": [model_chn],
            #             "windowSize": [model_winSize],
            #             })
            # models_list = os.path.join(fs.base_location, "usermodels", "models.csv")
            # with open(models_list,'a') as fd:
            #     df.to_csv(fd, header=False, index=False)

            record = UserNet(name=mod_name,
                                    channels=model_chn, 
                                    windowSec = model_winSec,
                                    sampleFrequency = model_sampleFrequency,
                                    # file = user_model.state_dict(),
                                    link = os.path.join(fs.base_location, "usermodels", mod_name)
                                    )
            addDefaultModel()
            record.save()

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
        
        cleanFolder("dataset")

        #crea nuovo dataset (diviso in files pkl)
        fs = FileSystemStorage()
        base_location = fs.base_location
        file_list = pd.DataFrame(list(UserFiles.objects.all().values()))

        sf_max = UserFiles.objects.aggregate(Max("sampleFrequency"))["sampleFrequency__max"]
        sf_min = UserFiles.objects.aggregate(Min("sampleFrequency"))["sampleFrequency__min"]
        ch_max = UserFiles.objects.aggregate(Max("channels"))["channels__max"]
        ch_min = UserFiles.objects.aggregate(Min("channels"))["channels__min"]

        if(ch_max != ch_min or sf_max != sf_min):
            return JsonResponse(data={"error": "file must have same sample frequency and channels"}, status = 400)


        for i in range(file_list.shape[0]):
            filename = file_list["name"][i]
            seizureStart = int(file_list["seizureStart"][i])
            seizureEnd = int(file_list["seizureEnd"][i])
            channels = file_list["channels"][i]
            nSignal = file_list["nSignal"][i]
            sampleFrequency = int(file_list["sampleFrequency"][i])
            
            # if((sf != None and sampleFrequency != sf) or (ch!=None and channels != ch)):
            #     return JsonResponse(data={"error": "file must have same sample frequency and channels"}, status = 400)
            # sf = sampleFrequency
            # ch = channels
            
            if(windowSec > seizureEnd-seizureStart):
                return JsonResponse(data={"error": "bad window size parameter"}, status = 400)
            createDataset(filename, base_location, seizureStart, seizureEnd, windowSec, stride)

        #I parametri della rete vengono caricati su variabili globali 
        # -> possibile allenare rete ripetutamente
        global model_chn
        global model_winSec
        global model_sampleFrequency
        model_chn = channels
        model_winSec = windowSec
        model_sampleFrequency = sampleFrequency

        return JsonResponse(data={"data": "database created"}, status = 200)


    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)




@method_decorator(csrf_exempt, name='dispatch')
class Predict(View):
    def get(self, request):
        model_id = request.GET.get("model_id", 0)

        try:
            m = UserNet.objects.get(id=model_id)
        except UserNet.DoesNotExist:
            addDefaultModel()
            m = UserNet.objects.get(id=0)


        windowSec = int(m.windowSec)
        sampleFrequency = int(m.sampleFrequency)
        windowSize = windowSec * sampleFrequency
        channels = m.channels
        
        #controllo channels e sample rate del file coincidono con rete 
        info = file_info(file_path)
        if(info["channels"] != channels or info["sampleFrequency"] != sampleFrequency):
            return JsonResponse(data={
                                    "error": "file e rete non compatibili",
                                    "file_chn": info["channels"],
                                    "net_chn": channels,
                                    "file_sample": info["sampleFrequency"],
                                    "net_sample": sampleFrequency
                                    }, 
                                status = 400)

        
        model = ConvNet(channels= channels, windowSize = windowSize)      
        model.load_state_dict(torch.load(m.link))
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
            "name": m.name,
        }
        dataset = EvalDataset(complete_tensor)
        loader = DataLoader(dataset = dataset, 
                            batch_size=1,
                            shuffle=False)
        response["time"] = []
        response["values"] = []
        seizureWindows = 0
        for i, data in enumerate(loader):
            result = model(data)
            _, predicted = torch.max(result.data, 1)
            if(predicted==1):
                seizureWindows = seizureWindows+1
            response["time"].append(str(i*windowSec))
            response["values"].append(predicted.item())
        
        response["seizureWindows"] = seizureWindows
        response["totalWindows"] = complete_tensor.shape[0]
        return JsonResponse(data = response, status=200)

    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)


@method_decorator(csrf_exempt, name='dispatch')
class UserModels(View):
    def get(self, request):

        response= {}
        response["id"] = []
        response["name"] = []
        all_models = UserNet.objects.all()
        for m in all_models:
            # response[m.id] = {  "name": m.name,
            #                     "channels": m.channels, 
            #                     "windowSec" : m.windowSec,
            #                     "sampleFrequency": m.sampleFrequency,
            #                     "link": m.link
            #                         }
            response["name"].append(m.name)
            response["id"].append(m.id)
        return JsonResponse(response, status=200)

    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)


class CleanUserModels(View):
    def get(self, request):
        UserNet.objects.all().delete()
        cleanFolder("usermodels")
        addDefaultModel()

        return JsonResponse({"message": "no user models in database"}, status = 200)


def addDefaultModel():
    fs = FileSystemStorage()
    record = UserNet(id=0,
                    name="Default model",
                    channels="23", 
                    windowSec = "30",
                    sampleFrequency = "256",
                    # file = user_model.state_dict(),
                    link = os.path.join(fs.base_location, "cnn", "trained_model_20190610-005842.pth")
                    )
    record.save()

#TODO da finire db 
class CleanTrainingFiles(View):
    def get(self, request):
        UserFiles.objects.all().delete()
        cleanFolder("training")

        return JsonResponse({"message": "deleted user training files in database"}, status = 200)