"""
URL configuration for mu_shop_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.menu.views import GoodsMainMenu, GoodsSubMenu

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_menu/', GoodsMainMenu.as_view()),
    path('sub_menu/', GoodsSubMenu.as_view()),
    path('goods/', include('goods.urls')),# 关联goods模块下的url
    path('cart/', include('cart.urls')),
    path('user/', include('user.urls')),
    path('order/', include('order.urls')),
    path('address/', include('address.urls')),
    path('comment/', include('comment.urls')),
    path('pay/', include('pay.urls')),
]
