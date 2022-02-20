'''
@Author: APTX
@Email: NOIR.APTX4869@gmail.com
@Date: 2019-01-09 10:48:01
@LastEditTime: 2019-02-20 14:33:25
@About: 
'''
from django.db import models
# from django.contrib.auth.models import User
from django.utils.text import Truncator
# 一个工具类
from django.utils.html import mark_safe, strip_tags
from markdown import markdown
from django.conf import settings
from .xss import xss
from django.core import validators


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True,
                            verbose_name='名字')  # 设置唯一
    desc = models.CharField(max_length=300, verbose_name='描述')

    class Meta:
        verbose_name = '标签'

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()-1
        # 得到一个板块的所有回复数

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()
        # created_at前面加-表示倒排


class Topic(models.Model):
    subject = models.CharField(max_length=255, verbose_name='标题')
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(
        Board, related_name='topics', on_delete=models.CASCADE, verbose_name='所属标签')
    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='topics', on_delete=models.CASCADE, verbose_name='题主')
    #   不添加on_delete 级联更新会显示错误
    #   related_name='topics' 反向使用,如Board.topics
    views = models.PositiveIntegerField(default=0, verbose_name='点击')
    # 点击次数
    message = models.TextField(max_length=4000, null=True, verbose_name='内容')
    golden_eagle = models.BooleanField(default=False)

    def __str__(self):
        truncated_message = Truncator(self.subject)
        return truncated_message.chars(30)

    class Meta:
        verbose_name = '主题'

    def post_count(self):
        return Post.objects.filter(topic__pk=self.pk).count()-1

    def get_last_post(self):
        return Post.objects.filter(topic__pk=self.pk).order_by('-created_at').first()


class Post(models.Model):
    message = models.TextField(max_length=4000, verbose_name='内容')
    topic = models.ForeignKey(
        Topic, related_name='posts', on_delete=models.CASCADE, verbose_name='所属主题')
    created_at = models.DateTimeField(auto_now_add=True)  # 选择当前日期和时间
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE, verbose_name='答主')
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name='+', on_delete=models.CASCADE)
    # related_name 设置为'+'时表示不需要反向

    class Meta:
        verbose_name = '回复'

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
        # 将一个长字符串截取为任意长度字符的简便方法

    def get_message_as_markdown(self):
        # return mark_safe(markdown(self.message, safe_mode=True))
        return mark_safe(markdown(xss(self.message), safe_mode='escape'))


class Picture(models.Model):
    src = models.FileField(upload_to='picture/%Y/%m', null=True, blank=True, verbose_name='轮播图片',
                           validators=[validators.FileExtensionValidator(['jpg', 'png'],
                                                                         message='必须为jpg, png格式的文件')])
    link = models.CharField(max_length=255, verbose_name='链接', default='#')
    title = models.CharField(max_length=255, verbose_name='介绍', default='None')

    class Meta:
        verbose_name = '轮播图'

    def __str__(self):
        return self.title
