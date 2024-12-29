import json

from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from apps.cart.models import Cart
from apps.cart.serializers import CartSerializers, CartDetailSerializers
from utils import ResponseMessage

# Create your views here.
# 购物车接口
class CartApiView(APIView):
    #  @todo 需要补充登录验证
    def post(self, request):
        request_data = request.data
        print(request_data, type(request_data))
        # email = request_data.get('email')
        email = request.user.get("data").get("username")
        print('email', email)

        sku_id = request_data.get('sku_id')
        nums = request_data.get('nums')
        # 删除
        is_delete = request_data.get('is_delete')

        # 判断数据是否存在 存在更新 不存在插入
        data_exists = Cart.objects.filter(
            email=email,
            is_delete=0, # 0表示这条数据没有删除
            sku_id=sku_id
        )

        print('data_exists.exists()', data_exists.exists())
        if data_exists.exists():
            exists_cart_data = data_exists.get(
                    email=email,
                    is_delete=0,
                    sku_id=sku_id
                )
            if is_delete == 0:
                new_nums = nums + exists_cart_data.nums
                request_data['nums'] = new_nums
            #     todo  这里为什么数据库是啥就取啥？
            elif is_delete == 1:
                request_data['nums'] = exists_cart_data.nums
            #  反序列化
            cart_ser = CartSerializers(data=request_data)
            cart_ser.is_valid(raise_exception=True)
            #   更新
            Cart.objects.filter(
                email=email,
                is_delete=0,
                sku_id=sku_id
            ).update(**cart_ser.data)
            if is_delete == 0:
                return ResponseMessage.CartResponse.success('更新成功')
            elif is_delete == 1:
                return ResponseMessage.CartResponse.success('删除成功')
        else:
            # 插入逻辑
            cart_ser = CartSerializers(data=request_data)
            # 必须要进行验证
            cart_ser.is_valid(raise_exception=True)
            Cart.objects.create(**cart_ser.data)
            # return HttpResponse('插入成功')
            return ResponseMessage.CartResponse.success('插入成功')
        # return HttpResponse('ok')

    def get(self, request):
        email = request.GET.get('email')
        cart_result = Cart.objects.filter(
            email=email,
            is_delete=0, # 0表示未删除
        )

        # 序列化
        cart_ser = CartSerializers(instance=cart_result, many=True)
        # return JsonResponse(cart_ser.data, safe=False)
        # return JsonResponse(cart_ser.data)
        return ResponseMessage.CartResponse.success(cart_ser.data)

# 利用序列化器进行多表联查
class CartDetailApiView(APIView):
    def post(self, request):
        # if not request.user.get("status"):
        #     return JsonResponse(request.user,safe=False)
        email = request.user.get("data").get("username")
        request_data = json.loads(request.body)
        request_data['sku_id'] = request_data.get('sku_id', '')

        # 查单个
        if request_data['sku_id']:
            filters = {
                'sku_id': request_data['sku_id'],
                'email': email,
                'is_delete': 0,
            }
            db_cart_detail = Cart.objects.filter(**filters)
            db_data = CartDetailSerializers(db_cart_detail)
            return ResponseMessage.CartResponse.success(db_data.data)
        else:
            filters = {
                'email': email,
                'is_delete': 0
            }
            db_cart_detail = Cart.objects.filter(**filters).all()
            db_data = CartDetailSerializers(db_cart_detail, many=True)
            return ResponseMessage.CartResponse.success(db_data.data)


class CartCountApiView(APIView):
    def post(self, request):
        # if not request.user.get("status"):
        #     return JsonResponse(request.user,safe=False)
        print('vvvvvv', request.user.get("data"), 'vvvvvv222',request)

        email = request.user.get("data").get("username")
        db_count = Cart.objects.filter(email=email,is_delete=0).aggregate(Sum('nums'))
        return ResponseMessage.CartResponse.success(db_count)

class CartAddApiView(APIView):
    def post(self, request):
        # if not request.user.get("status"):
        #     return JsonResponse(request.user,safe=False)
        email = request.user.get("data").get("username")
        print('emai===>l', email)
        request_data = json.loads(request.body)
        # request_data['id'] = request_data.get('id', '')
        request_data['nums'] = request_data.get('nums', '')
        request_data['sku_id'] = request_data.get('sku_id', '')
        request_data['email'] = email
        request_data['is_delete'] = 0
        print('request_data', request_data)

        # db_cart = Cart.objects.filter(sku_id=request_data['sku_id'], email=email, is_delete=0)
        db_cart = Cart.objects.filter(sku_id=request_data['sku_id'], email=email, is_delete=0).first()
        print('db_cart', db_cart)
        # if db_cart.exists():
        try:
            if db_cart:
            # if db_cart.exists():
            #     db_cart_data = db_cart.get(
            #         email=email,
            #         sku_id=request_data['sku_id'],
            #         is_delete=0,
            #     )
                print('db_cart_data', db_cart)
                # request_data['nums'] = request_data['nums'] + db_cart_data.nums
                # print('nnnnnnnnnmms', request_data['nums'], db_cart_data.nums)
                request_data['nums'] = request_data['nums'] + db_cart.nums
                cart_ser = CartSerializers(data=request_data)
                cart_ser.is_valid(raise_exception=True)
                Cart.objects.update(nums=request_data['nums'])
                return ResponseMessage.CartResponse.success('添加购物车成功')
            else:
                cart_ser = CartSerializers(data=request_data, many=False)
                cart_ser.is_valid(raise_exception=True)
                Cart.objects.create(
                    **cart_ser.data
                )
                return ResponseMessage.CartResponse.success('加入购物车成功')
        except ValidationError as e:
            print('ValidationError', e)
            # 捕获序列化器的验证错误，并返回详细的错误信息
            return ResponseMessage.CartResponse.failed(str(e))
        except Exception as e:
            print('Exception', e)
            # 捕获其他未知错误，并返回
            return ResponseMessage.CartResponse.failed(str(e))



class CartUpdateApiView(APIView):
    def post(self, request):
        email = request.user.get("data").get("username")
        sku_id = request.data['sku_id']
        nums = request.data['nums']
        Cart.objects.filter(email=email,sku_id=sku_id,is_delete=0).update(nums=nums)
        return ResponseMessage.CartResponse.success('update success')

class CartDeleteApiView(APIView):
    def post(self, request):
        email = request.user.get("data").get("username")
        print('request.data', request.data)
        sku_id = request.data['sku_id']
        Cart.objects.filter(email=email,sku_id=sku_id,is_delete=0).update(is_delete=1)
        return ResponseMessage.CartResponse.success('delete success')

