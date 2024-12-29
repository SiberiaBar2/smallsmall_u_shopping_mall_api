from django.urls import path, re_path
from .views import CommentGenericApiView, CommentDetailApiView, CommentCountApiView

urlpatterns = [
    path('detail', CommentDetailApiView.as_view()),
    path('count', CommentCountApiView.as_view()),
    path('', CommentGenericApiView.as_view({
        'get': 'my_list', # ViewSetMixin 要最先继承 这里传参了 下面也必须传；GenericAPIView 也必须第二个继承 需要使用其内部的dispatch
        'post': 'my_save',
    })),
    re_path('(?P<pk>.*)', CommentGenericApiView.as_view({
        'get': 'singer',
        'post': 'my_edit',
        'delete': 'my_delete'
    })),
]