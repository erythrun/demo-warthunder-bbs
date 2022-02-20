from django.contrib import messages
'''
@Author: X105E
@Email: NOIR.APTX4869@gmail.com
@Date: 2018-12-14 09:56:04
@LastEditTime: 2019-01-25 15:41:18
@About: 
'''
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Board, Topic, Post, Picture
# from django.contrib.auth.models import User
# from django.conf import settings
from accounts.models import User
from .forms import new_topic_form, post_form
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import ListView
import datetime
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    boards = Board.objects.all()
    pictures = Picture.objects.all()
    topics = Topic.objects.all().order_by(
        '-last_updated').annotate(replies=Count('posts') - 1)
    # queryset = Topic.objects.all().order_by(
    #     '-last_updated').annotate(replies=Count('posts') - 1)
    # page = request.GET.get('page', 1)
    # paginator = Paginator(queryset, 2)
    # try:
    #     topics = paginator.page(page)
    # except PageNotAnInteger:
    #     topics = paginator.page(1)
    # except EmptyPage:
    #     topics = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'boards': boards, 'pictures': pictures,'topics':topics})
    # 这里的{'boards': boards}用于模板的渲染




def board_topics(request, pk):
    board = Board.objects.get(pk=pk)
    topics = board.topics.order_by(
        '-last_updated').annotate(replies=Count('posts')-1)
    # 统计回复数
    return render(request, 'topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()
    if request.method == 'POST':
        form = new_topic_form(request.POST)
        if form.is_valid():  # 验证表单是否有效
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user  # 字典?
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                # 从提交的form中得到
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
            # return redirect('board_topics', pk=board.pk)  # 重定向到问题页
        # subject = request.POST['subject']
        # message = request.POST['message']
        # user = User.objects.first()  # 临时使用一个账号作为登录用户
        # topic = Topic.objects.create(
        #     subject=subject,
        #     board=board,
        #     starter=user
        # )

    else:  # get请求,直接初始化一个新表单
        form = new_topic_form()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1  # 点击
    topic.save()
    collect_status = False
    try:
        pk = []
        collections = request.user.collection.all()
        for collection in collections:
            pk.append(collection.pk)
        if topic.pk in pk:
            collect_status = True
    except:
        collect_status = False
    # 检查主题是否在收藏里面

    queryset = topic.posts.all().order_by('created_at')
    # 这里的board__pk是外键的反向引用,双下划线跨表查询
    # print(topic)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'topic_posts.html', {'topic': topic, 'posts': posts, 'collect_status': collect_status})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = post_form(request.POST)
        # request后接动作为大写
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = timezone.now()
            topic.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = post_form()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
    # 一个/t 排bug到吐


# 在视图函数replay_topic中，使用topic_pk，因为引用的是函数的关键字参数，
# 而在new_topic视图中，使用的是topic.pk，因为topic是一个对象（Topic模型的实例对象），
# .pk是这个实例对象的一个属性，

# gcbv分页
class topic_list_view(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by(
            '-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class post_list_view(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get(
            'pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset


@method_decorator(login_required, name='dispatch')  # 装饰调度类
class PostUpdateView(UpdateView):  # 编辑功能
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'
    # 如果没有设置context_object_name 来发布，
    # 它将可以被用作：object.topic.board.pk(html文件那里?)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


@login_required
def board_topics_golden(request, pk):
    board = Board.objects.get(pk=pk)
    topics = Topic.objects.filter(board__pk=pk, golden_eagle=True).all().order_by(
        '-last_updated').annotate(replies=Count('posts')-1)
    # topics = get_object_or_404(Topic, board__pk=pk, golden_eagle=True)
    # topics = board.topics.objects.filter(golden_eagle=True).all().order_by(
    #     '-last_updated').annotate(replies=Count('posts')-1)
    # 统计回复数
    return render(request, 'topics_golden.html', {'board': board, 'topics': topics})


@login_required
def collect(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    request.user.collection.add(topic)
    request.user.save()
    messages.success(request, "主题收藏成功")
    return redirect('topic_posts', pk=pk, topic_pk=topic_pk)


@login_required
def remove(request,pk,topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    request.user.collection.remove(topic)
    request.user.save()
    messages.success(request, "主题移除成功")
    return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
