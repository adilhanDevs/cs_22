from rest_framework import serializers
from .models import Account
from posts.serializers import PostListSerializer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'age', 'avatar', 'gender', 'email', 'username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        obj = Account.objects.create_user(username, password)
        obj.save()
        return obj


class AccountPostsSerializer(serializers.ModelSerializer):
    user_posts = PostListSerializer(many=True)

    class Meta:
        model = Account
        fields = ['id', 'name', 'user_posts']