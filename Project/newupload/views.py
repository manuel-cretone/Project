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

# import sys
# sys.path.insert(0, '../service')

from .service.file_service import *
from .service.statisticService import *


global file_path
file_path = None
# file_path = "C:\\Users\\joyod\\Documents\\Uni\\Project\\Project\\media\\chb01_01.edf"


#view per file upload
@method_decorator(csrf_exempt, name='dispatch')
class Upload(View):
    def post(self, request):
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
            return JsonResponse(file_info(file_path), status = 200)
        else:
            return JsonResponse({"error": "no myfile field"}, status=400)
    
    def get(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)



# def manageParam(request):
#     if request.method == 'POST':
#         channel = request.POST.get("channel", 0)
#         start = request.POST.get("start", 0)
#         len = request.POST.get("len", 30)
#     if request.method == 'GET':
#         channel = request.GET.get("channel", 0)
#         start = request.GET.get("start", 0)
#         len = request.GET.get("len", 30)
#     # return readFile(channel, start, len)
#     return (channel, start, len)

def readParams(request):
    channel = request.GET.get("channel", 0)
    start = request.GET.get("start", 0)
    len = request.GET.get("len", 30)
    return (channel, start, len)

def readFile(channel, start=0, len=None):
    fun = extension_recognise(file_path)
    values = fun(file_path, channel, start, len)

    return values

#view per leggere valori
@method_decorator(csrf_exempt, name='dispatch')
class Values(View):
    def get(self, request):
        channel, start, len = readParams(request)
        values = readFile(channel, start, len)
        data = {
            "file": file_path,
            "canale": channel,
            "inizio":start,
            "dimensione":len,
            "valori": values
        }
        response = JsonResponse(data, status = 200)
        return response

    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)

#view per ottenere statistiche
class Statistics(View):
    def get(self, request):
        channel, start, len = readParams(request)
        values = readFile(channel, start, len)
        data = getStatistic(values)
        response = JsonResponse(data, status = 200)
        return response

    def post(self, request):
        response = {"error": "Method not allowed"}
        return JsonResponse(response, status=405)


#view per ottenere istogramma valori
class histogram(View):
    def get(self, request):
        pass