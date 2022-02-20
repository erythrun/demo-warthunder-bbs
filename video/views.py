'''
@Author: APTX
@Email: NOIR.APTX4869@gmail.com
@Date: 2018-12-18 20:35:16
@LastEditTime: 2019-01-13 13:29:59
@About: 
'''
from django.shortcuts import render, get_object_or_404, redirect
from .models import Video,Comment
from django.contrib.auth.decorators import login_required
from .forms import comment_form

def video_list(request):
    videos = Video.objects.all().order_by('-upload_at')
    return render(request, 'video_list.html', {'videos': videos})


@login_required
def video_play(request, video_pk):
    video = get_object_or_404(Video, pk=video_pk)
    video.views += 1
    video.save()
    if request.method == 'POST':
        form = comment_form(request.POST)
        # re_form = comment_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.video = video
            comment.created_by = request.user
            comment.save()
            return redirect('video_play', video_pk=video_pk)


    else:
        re_form = comment_form()
        return render(request, 'video_play.html', {'video': video,'form':re_form})


def new_comment(request):
    if request.method == 'POST':
        pass
    else:
        form = comment_form()
        return render(request,'video')
