# 配置数据库
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',

        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'muxi',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST': 'queek.work',
        # 'HOST': '43.163.113.67',
        'PORT': '3306'
    }
}

# 需要改成服务器地址
# IMAGE_URL='http://43.163.113.67/static/product_images/'
IMAGE_URL='http://queek.work/static/product_images/'

APPID = '2021000143606540'

# 异步接收url post请求
APP_NOTIFY_URL = 'http://queek.work/pay/alipay/return'
# 同步接收url 用户在页面支付成功之后就跳转的页面 get请求
RETURN_URL = 'http://queek.work/pay/alipay/return'
# 是否是开发环境
ALIPAY_DEBUG=True