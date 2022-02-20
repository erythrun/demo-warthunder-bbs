'''
@Author: X105E
@Email: NOIR.APTX4869@gmail.com
@Date: 2018-12-24 10:54:57
@LastEditTime: 2019-02-20 14:35:41
@About: 
'''
from django.contrib import admin
from .models import Board,Topic,Post,Picture


class TopicAdmin(admin.ModelAdmin):
    # 定义admin总览里每行的显示信息
    list_display = ('pk','subject', 'board', 'starter')
    # 定义搜索框以哪些字段可以搜索
    search_fields = ('subject', 'message')

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk','__str__','topic','created_by')
    search_fields = ('message',)

# 引用的固定格式，注册的model和对应的Admin，Admin放在后边
# 同样还有noregister方法：比如admin.site.noregister(Group)，把group这个表在admin中去掉（默认user和group都是注册到admin中的）
admin.site.register(Board)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Picture)
# Register your models here.
