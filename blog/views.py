import markdown,re
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Category,Tag
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# Create your views here.


def index(request):

    post_list = Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})


def detail(request,pk):
    # post = get_object_or_404(Post,pk=pk)        # 从 django.shortcuts 模块导入的 get_object_or_404 方法
    # post.body = markdown.markdown(post.body,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc'
    #                               ])
    # return render(request,'blog/detail.html',context={'post':post})

    post = get_object_or_404(Post,pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify)

    ])
    post.body = md.convert(post.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>',md.toc,re.S)   # 看不懂这句
    post.toc = m.group(1) if m is not None else ''

    return render(request,'blog/detail.html',context={'post':post})


def archive(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})


def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})


def tag(request,pk):
    t = get_object_or_404(Tag,pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

