from django.urls import path, include, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.Upload.as_view(), name="upload_file"),
    path('values', views.Values.as_view(), name="getValues"),
    path('statistics', views.Statistics.as_view(), name="getStatistics"),
    # re_path(r'^getparam/$', views.manageParam, name="manageParam")
]