from django.urls import path
from .views import CartApiView, CartDetailApiView, CartCountApiView, CartUpdateApiView, CartDeleteApiView, CartAddApiView

urlpatterns = [
    path('', CartApiView.as_view()),
    path('detail', CartDetailApiView.as_view()),
    path('count', CartCountApiView.as_view()),
    path('update', CartUpdateApiView.as_view()),
    path('delete', CartDeleteApiView.as_view()),
    path('add', CartAddApiView.as_view()),
]