from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    account_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'text', 'account_name']

    def get_account_name(self, obj):
        return obj.account.name


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'post']

    def validate_text(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Comment text cannot be empty.')
        return value
