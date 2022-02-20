from django import forms
from .models import Topic, Post


class new_topic_form(forms.ModelForm):
    # Django 使用两种类型的 form：forms.Form 和 forms.ModelForm。Form 类是通用的表单实现。
    # 可以使用它来处理与应用程序 model 没有直接关联的数据。ModelForm 是 Form 的子类，它与 model 类相关联。
    # message = forms.CharField(widget=forms.Textarea(
    #     attrs={'rows': 4, 'placeholder': '你想发表什么呢'}
    # ),
    #     max_length=4000)
    # widget是插件,现在属性为文本框
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update(
            {'rows': 8,  'id': 'md_editor'})

    class Meta:
        model = Topic
        fields = ['subject', 'message']
        # 表单类与数据库类?所以不分开定义直接在这里引用吗
        # message在原Topic中不存在,为额外字段
        # 11.27更新,已追加


class post_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update(
            {'placeholder': '填入你的回复吧', 'id': 'md_editor'})
        # 设置form 的属性

    class Meta:
        model = Post
        fields = ['message', ]
        # 定义到fields中的都为表单处理,上面也一样
