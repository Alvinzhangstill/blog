from django import forms
from .models import Comment


# django表单类
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','url','text']    # ？？ Django会自动将fields中声明的模型字段设置为表单的属性



