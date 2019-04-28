from django.urls import path
from .views import *

urlpatterns = [
    path('', FileUploadView.as_view()),
    path('prova', ShowUploadedFiles.as_view())
]