from django import forms
from .models import Comment


class comment_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update(
            {'rows': 4, 'placeholder': '填入你的评论吧'})

    class Meta:
        model = Comment
        fields = ['comment', ]
