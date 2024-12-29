from django.urls import path
from .views import GoodsGategoryApiView, GoodsDetailApiView, GoodsFindAPIView, GoodsSearchApiView, GoodsKeywordCountApiView

urlpatterns = [
    path('find', GoodsFindAPIView.as_view()),
    path('keyword/count/<str:keyword>', GoodsKeywordCountApiView.as_view()),
    path('category/<int:category_id>/<int:page>', GoodsGategoryApiView.as_view()),
    path('search/<str:keyword>/<int:page>/<int:order_by>', GoodsSearchApiView.as_view()),
    path('<str:sku_id>', GoodsDetailApiView.as_view()),
    # path('find', GoodsFindAPIView.as_view()), #  这个容易匹配到上面 所以写到最上面
]