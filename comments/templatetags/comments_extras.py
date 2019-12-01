from django import template
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None):     # 接受一个Post模型的实例，也可能传递一个评论表单CommentForm的实例，没有就自己创建--复用。
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }
