from mu_shop_api.settings import IMAGE_URL
from rest_framework import serializers
from apps.goods.models import Goods

# todo 有待考究 不是特别清楚
class GoodsSerializers(serializers.ModelSerializer):
    # 这里写的字段就是序列化是你想要进行处理的字段
    # name = serializers.CharField()
    image = serializers.SerializerMethodField()
    # 处理时间序列化 被处理的字段会写在前面
    create_time = serializers.DateTimeField('%Y-%m-%d %H:%M:%S')
    def get_image(self, obj):
        new_image_path = IMAGE_URL + obj.image
        return new_image_path

    # 没有这个会报错
    class Meta:
        model = Goods
        fields = "__all__"