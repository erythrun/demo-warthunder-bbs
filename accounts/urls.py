'''
@Author: X105E
@Email: NOIR.APTX4869@gmail.com
@Date: 2019-01-08 11:33:55
@LastEditTime: 2019-03-31 15:18:54
@About: 
'''
from django.urls import path
from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
from . import forms


urlpatterns = [
    path('signup/', views.signup, name='signup'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('login/',
    #      auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('login/', auth_views.LoginView.as_view(form_class=forms.new_login_form,template_name='login.html'), name='login'),
    # 2.0后的版本登录限制视图为accounts/login/而不是login/,所以修改了下
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # 这里的登入登出都没有使用到view中的方法
    # 登入模板中传递的next参数,使用自带的方法可以不用管,自动添加重定向
    url(r'reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'reset/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    url(r'reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    url(r'settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    url(r'settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
    url(r'message/',
        views.UserUpdateView.as_view(), name='my_account'),
    url(r'captcha/', include('captcha.urls')),
    path('user_log/<user_pk>/', views.user_log, name='user_log'),
    path('user_log_post/<user_pk>/', views.user_log_post, name='user_log_post'),
    path('collection_log/', views.collection_log, name='collection_log'),
    path('remove_log/<pk>/<topic_pk>/',views.remove_log,name='remove_log'),
]

