from django.contrib import admin
from .models import Post,Category,Tag
import sys

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
reload(sys)
sys.setdefaultencoding('utf-8')
