"""
Django settings for mu_shop_api project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# 将apps下的模块 加入到项目跟的搜索路径， 可以直接从源码包导入
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)vcwmvh-=npl9__xy7po6i=9)o4ibsk*i6yaqug+bu9-#lrs9f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 所有的ip都能访问
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cart', # 导入
    'comment',
    'order',
    'goods',
    'user',
    'rest_framework',
    'corsheaders',
    'menu',
    'address',
]

# 允许所有域名跨域
CORS_ORIGIN_ALLOW_ALL = True
# 允许携带cookie
CORS_ALLOW_CREDENTIALS = True

# 类似于拦截器
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', # 注释c's'r'f
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mu_shop_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mu_shop_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# 配置数据库
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',

        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'muxi',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST': '0.0.0.0',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# 这个是图片的访问路径
# 我们的图片访问路径是 http://localhost:8080/static/prodoct/1.jpg
STATIC_URL = 'static/'
# 需要配置我们的文件夹所在路径
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 静态文件服务器位置
IMAGE_URL='http://localhost:8000/static/product_images/'

# 全局的token验证配置 这里引入便不用再局部引入了
REST_FRAMEWORK = {
    # "DEFAULT_AUTHENTICATION_CLASSES": ['utils.jwt_auth.JwtQueryParamAuthentication'],
    "DEFAULT_AUTHENTICATION_CLASSES": ['utils.jwt_auth.JwtHeaderAuthentication'],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # 确保全局允许所有访问
    ],
}

# 支付宝沙箱环境配置
APPID = '2021000143606540'

ALI_PUB_KEY_PATH = os.path.join(BASE_DIR, 'apps/pay/keys/alipay_key.txt')
PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'apps/pay/keys/private_key.txt')

# 异步接收url post请求
APP_NOTIFY_URL = 'http://127.0.0.1:8000/pay/alipay/return'
# 同步接收url 用户在页面支付成功之后就跳转的页面 get请求
RETURN_URL = 'http://127.0.0.1:8000/pay/alipay/return'
# 是否是开发环境
ALIPAY_DEBUG=True