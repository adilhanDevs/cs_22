from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Post, Like
from .serializers import (
    PostSerializer,
    LikeSerializer,
    LikeToggleSerializer,
    PostListSerializer,
    PostCreateSerializer,
)


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = PostCreateSerializer(data=data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeAPIView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = LikeToggleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        post = serializer.validated_data['post']
        like_obj = Like.objects.filter(post=post, account=request.user).first()

        if not like_obj:
            Like.objects.create(post=post, account=request.user)
        else:
            like_obj.delete()
            return Response({"message": "Like was delete"}, status=status.HTTP_200_OK)

        return Response({"message": f"Like was created"}, status=status.HTTP_201_CREATED)
