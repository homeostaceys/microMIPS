from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static


from . import views

app_name = 'mips'

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^load/$', views.load, name='load'),
    url(r'^inputcode/$', views.inputcode, name='inputcode'),
    url(r'^opcode/$', views.opcode, name='opcode'),
    url(r'^check/$', views.check, name='check'),
    url(r'^reset/$', views.resetindex, name='resetindex'),
    url(r'^pipeline/$', views.pipeline, name='pipeline'),
    url(r'^pipelinemap/$', views.pipelinemap, name='pipelinemap'),
    url(r'^editmem/$', views.editmem, name='editmem'),
    url(r'^editreg/$', views.editreg, name='editreg'),
    url(r'^e404/$', views.error_404, name='404'),
    url(r'^500/$', views.error_500, name='500'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)