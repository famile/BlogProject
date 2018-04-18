#coding:utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post,Category
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView

# Create your views here.

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    # 这个方法默认获取指定模型的全部列表数据，为了获取指定分类文章列表数据，我们复写该方法
    def get_queryset(self):
        # 在类视图中，从URL捕获的命名组参数保存在实例的kwargs，非命名组参数保存在args，
        # 使用 self.kwargs.get('pk') 来获取从 URL 捕获的分类 id 值
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView,self).get_queryset().filter(category=cate)
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
    post.increase_views()
    # 记得在顶部引入markdown模块
    # 这里我们给markdown渲染函数传递了额外的参数extensions，它是对markdown语法的扩展，这里我们使用了3个扩展，分别是extra（本身包含很多扩展），codehilite（语法高亮扩展），toc（自动生成目录）
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    form = CommentForm()
    # 获取这篇post下的全部评论
    comment_list = post.comment_set.all()

    return render(request,'blog/detail.html',
                  context={
                      'post':post,
                      'form':form,
                      'comment_list':comment_list
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