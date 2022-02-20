from django.urls import path
from django.conf.urls import url, include
from . import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('list/', views.video_list, name='video_list'),
    path('play/<video_pk>/', views.video_play, name='video_play'),

]

