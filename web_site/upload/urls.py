from django.urls import path
from . import views

urlpatterns = [
    # il nome si riferisce a questo particolare ULR mappato
    path('', views.index, name='index'),
]
