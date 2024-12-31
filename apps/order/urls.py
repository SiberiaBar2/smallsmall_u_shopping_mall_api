from django.urls import path, re_path
from .views import OrderGoodsGenericApiView, OrderInfoApiView, OrderCreateApiView, OrderDetailGenericAPIView

urlpatterns = [
    path('create', OrderCreateApiView.as_view()),
    path('goods', OrderGoodsGenericApiView.as_view()),
    path('update', OrderDetailGenericAPIView.as_view()),
    path('info', OrderInfoApiView.as_view()),
    re_path("goods/(?P<trade_no>.*)",OrderGoodsGenericApiView.as_view()),
]