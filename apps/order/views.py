from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from apps.order.models import OrderGoods
from apps.order.serializers import OrderGoodsSerializer


# GenericAPIView 基于 APIView 又做了封装
# Create your views here.
class OrderGoodsGenericApiView(GenericAPIView):
    queryset = OrderGoods.objects
    serializer_class = OrderGoodsSerializer
    # todo 不太理解
    def post(self, request):
        # trade_no = request.data.get('trade_no')
        # self.get_queryset()
        ser = self.get_serializer(data=request.data)
        ser.is_valid()
        ser.save()
        return JsonResponse('ok', safe=False)

