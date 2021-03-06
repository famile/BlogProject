# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
from django.utils.six import python_2_unicode_compatible


# Create your models here.

# 文章(Post) 分类(Category) 标签(tag)


# python_2_unicode_compatible  装饰器用于兼容 Python2
class Category(models.Model):
    """
        Django 要求模型必须继承 models.Model 类。
        Category 只需要一个简单的分类名 name 就可以了。
        CharField 指定了分类名 name 的数据类型，CharField 是字符型，
        CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
        当然 Django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
        Django 内置的全部类型可查看文档：
        https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
        """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# @python_2_unicode_compatible
class Post(models.Model):
    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文, 使用了TextField
    # 存储比较短的字符串使用CharField,但对于文章的正文来说可能是一大段文本,因此使用TextField
    body = models.TextField()

    # excerpt用于存储摘要，通过模型的save方法，在数据被保存到数据库前，先从body字段摘取n个字符保存到excerpt字段中，从而实现自动摘要的目的
    excerpt = models.CharField(max_length=200, blank=True)

    # 这两个分别表示文章的创建时间和最后一次修改时间,存储时间的字段用DateTimeField类型
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要,可以没有文章摘要,但默认情况下CharField 要求我们必须存入数据,否则就会报错
    # 如果CharField的blank=True 参数值后就可以允许空值了
    excerpt = models.CharField(max_length=200, blank=True)

    # 这是分类与标签,分类和标签的模型我们已经定义在上面
    # 我们在这里把文章对应的数据库和分类、标签对应的数据表关联起来,但是关联形式稍微不同
    # 我们规定一边文章只能对应一个分类,但是一个分类可以多篇文章,所以我们使用的是ForeignKey,及一对多的关联关系
    # 对于标签来说,一篇文章可以有多个标签,一个标签可能关联多篇文章,是多对多关系,使用ManyToManyField
    # 同时规定文章可以没有标签,tag指定了blank=True
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者,这里User是从 django.contrib.auth.models 导入的
    # django.contrib.auth 是Django 内置的应用,专门用于处理网站用户的注册、登录等流程,User是Django为我们已经写好的用户模型
    # 这里我们通过ForeighKey 把文章和User关联了起来
    # 因为我们规定一篇文章只能有一个作者,而一个作者可能会写多篇文章,因此这是一对多的关联关系,和Category类型
    author = models.ForeignKey(User)
    # 新增views字段记录阅读量，该类型的值只允许为正整数或0，
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # 'blog:detail' 意思是blog应用下的name=detail的函数，reverse函数会去解析这个视图函数对应的URL
        # Post 的id和pk是等价的
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        # 如果没有摘要
        if not self.excerpt:
            # 首先实例化一个Markdown类，用于渲染body的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将Markdown文本渲染成HTML文本
            # strip_tags去掉HTML文本的全部HTML标签
            # 从文本摘取前54个字符给excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        # 调用父类的save方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time']
