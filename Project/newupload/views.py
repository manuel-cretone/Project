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
from .models import UserNet, UserFiles, Layer
from django.db.models import Max, Min
import matplotlib.pyplot as plt
from matplotlib import gridspec



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
global model_modular

#TODO da inizializzare None
model_chn = 23
model_winSec = 30
model_sampleFrequency = 256


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
            "valori": values.tolist(),
            "timeScale": timeScale.tolist()
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
        fs = FileSystemStorage()
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
                window.append(values.tolist())
            except Exception as e:
                print("err", e)
                break
        # nChannels = int(len(window))
        data["nChannels"] = channels
        data["window"] = window
        data["timeScale"] = timeScale.tolist()
        
        # window = np.array(window)
        # timeScale = np.array(timeScale)
        # gs = gridspec.GridSpec(channels, 1) 
        # for i in range(channels):
        #     ax0 = plt.subplot(gs[i])
        #     line0, = ax0.plot(timeScale, window[i], linewidth=1)
        # plt.setp(ax0.get_xticklabels(), visible=False)
        # plt.subplots_adjust(hspace=.0)
        # plt.savefig(os.path.join(fs.base_location, "chart", "prova.png"))
        response = JsonResponse(data, status = 200)
        return response

    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)


#view per ottenere statistiche
class Statistics(View):
    def get(self, request):
        channel, start, length = readParams(request)
        values, _ = readFile(file_path, channel, start=0, len=None)
        
        data = getStatistic(values.tolist())
        response = JsonResponse(data, status = 200)
        return response

    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)


#view per ottenere istogramma valori
class Distribution(View):
    def get(self, request):
        channel, start, length = readParams(request)
        values, _ = readFile(file_path, channel, start=0, len=None)
        hist, bins = count_occurrences(values.tolist(), 20) #esempio con parametro 2 
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
        # user_model = ConvNet(model_chn, model_winSec*model_sampleFrequency)
        user_model = model_modular
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
            # torch.save(user_model.state_dict(), os.path.join(fs.base_location, "usermodels", mod_name))
            torch.save(user_model, os.path.join(fs.base_location, "usermodels", mod_name))

            record = UserNet(name=mod_name,
                                    channels=model_chn, 
                                    windowSec = model_winSec,
                                    sampleFrequency = model_sampleFrequency,
                                    # file = user_model.state_dict(),
                                    link = os.path.join(fs.base_location, "usermodels", mod_name)
                                    )
            
            # addDefaultModel()
            record.save()

        except Exception as e:
            print(str(e))
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
                return JsonResponse(data={"error": f"bad window size parameter in {filename}"}, status = 400)
            _, dim = createDataset(filename, base_location, seizureStart, seizureEnd, windowSec, stride)

        #I parametri della rete vengono caricati su variabili globali 
        # -> possibile usare dataset per allenare diverse reti 
        global model_chn
        global model_winSec
        global model_sampleFrequency
        model_chn = channels
        model_winSec = windowSec
        model_sampleFrequency = sampleFrequency

        _ = CleanTrainingFiles.as_view()(self.request)
        response= {
            "channels": int(channels),
            "windowSec": int(windowSec),
            "sampleFrequency": int(sampleFrequency),
            "numberOfWindows": int(dim) 
        }
        return JsonResponse(data=response, status = 200)


    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)




@method_decorator(csrf_exempt, name='dispatch')
class Predict(View):
    def get(self, request):
        model_id = request.GET.get("model_id", None)
        fs = FileSystemStorage()
        # try:
        #     m = UserNet.objects.get(id=model_id)
        # except UserNet.DoesNotExist:
        #     addDefaultModel()
        #     m = UserNet.objects.get(id=0)

        try:
            m = UserNet.objects.get(id=model_id)

            windowSec = int(m.windowSec)
            sampleFrequency = int(m.sampleFrequency)
            windowSize = windowSec * sampleFrequency
            channels =int(m.channels) 
            name = m.name
            model = torch.load(m.link)
        except:
            # addDefaultModel()
            # m = UserNet.objects.get(id=0)
            windowSec = 30
            sampleFrequency = 256
            windowSize = windowSec * sampleFrequency
            channels = 23
            name = "Default"
            model = ConvNet(channels= channels, windowSize = windowSize)      
            model.load_state_dict(torch.load(os.path.join(fs.base_location, "cnn", "trained_model_20190610-005842.pth")))


        
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

        model = model.eval()

        all_signals= []
        for chn in range(channels):
            values_array, _ = readFile(file_path, chn)
            # values_array = np.array(values_array)
            values_matrix = windowGenerator(values_array, windowSize)
            values_tensor = torch.tensor(values_matrix)
            all_signals.append(values_tensor)
        complete_tensor = combineAllTensor(all_signals)

        response = {
            "dim": str(complete_tensor.shape),
            "name": name,
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
                res = 1
            elif(predicted == 0):
                res = 0.5
            response["time"].append(str(i*windowSec))
            response["values"].append(res)
        
        response["seizureWindows"] = seizureWindows
        response["totalWindows"] = complete_tensor.shape[0]
        response["windowSize"] = windowSize
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
        # addDefaultModel()

        return JsonResponse({"message": "no user models in database"}, status = 200)


# def addDefaultModel():
#     fs = FileSystemStorage()
#     record = UserNet(id=0,
#                     name="Default model",
#                     channels="23", 
#                     windowSec = "30",
#                     sampleFrequency = "256",
#                     # file = user_model.state_dict(),
#                     link = os.path.join(fs.base_location, "cnn", "trained_model_20190610-005842.pth")
#                     )
#     record.save()


class CleanTrainingFiles(View):
    def get(self, request):
        UserFiles.objects.all().delete()
        cleanFolder("training")

        return JsonResponse({"message": "deleted user training files in database"}, status = 200)


class AddConvolutionalLayer(View):
    def get(self, request):
        latest = Layer.objects.order_by('-id').values()
        if (latest):
            input = latest[0]['output']
            print("non primo", input)
            last_out = latest[0]['out_dim']
        else:
            #TODO se model_chn è None, non è stato creato il dataset! interrompi
            input = model_chn
            print("primo!", input)
            last_out = model_winSec*model_sampleFrequency
        
        output = int(request.GET.get("output",10))
        kernel = int(request.GET.get("kernel",10))
        stride = int(request.GET.get("stride",1))
        padding = int(request.GET.get("padding",10))
        pool_kernel = int(request.GET.get("pool_kernel",10))
        pool_stride = int(request.GET.get("pool_stride",1))
        out_dim_conv = ((last_out - kernel + 2*padding) / stride) + 1
        out_dim_max = ((out_dim_conv - pool_kernel ) / pool_stride) + 1
        
        if(kernel > last_out+padding or stride > last_out+padding or pool_kernel>out_dim_conv):
            return JsonResponse({"error": "bad parameters"}, status = 400)
        
        record = Layer(
            input = input,
            output = output,
            kernel = kernel,
            stride = stride,
            padding = padding,
            pool_kernel = pool_kernel,
            pool_stride = pool_stride,
            out_dim = out_dim_max
        )
        record.save()

        data = {"message": list(Layer.objects.all().values())}
        return JsonResponse(data = data, status = 200)

#if you set "linear", one more linear layer is added before the final one
class InitializeNet(View):
    def get(self, request):
        linear = request.GET.get("linear", None)
        global model_modular
        model_modular = initializeNet(linear)
        response = {}
        response["modules"] = []
        for param_tensor in model_modular.state_dict():
            response["modules"].append(f"{param_tensor}, {model_modular.state_dict()[param_tensor].size()}")

        _ = CleanLayers.as_view()(self.request)
        return JsonResponse(response, status = 200)


def initializeNet(linear = None):
    layers = Layer.objects.order_by('id')
    conv_list = nn.ModuleList()
    linear_list = nn.ModuleList()
    # conv_dict = nn.ModuleDict()
    # linear_dict = nn.ModuleDict()
    conv_out_dim = None
    
    for i, layer in enumerate(layers):
        seq = nn.Sequential(
            nn.Conv1d(in_channels= layer.input, out_channels = layer.output, kernel_size=layer.kernel, stride=layer.stride, padding=layer.padding),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=layer.pool_kernel, stride=layer.pool_stride)
        )
        conv_out_dim = layer.out_dim
        conv_out_r = layer.output
        conv_list.append(seq)
        # conv_dict.update({str(i): seq})
    linear_input = conv_out_dim * conv_out_r
    try:
        linear = int(linear)
        linear_list.append(nn.Linear(in_features = linear_input, out_features = linear))
        linear_list.append(nn.Linear(in_features = linear, out_features=2))
        # linear_dict.update({"1": nn.Linear(in_features = linear_input, out_features = linear)})
        # linear_dict.update({"2": nn.Linear(in_features = linear, out_features=2)})
    except:
        linear_list.append(nn.Linear(in_features = linear_input, out_features=2))
        # linear_dict.update(("1", nn.Linear(in_features = linear_input, out_features=2)))
    # print("parametri in lista: ", conv_list, linear_list)

    model = ModularConv(conv_list, linear_input, linear_list)
    # print("valori nella rete", model.modules)

    return model     


        

class CleanLayers(View):
    def get(self, request):
        Layer.objects.all().delete()
        return JsonResponse(data = {"message": "all layers deleted"}, status = 200)


