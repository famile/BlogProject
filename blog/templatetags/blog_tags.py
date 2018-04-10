#coding:utf-8

from django import template
from ..models import Post, Category

register = template.Library()

# 这个函数功能就是获取数据库前num篇文章

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag
def archives():
    # order='DESC' 表明降序排列（即离当前越近的时间越排在前面）
    return Post.objects.dates('created_time','month',order='DESC')

@register.simple_tag
def get_categories():
    # 别忘了在顶部引入Category类
    return Category.objects.all();