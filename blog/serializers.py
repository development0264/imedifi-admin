from rest_framework import serializers
from .models import Category, Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SerializerBlog(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'