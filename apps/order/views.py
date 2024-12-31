from datetime import datetime

from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from apps.cart.models import Cart
from apps.order.models import OrderGoods, Order
from apps.order.serializers import OrderGoodsSerializer, OrderPaymentSerializer, OrderSerializer
from utils import ResponseMessage


# GenericAPIView 基于 APIView 又做了封装
# Create your views here.
# 生成订单号
class OrderGoodsGenericApiView(GenericAPIView):
    queryset = OrderGoods.objects
    serializer_class = OrderGoodsSerializer
    # todo 不太理解
    def post(self, request):
        # trade_no = request.data.get("trade_no")
        # print(self.get_queryset())
        # print(self.get_serializer())
        print(request.data)
        ser = self.get_serializer(data=request.data)
        ser.is_valid()
        ser.save()
        return JsonResponse("ok",safe=False)
    def get(self, request, trade_no):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        print('trade_no=====>', trade_no)

        email = request.user.get("data").get("username")
        db_result = Order.objects.filter(email=email, trade_no=trade_no, is_delete=0).first()
        db_ser = OrderPaymentSerializer(instance=db_result)
        return ResponseMessage.OrderResponse.success(db_ser.data)

class OrderCreateApiView(GenericAPIView):
    queryset = Order.objects
    serializer_class = OrderSerializer
    def post(self, request):
        # trade_no = request.data.get('trade_no')
        # self.get_queryset()
        email = request.user.get('data').get('username')
        print('email====>', email)
        import time
        trade_no = int(time.time()*1000)
        request_data = request.data
        trade_data = request_data['trade']
        goods_data = request_data['goods']
        trade_data['trade_no'] = trade_no
        trade_data['email'] = email
        trade_data['pay_status'] = 0
        trade_data['is_delete'] = 0
        trade_data['create_time'] = datetime.now()
        # 要保存的是订单的信息
        ser = self.get_serializer(data=trade_data)
        ser.is_valid()
        ser.save()

        goods_order_data = {}
        # 循环一次 保存到ordergoods一次 从购物车删除一次
        for data in goods_data:
            goods_order_data['trade_no'] = trade_no
            goods_order_data['sku_id'] = data['sku_id']
            goods_order_data['goods_num'] = data.get('nums')
            if goods_order_data['goods_num'] is None:
                goods_order_data['goods_num'] = data.get('goods_nums')
            OrderGoods.objects.create(**goods_order_data)
            # 这里记得要加email sku_id可能重复 要表示是谁的商品
            Cart.objects.filter(sku_id=goods_order_data['sku_id'], email=trade_data['email']).update(is_delete=1)

        return ResponseMessage.CartResponse.success(ser.data)

class OrderInfoApiView(GenericAPIView):
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

class OrderDetailGenericAPIView(GenericAPIView):
    queryset = Order.objects
    serializer_class = OrderSerializer

    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user,safe=False)
        trade_no = request.data.get('trade_no')
        print(' self.get_queryset()',  self.get_queryset()) # order.Order.objects
        self.get_queryset().filter(trade_no=trade_no).update(**request.data)
        return ResponseMessage.OrderResponse.success('ok')