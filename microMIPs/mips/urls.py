from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static


from . import views

app_name = 'mips'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^load/$', views.load, name='load'),
    url(r'^inputcode/$', views.inputcode, name='inputcode'),
    url(r'^check/$', views.check, name='check'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)