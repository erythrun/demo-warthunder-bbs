'''
@Author: X105E
@Email: NOIR.APTX4869@gmail.com
@Date: 2018-12-18 15:55:14
@LastEditTime: 2019-01-24 16:04:01
@About: 
'''
from django.urls import path
from django.conf.urls import url, include
from . import views


urlpatterns = [
    path('<pk>/new/', views.new_topic, name='new_topic'),
    path('<pk>/', views.topic_list_view.as_view(), name='board_topics'),
    path('<pk>/topics/<topic_pk>/',
         views.topic_posts, name='topic_posts'),
#     path('<pk>/topics/<topic_pk>/',
#          views.post_list_view.as_view(), name='topic_posts'),
    path('<pk>/topics/<topic_pk>/reply/', views.reply_topic,
         name='reply_topic'),
    path('<pk>/topics/<topic_pk>/posts/<post_pk>/edit/',
         views.PostUpdateView.as_view(), name='edit_post'),
    # url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
    #     views.PostUpdateView.as_view(), name='edit_post'),
    path('<pk>/golden/', views.board_topics_golden,
         name='board_topics_golden'),
    path('<pk>/topics/<topic_pk>/collect/',
         views.collect, name='collect'),
    path('<pk>/topics/<topic_pk>/remove/',views.remove,name='remove'),
]
