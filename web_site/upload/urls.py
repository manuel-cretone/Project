from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    # il nome si riferisce a questo particolare ULR mappato
    path('', views.index, name='index'),
    path('update', views.simple_upload, name='loaded')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
