from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Category")

    def __str__(self):
        return self.category_name


from ckeditor.fields import RichTextField


class Blog(models.Model):
    blog_heading = models.CharField(max_length=50, verbose_name="Blog Heading")
    author = models.CharField(max_length=30, null=True, blank=True, verbose_name="Author")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, name="category")
    subcontent = HTMLField(null=True, blank=True, verbose_name="Sub Content")

    def __str__(self):
        return self.blog_heading
