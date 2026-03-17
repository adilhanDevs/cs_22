from rest_framework import serializers
from .models import Post, Like
from comments.serializers import CommentSerializer


class PostListSerializer(serializers.ModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(view_name='post-detail')

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'image', 'created_at', 'detail_url', 'user']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'user']


class PostSerializer(serializers.ModelSerializer):
    post_comments = CommentSerializer(many=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "description", "image", "created_at", "post_comments", "likes_count"]

    def get_likes_count(self, obj):
        return obj.post_likes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'