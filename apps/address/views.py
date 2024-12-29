import json

from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.views import APIView

from apps.address.models import UserAddress
from apps.address.serializers import AddressSerializer
from utils import ResponseMessage
from utils.jwt_auth import JwtQueryParamAuthentication, JwtHeaderAuthentication


# 添加地址接口
class AddressGenericApiView(
    GenericAPIView,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
):
    queryset = UserAddress.objects
    serializer_class = AddressSerializer
    # 若进行了全局配置 这里可不再引入
    # authentication_classes = [JwtHeaderAuthentication]

    def post(self, request):
        return self.create(request)

    def get(self, request, pk):
        print('pk', pk)
        if not request.user.get('status'):
            return JsonResponse(request.user, safe=False)
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

class AddressListGenericApiView(
    GenericAPIView,
    ListModelMixin
):
    queryset = UserAddress.objects
    serializer_class = AddressSerializer
    authentication_classes = [JwtQueryParamAuthentication]

    def get(self, request):
        # token 第一部分
        print('rrrr', request.user)
        # token 第二部分
        print('rrrr1', request.auth)

        if not request.user.get('status'):
            return JsonResponse(request.user, safe=False)
        return self.list(request)

class AddressList(APIView):
    # 重写地址列表
    def post(self, request):
        # if not request.user.get("status"):
        #     return JsonResponse(request.user, safe=False)
        username = request.user.get('data').get('username')
        address_list = UserAddress.objects.filter(email=username).all().order_by('-default', 'create_time')
        address_list_json = AddressSerializer(instance=address_list, many=True)
        return ResponseMessage.AdddressResponse.success(address_list_json.data)

class UpdateAdderssApiView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        username = request.user.get('data').get('username')
        # 必须从request.body获取数据 django的post只能处理formdata数据
        data = json.loads(request.body)
        id = data['id']
        email = username
        signer_name = data['signer_name']
        telphone = data['telphone']
        signer_address = data['signer_address']
        district = data['district']
        default = data['default']

        if default == 1:
            UserAddress.objects.exclude(id=id).update(default=0)
        db_address = UserAddress.objects.filter(id=id).update(
            id=id,
            email=email,
            signer_name=signer_name,
            telphone=telphone,
            signer_address=signer_address,
            district=district,
            default=default
        )
        return ResponseMessage.AdddressResponse.success(id)

class AddAddressNewApiView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        username = request.user.get('data').get('username')
        data = json.loads(request.body)
        email = username
        signer_name = data['signer_name']
        telphone = data['telphone']
        signer_address = data['signer_address']
        district = data['district']
        default = data['default']
        if default == 1:
            UserAddress.objects.update(default=0)
        new_address = UserAddress.objects.create(
            email=email,
            signer_name=signer_name,
            telphone=telphone,
            signer_address=signer_address,
            district=district,
            default=default
        )
        json_data = AddressSerializer(instance=new_address)
        return ResponseMessage.AdddressResponse.success(json_data.data)

class DeleteAddressApiView(APIView):
    def post(self, request):
        if not request.user.get("status"):
            return JsonResponse(request.user, safe=False)
        # 必须从request.body获取数据 django的post只能处理formdata数据
        data = json.loads(request.body)
        id = data['id']
        UserAddress.objects.get(id=id).delete()
        return ResponseMessage.AdddressResponse.success('ok')


