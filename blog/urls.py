"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from accounts.views import AccountAPIView, AccountPostAPIView
from comments.views import CommentListCreateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

api_urlpatterns = [
    path('', include('posts.urls')),
    path('accounts/', include('accounts.urls')),
    path('comments/', include('comments.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts', AccountAPIView.as_view(), name='accounts-no-slash'),
    path('api/accounts/<int:pk>', AccountPostAPIView.as_view(), name='account-posts-no-slash'),
    path('api/comments', CommentListCreateAPIView.as_view(), name='comment-list-no-slash'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair_no_slash'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh_no_slash'),
    path('api/', include(api_urlpatterns))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
