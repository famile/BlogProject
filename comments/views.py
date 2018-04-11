#coding:utf-8
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request,post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来
    # 这里我们使用了Django提供的一个快捷函数 get_object_or_404
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回404页面给用户
    post = get_object_or_404(Post, pk=post_pk)
    # 只有当用户请求为POST 时才处理表单数据
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象
        # 我们利用这些数据构造CommentForm的实例，这样Django的表单就生成了
        form = CommentForm(request.POST)

        # 调用form.is_valid()方法时，Django自动帮我们检查表单的数据是否符合格式要求
        if form.is_valid():
            # 检查到数据是合法的，调用表单的save方法保存数据到数据库
            # commit=False 的作用是仅仅利用表单的数据生成Comment模型类的实例，但还不保存评论到数据库
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来
            comment.post = post

            comment.save();

            # 重定向到post的详情页，实际上当redirect函数接受一个模型的实例时，它会调用这个模型实例的get_absolute_url方法，
            # 然后重定向到get_absolute_url方法返回的URL
            return redirect(post)
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误
            # 因此传三个模板变量给detail.html
            # 一个是文章Post 一个是评论列表 一个是表单form
            # 这里我们用的是post.comment_set.all() 方法，这个方法类似 Post.object.all() 其作用是获取post下的全部评论
            # Post和Comment是ForeighKey关联的，所以使用post.comment_set.all()反向查询全部评论
            comment_list = post.comment_set.all()
            context = {'post':post,
                       'form':form,
                       'comment_list':comment_list
                       }
            return render(request,'blog/detail.html',context=context)
    # 不是post请求，说用用户没有提交数据，重定向到文章详情页
    return redirect(post)
