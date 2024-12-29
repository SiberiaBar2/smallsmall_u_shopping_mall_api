from django.urls import path
from .views import OrderGoodsGenericApiView

urlpatterns = [
    path('goods', OrderGoodsGenericApiView.as_view()),
]