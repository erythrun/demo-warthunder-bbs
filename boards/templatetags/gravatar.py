'''
@Author: APTX
@Email: NOIR.APTX4869@gmail.com
@Date: 2018-12-15 13:26:58
@LastEditTime: 2019-01-20 14:02:20
@About: 
'''
from django.utils.html import strip_tags  # 去掉所有html标签
import markdown
import hashlib
from urllib.parse import urlencode
from django import template
from django.conf import settings
import hashlib

register = template.Library()


@register.filter(name="gravatar")
def gravatar(user):
    email_hash = hashlib.md5("{}".format(user.email).encode("utf-8")).hexdigest()
    url = 'http://www.gravatar.com/avatar/{}?s={}&d={}'.format(
        email_hash, 160, 'robohash')
        # 风格类型:identicon、monsterid、wavatar、retro、robohash
    return url
#     email = user.email
#     g = Gravatar(email)
#     url = g.get_image(size=80, default='', force_default=False,
#                       rating='', filetype_extension=False, use_ssl=False)
#     return url
# @register.filter(name="gravatar")
# def gravatar(user):
#     email = user.email.lower().encode('utf-8')
#     default = 'mm'
#     size = 256
#     url = 'https://www.gravatar.com/avatar/{md5}?{params}'.format(
#         md5=hashlib.md5(email).hexdigest(),
#         params=urlencode({'d': default, 's': str(size)})
#     )
#     return url









