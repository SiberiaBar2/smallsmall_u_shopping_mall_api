from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from apps.order.models import OrderGoods, Order
from apps.order.serializers import OrderGoodsSerializer, OrderPaymentSerializer
from utils import ResponseMessage


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

    def get(self, request):
        # if not request.user.get("status"):
        #     return JsonResponse(request.user, safe=False)
        email = request.user.get('data').get('username')
        print('email====>', email)
        # email = '4@qq.com'
        pay_status = request.GET.get('pay_status')
        # 返回全部
        if pay_status == '-1':
            db_res = Order.objects.filter(
                email=email,
                is_delete=0
            ).all().order_by('-create_time')
        else:
            db_res = Order.objects.filter(
                email=email,
                is_delete=0,
                pay_status=pay_status
            ).all().order_by('-create_time')

        # 序列化
        db_data = OrderPaymentSerializer(instance=db_res, many=True)

        return ResponseMessage.OrderResponse.success(db_data.data)