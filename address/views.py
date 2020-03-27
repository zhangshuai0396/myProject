from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from address.models import Address
from permission.permission import AddressPermission, AdminBuyerPermission
from static.const import BUYER
from user.models import User
from user.serializer import AddressSerializers, AddressListSerializers


# 地址添加
class AddressApiView(CreateAPIView):
    serializer_class = AddressSerializers
    queryset = Address.objects.all()
    permission_classes = [AddressPermission]

    # 重写create方法实现通过用户名添加地址
    def create(self, request, *args, **kwargs):
        user_name = request.data.get("user_name")
        req_data = request.data.copy()
        if user_name:
            user_obj = User.objects.filter(name=user_name).first()
            if user_obj:
                req_data.update({"u_id": user_obj.id})
        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 单个地址的查删改
class SingleAddressApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = AddressListSerializers
    queryset = Address.objects.all()
    permission_classes = [AddressPermission]


# 地址分页
class PageListAddressApiView(ListAPIView):
    serializer_class = AddressListSerializers
    permission_classes = [AdminBuyerPermission]

    # 此处不定义过滤器，简单
    def get_queryset(self):
        address = Address.objects.all()
        user_name = self.request.query_params.get("query")
        page_size = self.request.query_params.get("page_size")
        # print(user_name)
        # 指定每页大小
        if page_size:
            self.paginator.page_size = page_size
        # 买家只能看自己的地址
        if self.request.user.role == BUYER:
            user_name = self.request.user.name

        if user_name:
            # 通过用户名来搜索地址
            user = User.objects.filter(name=user_name)
            try:
                u_id = user.first().id
            except:
                return []
            address = address.filter(u_id=u_id)
        return address.order_by("id")
