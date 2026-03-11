from rest_framework import generics
from .serializers import AccountSerializer, AccountPostsSerializer
from .models import Account


class AccountAPIView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountPostAPIView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountPostsSerializer