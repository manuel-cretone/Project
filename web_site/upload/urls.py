from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from . import views
from . import chview
from . import templates

urlpatterns = [
    # il nome si riferisce a questo particolare ULR mappato
    path('', views.simple_upload),
    # path('loaded', views.index, name='loaded')
    path('loaded', views.chart, name = 'loaded'),
    # path('ch', views.ch),
    path('ch', views.chart)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
