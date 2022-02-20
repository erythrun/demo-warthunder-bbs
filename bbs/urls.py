'''
@Author: X105E
@Email: NOIR.APTX4869@gmail.com
@Date: 2019-01-09 10:48:01
@LastEditTime: 2019-01-24 15:18:24
@About: 
'''
"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from boards import views
from accounts import views as accounts_views
# as 引入别名,防止冲突
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import settings
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    url('^$', views.home, name='home'),
    # 正则,^表示开始,$表示结束,匹配空行
    url('^accounts/',include('accounts.urls')),
    url('^video/',include('video.urls')),
    url('^boards/',include('boards.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
