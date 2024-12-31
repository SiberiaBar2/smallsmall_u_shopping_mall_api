from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from datetime import datetime

from apps.order.models import Order
from apps.pay.alipay import AliPay
from utils import ResponseMessage


# Create your views here.
class ToAliPayPageAPIView(APIView):
    def post(self, request):
        try:
            trade_no = request.data.get("tradeNo")
            total_amount = request.data.get("orderAmount")
            print('trade_no', trade_no, 'total_amount', total_amount)
            alipay = AliPay()
            url = alipay.direct_pay(
                out_trade_no=trade_no,
                subject="主题:" + trade_no,
                total_amount=total_amount,
            )
            re_url = alipay.gateway + "?{data}".format(data=url)
            return ResponseMessage.AliPayResponse.success({"alipay": re_url})
        except Exception as e:
            print('eeeee', e)

            return JsonResponse({"alipay": 'error'})

class AlipayAPIView(APIView):
    def get(self, request):
        processed_dict = {}
        for k,v in request.GET.items():
            processed_dict[k] = v
        sign = processed_dict.pop("sign",None)
        alipay = AliPay()
        is_verify = alipay.verify(processed_dict, sign)
        if is_verify is True:
            trade_no = processed_dict.get('out_trade_no')
            ali_trade_no = processed_dict.get('trade_no')
            # 0待支付  1 待确认  2支付完成  3 已完成
            pay_status = 2
            Order.objects.filter(trade_no=trade_no).update(
                ali_trade_no=ali_trade_no,
                pay_status=pay_status,
                pay_time=datetime.now()
            )
        return redirect("http://localhost:5173/profile/3")

    def post(self,request):
        processed_dict = {}
        for k, v in request.POST.items():
            processed_dict[k] = v
        sign = processed_dict.pop("sign", None)
        alipay = AliPay()
        is_verify = alipay.verify(processed_dict, sign)
        if is_verify is True:
            trade_no = processed_dict.get('out_trade_no')
            ali_trade_no = processed_dict.get('trade_no')
            # 0待支付  1 待确认  2支付完成  3 已完成
            pay_status = 2
            Order.objects.filter(trade_no=trade_no).update(
                ali_trade_no=ali_trade_no,
                pay_status=pay_status,
                pay_time=datetime.now()
            )
        return redirect("http://localhost:5173/profile/3")