#coding:utf-8

from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$',views.index,name='index'),
    # 正则的意思：post/开头，后跟一个至少一位数的数字，并且以/符号结尾
    # [0-9]+表示以为或者多位数，此处（？P<pk>[0-9]+）表示命名捕获组，其作用就是从用户访问的URL里把括号内匹配的字符串捕获
    # 并作为关键字参数传给其对应的视图函数detail
    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),
    # 两个括号括起来的地方是两个命名的参数，Django会从用户访问的URL种自动提取这两个参数的值，
    url(r'archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives,name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$',views.category,name='category'),
]
