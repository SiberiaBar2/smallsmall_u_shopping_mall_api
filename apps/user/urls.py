from django.urls import path
from .views import UserApiView, LoginView, UserInfoApiView, UserUpdateApiView, RegisterUserApiView

urlpatterns = [
    path('', UserApiView.as_view()),
    path('login', LoginView.as_view()),
    path('register', RegisterUserApiView.as_view()),
    path('info', UserInfoApiView.as_view()),
    path('update', UserUpdateApiView.as_view()),
]