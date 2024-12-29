from rest_framework import serializers
from apps.address.models import UserAddress

class AddressSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = UserAddress
        fields = "__all__"