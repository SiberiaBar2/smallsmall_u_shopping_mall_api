import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.menu.models import MainMenu, SubMenu
from utils import ResponseMessage

# Create your views here.
class GoodsMainMenu(View):
    def get(self, request):
        print('get来了')
        main_menu = MainMenu.objects.all()
        # return HttpResponse('get请求')

        result_list = []
        result_json = {}

        for m in main_menu:
            # result_list.append(m)
            # 先将py对象转为字符串
            # 将字符串转化为正常对象供前端使用
            result_list.append(json.loads(m.__str__()))
        # result_json['status'] = 1000
        # result_json['data'] = result_list
        # return HttpResponse(json.dumps(result_json), content_type='application/json')
        return ResponseMessage.MenuResponse.success(result_list)

    def post(self, request):
        print('post来了')
        return HttpResponse('post请求')

class GoodsSubMenu(View):
    def get(self, request):
        print('get来了')
        param_id = request.GET['main_menu_id']

        result_list = []
        result_json = {}

        # 二级菜单内容
        sub_menu = SubMenu.objects.filter(
            main_menu_id=param_id
        )
        for m in sub_menu:
            result_list.append(json.loads(m.__str__()))

        # result_json['status'] = 1000
        # result_json['data'] = result_list
        return ResponseMessage.MenuResponse.success(result_list)
        # return HttpResponse(json.dumps(result_json), content_type='application/json')

