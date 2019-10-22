from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name    # 后面看看这有什么用


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多
    """
    # 文章标题
    title = models.CharField('标题',max_length=70)

    # 正文
    body = models.TextField('正文')

    # 创建时间和最后一次修改时间，存储时间的字段用DateTimeField类型
    created_time = models.DateTimeField('创建时间',default=timezone.now)
    modified_time = models.DateTimeField('修改时间')

    # 文章摘要
    excerpt = models.CharField('摘要',max_length=200, blank=True)  # CharField要求不能为空，设置blank=True后就可以为空了

    # 一篇文章只能对应一个分类，一个分类下可以有多篇文章，一对多
    category = models.ForeignKey(Category, verbose_name='分类',on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,verbose_name='标签', blank=True)  # 多对多，文章可以没有标签

    # 文章作者，User从 django.contrib.auth.models 导入
    # django.contrib.auth 是django内置的应用，专门用于处理网站用户的注册、登陆等流程，User是django为我们专门写好的用户模型
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)  # 文章与作者的关系，一对多

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):   # 重写save方法，每次修改，保存当次时间信息
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt   (很多网站都采用这样一种生成摘要的方式)
        self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})    # 不懂这种用法



