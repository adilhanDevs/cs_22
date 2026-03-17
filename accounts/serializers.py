from rest_framework import serializers
from .models import Account
from posts.serializers import PostListSerializer


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['id', 'name', 'age', 'avatar', 'gender', 'email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        return Account.objects.create_user(password=password, **validated_data)


class AccountPostsSerializer(serializers.ModelSerializer):
    user_posts = PostListSerializer(many=True)

    class Meta:
        model = Account
        fields = ['id', 'name', 'user_posts']