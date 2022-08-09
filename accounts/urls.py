from django.urls import path, include

from . import views
# third pkg
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework import routers

app_name = 'accounts'

router = routers.SimpleRouter()
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', views.TokenJWTView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('register/verify/', views.VerifyAccountView.as_view(), name='verify_account'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_reset'),
    path('password/forget/', views.PasswordForgetView.as_view(), name='password_forget'),
    path('password/forget/verify/', views.PasswordForgetConfirmView.as_view(), name='verify_forget'),
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow_user'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
