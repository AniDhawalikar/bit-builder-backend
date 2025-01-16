from django.urls import path
from .views import *

urlpatterns = [
    path('get', sample_get_api, name='signup'),
    path('signup', SignUpAPIView.as_view(), name='signup'),
    path('signin', SignInWithTokenAPIView.as_view(), name='signin'),
    path('reset_password', PasswordResetAPIView.as_view(), name='reset_password'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
]