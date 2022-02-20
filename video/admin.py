#!/usr/bin/env python
# coding=UTF-8
'''
@Author: APOTOXIN4869
@Email: NOIR.APTX4869@gmail.com
@About: 
@Date: 2018-12-25 17:24:30
@LastEditTime: 2019-02-20 15:43:04
'''
from django.contrib import admin
from .models import Video,Comment
# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    # 定义admin总览里每行的显示信息
    list_display = ('pk', '__str__', 'video', 'created_by')
    # 定义搜索框以哪些字段可以搜索
admin.site.register(Video)
admin.site.register(Comment,CommentAdmin)
