import json
import random

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.user.models import User
from apps.user.password_encode import get_md5
from apps.user.serializers import UserSerializers, UserSerializersALl
from utils import ResponseMessage
from utils.jwt_auth import create_token
from utils.remove_empty_fields import remove_empty_fields


# Create your views here.
# 注册功能
class UserApiView(APIView):
    def post(self, request):
        # 密码设置md5加密
        request.data['password'] = get_md5(request.data.get('password'))
        # 反序列化 把json变成一个对象
        print('request.data', request.data)
        user_data_ser = UserSerializers(data=request.data)
        # 不加 raise_exception=True 是否抛出异常 即使验证异常了 接口也不会提示 所以必须加
        user_data_ser.is_valid(raise_exception=True)
        # 第一种写法 这样写密码是加密了的
        # user_data = User.objects.create(**user_data_ser.data)
        # 第二种写法 也是加密了的
        user_data = user_data_ser.save()
        # 序列化 把json返回前端
        user_ser = UserSerializers(instance=user_data)
        print('user_ser', user_ser.data, user_ser)
        # return JsonResponse(user_ser.data)
        return ResponseMessage.UserResponse.success(user_ser.data)

    def get(self, request):
        email = request.GET.get('email')
        try:
            user_data = User.objects.get(email=email)
            user_ser = UserSerializers(user_data)
            return ResponseMessage.UserResponse.success(user_ser.data)
        except Exception as e:
            print(e)
            ResponseMessage.UserResponse.failed('用户信息获取失败')

class LoginView(GenericAPIView):
    def post(self, request):
        return_data = {}
        request_data = request.data
        email = request_data.get('username')

        user_data = User.objects.get(email=email)
        if not user_data:
            return ResponseMessage.UserResponse.other('用户不存在')
        else:
            user_ser = UserSerializers(instance=user_data, many=False)
            user_passw = request_data.get('password')
            md5_user_passw = get_md5(user_passw)
            print('user_ser.data', user_ser.data)
            # 数据库的密码
            db_user_passw = user_ser.data.get('password')
            print('md5_user_passw', md5_user_passw, db_user_passw, db_user_passw == md5_user_passw)
            if md5_user_passw != db_user_passw:
                return ResponseMessage.UserResponse.other('用户名或密码错误2')
            else:
                token_info = {
                    'username': email
                }
                token_data = create_token(token_info)
                return_data['token'] = token_data
                return_data['username'] = user_ser.data.get('name')
                return ResponseMessage.UserResponse.success(return_data)

class UserInfoApiView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        username = request.user.get('data').get('username')
        db_user_info = User.objects.filter(email=username).first()
        json = UserSerializers(instance=db_user_info)
        # 一定要记得.data
        return ResponseMessage.UserResponse.success(json.data)

class UserUpdateApiView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        username = request.user.get('data').get('username')
        data = json.loads(request.body)
        email = username

        id = data.get('id', '')
        print('id====>', id, 'data', data)
        if not id:
            return ResponseMessage.UserResponse.failed('id是必传参数')
            raise ValidationError({"detail": "id is required"})
        try:
            user_data = User.objects.get(id=id)
        except User.DoesNotExist:
            return ResponseMessage.UserResponse.failed('用户不存在')
        user_ser = UserSerializersALl(instance=user_data, many=False)

        print('ooooo', data.get('old_password', ''))
        print('ppppp', data.get('password', ''))
        old_password = get_md5(data.get('old_password', ''))
        print('old',old_password)
        # 数据库之前的密码
        db_user_passw = user_ser.data.get('password')
        birthday = data.get('birthday', '')
        # 要修改后的密码
        password = get_md5(data.get('password', ''))
        name = data.get('name')
        mobile = data.get('mobile')
        gender = data.get('gender')

        print('old_password', old_password, 'password', password)
        if old_password and password:
            if old_password != db_user_passw:
                return ResponseMessage.UserResponse.failed('旧密码不正确！')
        # 这里字段必须是字符串 否则 update 会报错
        filter_data = remove_empty_fields({
            'email': email,
            'birthday': birthday,
            'name': name,
            'mobile': mobile,
            'gender': gender,
            'password': password
        })
        User.objects.filter(id=id).update(**filter_data)
        return ResponseMessage.UserResponse.success('更新用户成功')

class RegisterUserApiView(APIView):
    def post(self, request):
        # 注册接口 不需要token验证
        authentication_classes = []  # 禁用认证
        permission_classes = [AllowAny]

        request_data = json.loads(request.body)
        request_data['email'] = request_data.get('username')
        request_data['password'] = request_data.get('password')
        request_data['password'] = get_md5(request_data['password'])
        request_data['name'] = self.get_random_name()

        user_ser = UserSerializersALl(data=request_data)
        user_ser.is_valid(raise_exception=True)
        User.objects.create(**user_ser.validated_data)
        return ResponseMessage.UserResponse.success('注册新用户成功')
    def get_random_name(self):
        names_dict = {
            "name1": "善良的雪人",
            "name2": "坚强的骑士",
            "name3": "勇敢的雪人",
            "name4": "善良的雪花",
            "name5": "聪明的骑士"
        }
        # 随机选择字典的值
        random_name = random.choice(list(names_dict.values()))
        return random_name
