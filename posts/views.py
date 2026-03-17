from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer, PostListSerializer, PostCreateSerializer
from accounts.models import Account


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['user'] = request.user.id
        serializer = PostCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeAPIView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        try:
            post = request.data['post']
            account = request.data['account']

            post = Post.objects.get(id=post)
            account = Account.objects.get(id=account)
            like_obj = Like.objects.filter(post=post, account=account).first()
        except Exception as e:
            return Response({"message": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

        if not like_obj:
            Like.objects.create(post=post, account=account)
        else:
            like_obj.delete()
            return Response({"message": "Like was delete"}, status=status.HTTP_200_OK)

        return Response({"message": f"Like was created"}, status=status.HTTP_201_CREATED)
