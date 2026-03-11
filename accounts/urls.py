from django.urls import path
from .views import AccountAPIView, AccountPostAPIView


urlpatterns = [
    path('', AccountAPIView.as_view(), name='accounts'),
    path('<int:pk>', AccountPostAPIView.as_view(), name='account-posts')
]