'''
@Author: APTX
@Email: NOIR.APTX4869@gmail.com
@Date: 2019-01-08 11:34:36
@LastEditTime: 2019-02-14 15:27:49
@About: 
'''
from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from boards.models import Topic

class User(AbstractUser):
    desc = models.CharField(max_length=50, null=True,default="他很懒，什么都没写",
                            blank=True, verbose_name='个性签名')
    location = models.CharField(max_length=30, null=True,blank=True, verbose_name='所在地')
    birth_date = models.DateField(null=True,blank=True, verbose_name='生日')
    avatar = ProcessedImageField(upload_to='avatar',
                                 null=True, blank=True,
                                 verbose_name='头像',
                                 #图片将处理成85x85的尺寸
                                 processors=[ResizeToFill(85, 85)],)

    collection = models.ManyToManyField(Topic, null=True, blank=True)
    privacy = models.BooleanField(default=True, verbose_name='是否允许他人查看历史记录？')
    class Meta:
       verbose_name = '用户'

