import datetime

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from apps.goods.models import Goods
from apps.order.models import OrderGoods
from apps.user.models import User
from mu_shop_api.settings import IMAGE_URL


class OrderGoodsSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     print('validated_data', validated_data)
    class Meta:
        model = OrderGoods
        fields = "__all__"

class OrderPaymentSerializer(serializers.Serializer):
    trade_no = serializers.CharField()
    email = serializers.CharField()
    order_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    address_id = serializers.IntegerField()
    pay_status = serializers.CharField()
    pay_time = serializers.DateTimeField()
    ali_trade_no = serializers.CharField()
    is_delete = serializers.IntegerField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # update_time = serializers.DateTimeField()

    order_goods = serializers.SerializerMethodField()

    # obj 为当前一个订单实例
    def get_order_goods(self, obj):
        print('哦哦哦哦哦哦哦哦哦', obj, obj.trade_no)
        # 不加 many=True 差不出来
        ser = OrderGoodsSerializer(OrderGoods.objects.filter(trade_no=obj.trade_no).all(), many=True).data
        print('ser', ser)

        for i in ser:
            print(i.get("sku_id"))
            goods_data = Goods.objects.filter(sku_id=i.get("sku_id")).first()
            i['p_price'] = goods_data.p_price
            i["image"] = IMAGE_URL + goods_data.image
            i["name"] = goods_data.name
            i["shop_name"] = goods_data.shop_name
        return ser
