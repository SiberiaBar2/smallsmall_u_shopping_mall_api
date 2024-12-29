import datetime

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from apps.order.models import OrderGoods
from apps.user.models import User

class OrderGoodsSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     print('validated_data', validated_data)

    class Meta:
        model = OrderGoods
        fields = "__all__"