from django.contrib import admin
from .models import Blog, Category


# Register your models here.

class admin_category(admin.ModelAdmin):
    list_display = ['blog_heading', 'category']
    list_filter = ['category']


admin.site.register(Blog, admin_category)
admin.site.register(Category)
