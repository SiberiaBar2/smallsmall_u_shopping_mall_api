from apps.cart.models import Cart
from apps.goods.serializers import GoodsSerializers
from mu_shop_api.settings import IMAGE_URL
from rest_framework import serializers
from apps.goods.models import Goods

class CartSerializers(serializers.ModelSerializer):
    # 设置必传字段
    sku_id = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    class Meta:
        model = Cart
        fields = "__all__"

# 查多个表不用指定meta
class CartDetailSerializers(serializers.Serializer):
    # 设置必传字段
    sku_id = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    nums = serializers.IntegerField()
    is_delete = serializers.IntegerField()
    goods = serializers.SerializerMethodField()

    def get_goods(self, obj):
        ser = GoodsSerializers(Goods.objects.filter(sku_id=obj.sku_id).first()).data
        return ser