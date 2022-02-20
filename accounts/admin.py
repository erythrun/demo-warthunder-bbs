'''
@Author: X105E
@Email: NOIR.APTX4869@gmail.com
@Date: 2018-12-14 09:56:04
@LastEditTime: 2019-02-19 16:50:29
@About: 
'''
from django.contrib import admin

# Register your models here.
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk','username','desc')
    search_fields = ('pk','username')


admin.site.register(User, UserAdmin)
