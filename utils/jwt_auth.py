import datetime

import jwt
from rest_framework.authentication import BaseAuthentication

from mu_shop_api.settings import SECRET_KEY

def create_token(payload, timeout=1):
    headers = {
        'alg': 'HS256',
        'typ': 'jwt'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=15)
    result = jwt.encode(headers=headers, payload=payload, key=SECRET_KEY, algorithm='HS256')
    return result

def get_payload(token):
    result = {"status": False, "data": None, "error": None}
    try:
       payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
       result['status'] = True
       result['data'] = payload
    except jwt.exceptions.DecodeError:
        print('token认证失败')
        result['error'] = 'token认证失败'
    except jwt.exceptions.ExpiredSignatureError:
        print('token已失效')
        result['error'] = 'token已失效'
    except jwt.exceptions.InvalidTokenError:
        print('无效、非法的token')
        result['error'] = '无效、非法的token'

    return result

# URL中传递
class JwtQueryParamAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.GET.get('token')
        result_payload = get_payload(token)

        # if not result_payload['status']:
            # raise
        print('result_payload', result_payload)
        # 必须这么写
        return (result_payload, token)

# 从头部获取token
class JwtHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 头信息会默认带上http
        # token = request.META.get('HTTP_TOKEN') # postman 中的方式
        token = request.META.get('HTTP_AUTHORIZATION')
        print('token', token)
        result_payload = get_payload(token)

        print('result_payload', result_payload)
        return (result_payload, token)