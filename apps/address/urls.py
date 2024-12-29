from django.urls import path, re_path
from .views import AddressGenericApiView, AddressListGenericApiView, AddressList, UpdateAdderssApiView, AddAddressNewApiView, DeleteAddressApiView

urlpatterns = [
    path('', AddressGenericApiView.as_view()),
    path('list', AddressListGenericApiView.as_view()),
    path('add', AddAddressNewApiView.as_view()),
    path('list/new', AddressList.as_view()),
    path('update', UpdateAdderssApiView.as_view()),
    path('delete', DeleteAddressApiView.as_view()),
    re_path('(?P<pk>.*)', AddressGenericApiView.as_view()),
]