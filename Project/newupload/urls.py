from django.urls import path, include, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.upload_file, name="upload_file"),
    # path('getj/', views.getJson, name="getJson"),
    path('getvalues/', views.getValues, name="getValues")
    # re_path(r'^getparam/$', views.manageParam, name="manageParam")
]