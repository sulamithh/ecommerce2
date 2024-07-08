from django.urls import path, include
from .views import UserDetailUpdateDeleteView, RegisterView, ChangePasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import location_view

urlpatterns = [
    path('profile/', UserDetailUpdateDeleteView.as_view(), name='user-detail-update-delete'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('location/', location_view, name='location_view'),
]
