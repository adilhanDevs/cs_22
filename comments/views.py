from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Comment
from .serializers import CommentCreateSerializer, CommentSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
	queryset = Comment.objects.select_related('account', 'post').all()
	permission_classes = [permissions.IsAuthenticated]

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return CommentCreateSerializer
		return CommentSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if not serializer.is_valid():
			print("Serializer errors:", serializer.errors)
			return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

		comment = serializer.save(account=request.user)
		return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
