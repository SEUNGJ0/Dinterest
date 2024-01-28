from django.urls import path
from App_Auth.Auth_views import UserListView, UserDetailView, JWTSignupView, JWTLoginView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView
app_name = "App_Auth"

urlpatterns = [
    path('user/', UserDetailView.as_view(), name='user-detail-view'),
    path('users/', UserListView.as_view(), name='users-list-view'),
    path('signup/', JWTSignupView.as_view(), name='jwt-signup-view'),
    path('login/', JWTLoginView.as_view(), name='jwt-login-view'),
    path('logout/', LogoutView.as_view(), name='logout-view'),

    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
]