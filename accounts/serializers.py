from rest_framework import serializers
from .models import Account
from posts.serializers import PostListSerializer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        # fields = '__all__'
        fields = ['id', 'name', 'age', 'avatar', 'gender', 'email']


class AccountPostsSerializer(serializers.ModelSerializer):
    user_posts = PostListSerializer(many=True)

    class Meta:
        model = Account
        fields = ['id', 'name', 'user_posts']