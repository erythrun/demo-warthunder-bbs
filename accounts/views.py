'''
@Author: X105E
@Email: NOIR.APTX4869@gmail.com
@Date: 2019-01-08 11:34:05
@LastEditTime: 2019-04-01 14:30:12
@About: 
'''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import signup_form,new_login_form
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from .models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from boards.models import Topic
from django.contrib import messages
from django.contrib.auth.views import LoginView



def signup(request):
    # form = UserCreationForm()
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = signup_form(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        # form = UserCreationForm()
        form = signup_form()
    return render(request, 'signup.html', {'form': form})


@method_decorator(login_required, name='dispatch')  # name?
class UserUpdateView(UpdateView):
    model = User
    fields = ('avatar','desc', 'birth_date', 'privacy',)
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user


@login_required
def user_log(request, user_pk):
    user_log = User.objects.get(pk=user_pk)
    if request.user.pk != int(user_pk):
        if user_log.privacy == False:
            return render(request, 'user_log_privacy.html')
    topics = User.objects.get(
        pk=user_pk).topics.all().order_by('-last_updated')
    # posts = User.objects.get(
    #     pk=user_pk).posts.all().order_by('-created_at')
    return render(request, 'user_log.html', {'user_log': user_log, 'topics': topics})


def user_log_post(request,user_pk):
    user_log = User.objects.get(pk=user_pk)
    posts = User.objects.get(
        pk=user_pk).posts.all().order_by('-created_at')
    return render(request, 'user_log_post.html', {'user_log': user_log, 'posts': posts})

@login_required
def collection_log(request):
    pk = []
    # queryset = User.objects.get(pk=request.user.pk).collection.all()
    collections = request.user.collection.all()
    for collection in collections:
        pk.append(collection.pk)
    topics = Topic.objects.filter(pk__in=pk).order_by('-last_updated')
    # return render(request, 'user_collect_log.html')
    return render(request, 'user_collect_log.html',{'topics':topics})


@login_required
def remove_log(request,pk,topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    request.user.collection.remove(topic)
    request.user.save()
    messages.success(request, "主题移除成功")
    return redirect('collection_log')


class new_login(LoginView):
    form_class = new_login_form
    template_name = 'login.html'
