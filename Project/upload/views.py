from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import FileSerializer
from .models import File
from .serializer import MySerializer

# Create your views here.
class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class ShowUploadedFiles(APIView):

    def get(self, request):
        ob= File.objects.all()
        print(ob[1])
        # serializzre ob
        file_s = MySerializer(ob[1])
        if file_s.is_valid():
            file_s.save()
            return Response(file_s.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_s.errors, status= status.HTTP_400_BAD_REQUEST)


# class MyView(APIView):
#     parser_classes = (MultiPartParser,)

#     def post(self, request, format=None):
#         # print("DATA",request.data)
#         # print("FILES", request.FILES['file'])
#         file_serializer = MySerializer(request.FILES['file'])
#         if(file_serializer.is_valid()):
#             file_serializer.save()
#             return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)