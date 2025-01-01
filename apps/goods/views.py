import decimal
import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from apps.goods.models import Goods
from apps.goods.serializers import GoodsSerializers
from utils import ResponseMessage


# Create your views here.
# 商品分类接口 goods/category
class GoodsGategoryApiView(APIView):
    def get(self, request, category_id, page):
        current_page = (page - 1) * 20
        end_data = page * 20
        category_data = Goods.objects.filter(
            type_id=category_id
        ).all()[current_page:end_data]  # limit的写法
        result_list = []
        for m in category_data:
            result_list.append(m.__str__())
        return ResponseMessage.GoodsResponse.success(result_list)


class GoodsDetailApiView(APIView):
    def get(self, request, sku_id):
        print('sku_id', sku_id)
        goods_data = Goods.objects.filter(
            sku_id=sku_id
        ).first()

        # 进行序列化 序列化的参数是instance ,反序列化的参数就是idata
        result = GoodsSerializers(instance=goods_data)
        return ResponseMessage.GoodsResponse.success(result.data)


class GoodsFindAPIView(APIView):
    def get(self, request):
        goods_find_data = Goods.objects.filter(
            find=1
        ).all()

        result = GoodsSerializers(instance=goods_find_data, many=True)

        return ResponseMessage.GoodsResponse.success(result.data)


class GoodsSearchApiView(APIView):
    def get(self, request, keyword, page, order_by):
        """
        SELECT r.comment_count,g.image, g.name,g.p_price,g.shop_name,g.sku_id from goods g
        LEFT JOIN
        (
        SELECT count(c.sku_id) as comment_count, c.sku_id from `comment` c GROUP BY c.sku_id
        ) r
        on g.sku_id=r.sku_id
        WHERE g.name LIKE '%手机%'
        ORDER BY r.comment_count DESC LIMIT 15, 15 -- 表示第二页
        """
        limit_page = (page - 1) * 15
        #   执行原生sql
        from django.db import connection
        from django.conf import settings

        order_dict = {
            1: 'r.comment_count',
            2: 'g.p_price',
        }
        sql = """
        SELECT r.comment_count,concat('{}',g.image) as image, g.name,g.p_price,g.shop_name,g.sku_id from goods g
        LEFT JOIN
        (
        SELECT count(c.sku_id) as comment_count, c.sku_id from `comment` c GROUP BY c.sku_id
        ) r
        on g.sku_id=r.sku_id
        WHERE g.name LIKE '%{}%'
        ORDER BY {} DESC LIMIT {}, 15
        """.format(settings.IMAGE_URL, keyword, order_dict[order_by], limit_page)
        cursor = connection.cursor()

        cursor.execute(sql)
        res = self.dict_fetchall(cursor)
        final_list = []
        for i in res:
            res_json = json.dumps(i, cls=DecimalEncoder, ensure_ascii=False)
            final_list.append(res_json)
        return ResponseMessage.GoodsResponse.success(final_list)

    def dict_fetchall(self, cursor):
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')


class GoodsKeywordCountApiView(APIView):
    def get(self, request, keyword):
        db_keyword_count = Goods.objects.filter(
            name__icontains=keyword
        ).count()
        return ResponseMessage.GoodsResponse.success(db_keyword_count)