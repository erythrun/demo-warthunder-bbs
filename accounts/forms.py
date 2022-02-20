from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.forms import User
from .models import User
from captcha.fields import CaptchaField


class signup_form(UserCreationForm):
    email = forms.CharField(label='邮箱', max_length=254, required=True,
                            widget=forms.EmailInput())
    # 必须首字母大写才有中文...
    captcha = CaptchaField(label='验证码', error_messages={"invalid": "验证码错误"})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class new_login_form(AuthenticationForm):
    captcha = CaptchaField(label='验证码', error_messages={"invalid": "验证码错误"})

    class Meta:
        model = User
        fields = ('username', 'password',)
