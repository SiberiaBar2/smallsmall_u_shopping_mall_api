from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from apps.comment.models import Comment
from apps.comment.serializers import CommentSerializers
from utils import ResponseMessage

# viewset 解决多个get方法的冲突问题
# Create your views here.
class CommentGenericApiView(
    ViewSetMixin, # 一定要放在最前面 不然会报错 GenericAPIView 也必须继承 需要使用其内部的dispatch
    GenericAPIView,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin
):
    queryset = Comment.objects
    serializer_class = CommentSerializers

    def singer(self, request, pk):
        print('单个')
        return self.retrieve(request, pk)

    def my_list(self, request):
        print('多个')
        return self.list(request)

    def my_edit(self, request, pk):
        print('更新')
        return self.update(request, pk)

    def my_save(self, request):
        print('保存')
        return self.create(request)

    def my_delete(self, request, pk):
        print('删除')
        return self.destroy(request, pk)


class CommentDetailApiView(APIView):
    def get(self, request):
        sku_id = request.GET.get('sku_id')
        page = request.GET.get('page')
        start = (int(page) - 1) * 10
        end = int(page) * 10
        db_comments = Comment.objects.filter(sku_id=sku_id).all()[start:end]
        json_comment = CommentSerializers(instance=db_comments, many=True)
        return ResponseMessage.CommentResponse.success(json_comment.data)


class CommentCountApiView(APIView):
    def get(self, request):
        sku_id = request.GET.get('sku_id')
        db_comment_count = Comment.objects.filter(sku_id=sku_id).count()
        return ResponseMessage.CommentResponse.success(db_comment_count)

