'''
@Author: APTX
@Email: NOIR.APTX4869@gmail.com
@Date: 2018-12-18 20:35:16
@LastEditTime: 2019-04-01 16:03:03
@About: 
'''
from django.db import models
from django.conf import settings
from django.utils.html import mark_safe
from markdown import markdown
from django.utils.text import Truncator
from django.core import validators


class Video(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    author = models.CharField(max_length=50, null=True,
                              blank=True, default='V.A.', verbose_name='作者')
    desc = models.TextField(max_length=300, null=True,
                            blank=True, verbose_name='简介')
    src = models.FileField(upload_to='video/%Y/%m',
                           null=True, blank=True, verbose_name='上传视频',
                           validators=[validators.FileExtensionValidator(['mkv', 'mp4'],
                                                                         message='必须为mkv,mp4格式的文件')])
    out_src = models.CharField(
        max_length=300, null=True, blank=True, verbose_name='外链视频', default='null')
    poster = models.FileField(upload_to='video/%Y/%m',
                              null=True, blank=True, verbose_name='封面')
    upload_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='videos', on_delete=models.CASCADE, verbose_name='上传id')
    upload_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    views = models.PositiveIntegerField(default=0, verbose_name='播放量')

    def __str__(self):
        return self.title

    def shot_desc(self):
        truncated_message = Truncator(self.desc)
        return truncated_message.chars(30)

    class Meta:
        verbose_name = '视频'


class Comment(models.Model):
    comment = models.TextField(max_length=4000, verbose_name='评论')
    video = models.ForeignKey(
        Video, related_name='comments', on_delete=models.CASCADE, verbose_name='所属视频')
    created_at = models.DateTimeField(auto_now_add=True)  # 选择当前日期和时间
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='video_posts', on_delete=models.CASCADE,verbose_name='用户')

    class Meta:
        verbose_name = '评论'

    def __str__(self):
        truncated_message = Truncator(self.comment)
        return truncated_message.chars(30)

    # def __str__(self):
    #     truncated_message = Truncator(self.message)
    #     return truncated_message.chars(30)
        # 将一个长字符串截取为任意长度字符的简便方法

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.comment, safe_mode='escape'))
