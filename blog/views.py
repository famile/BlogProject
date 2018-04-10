#coding:utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post,Category
import markdown

# Create your views here.

#
def index(request):

    # order_by(排序) -(逆序) created_time(文章的创建时间)
    post_list = Post.objects.all().order_by('-created_time')
    # render 这个函数根据根据我们传入的参数来构造httpResponse
    return render(request,'blog/index.html',context={
        'post_list':post_list
    })

#
def detail(request,pk):
    # 这里我们引入get_object_or_404方法，其作用就是当传入pk对应的Post在数据库存在时，就返回对应的post，如果不存在就给用户染回一个404错误
    post = get_object_or_404(Post,pk=pk)
    # 记得在顶部引入markdown模块
    # 这里我们给markdown渲染函数传递了额外的参数extensions，它是对markdown语法的扩展，这里我们使用了3个扩展，分别是extra（本身包含很多扩展），codehilite（语法高亮扩展），toc（自动生成目录）
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    return render(request,'blog/detail.html',
                  context={
                      'post':post,
                  })

# 归档
def archives(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def category(request, pk):

    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})