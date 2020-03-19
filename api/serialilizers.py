from rest_framework import serializers
from post.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [field.name for field in User._meta.fields if field.name != "password"]


class PostSerializers(serializers.ModelSerializer):
    author = UserSerializers()
    class Meta:
        model = Post
        fields = [field.name for field in Post._meta.fields]
