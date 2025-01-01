import datetime

from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from apps.user.models import User

class   UserSerializers(serializers.ModelSerializer):
    # email 作为用户名进行登录 这里我们需要做个唯一验证
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all(), message='用户已经存在了')], # 验证规则
    )

    # 只往数据库里写 不给前端返回
    # password = serializers.CharField(write_only=True)
    birthday = serializers.DateTimeField('%Y-%m-%d %H:%M:%S')
    create_time = serializers.DateTimeField('%Y-%m-%d %H:%M:%S', required=False)
    # 密码已经加密过 因此这里不再处理
    # create会被自动调用 这里可以做一些验证 和存储之前对数据做一些加工
    def create(self, validated_data):
        validated_data['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = User.objects.create(**validated_data)
        return result
    class Meta:
        model = User
        fields = "__all__"

class UserSerializersALl(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"