from django import template
from ..models import Post, Category, Tag

register = template.Library()


# 这里我们首先导入 template 这个模块，然后实例化了一个 template.Library 类，并将函数 show_recent_posts
# 装饰为 register.inclusion_tag，这样就告诉 django，这个函数是我们自定义的一个类型为 inclusion_tag 的模板标签。
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    # 这里 Post.objects.dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间（已去重），
    # 且是 Python 的 date 对象，精确到月份，降序排列。
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC')
    }


@register.inclusion_tag('blog/inclusions/_categories.html',takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }


@register.inclusion_tag('blog/inclusions/_tags.html',takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }


















