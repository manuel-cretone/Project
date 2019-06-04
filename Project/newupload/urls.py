from django.urls import path, include, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.Upload.as_view(), name="upload_file"),
    path('values/', views.Values.as_view(), name="getValues"),
    path('complete/', views.CompleteWindow.as_view(), name="completeWindow"),
    path('statistics/', views.Statistics.as_view(), name="getStatistics"),
    path('distribution/', views.Distribution.as_view(), name="distribution"),
    # path('predict/', views.Predict.as_view(), name="predict"),
    path('uptraining/', views.UploadTraining.as_view(), name = "uptraining"),
    path('convert/', views.ConvertDataset.as_view(), name="convert"),
    path('train/', views.Train.as_view(), name = "train")
    # re_path(r'^getparam/$', views.manageParam, name="manageParam")
]