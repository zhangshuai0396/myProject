from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from category.models import Category
from good.models import Goods
from permission.permission import GoodsPermission
from static.const import ADMIN, SELLER
from user.models import User
from user.serializer import GoodListSerializers


# 商品添加
class GoodsApiView(CreateAPIView):
    serializer_class = GoodListSerializers
    queryset = Goods.objects.all()
    permission_classes = [GoodsPermission]

    # 重写create方法实现通过商家用户名添加商品,
    def create(self, request, *args, **kwargs):
        user_name = request.data.get("user_name")
        category_name = request.data.get("category_name")
        # print(category_name)
        req_data = request.data.copy()
        if category_name:
            category_obj = Category.objects.filter(name=category_name).first()
            if category_obj:
                req_data.update({"category_id": category_obj.id})
        if user_name:
            user_obj = User.objects.filter(name=user_name).first()
            if user_obj:
                req_data.update({"u_id": user_obj.id})
        serializer = self.get_serializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_context(self):
        # print(self.request.path)
        return {
            # 'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }


# 单个商品的查删木得改，因为要改文件
class SingleGoodApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoodListSerializers
    queryset = Goods.objects.all()
    permission_classes = [GoodsPermission]

    # # 实现图片url返回不加域名
    # def get_serializer_context(self):
    #     # print(self.request.path)
    #     return {
    #         # 'request': self.request,
    #         'format': self.format_kwarg,
    #         'view': self
    #     }

    #     重写get_serializer方法，实现修改商品时通过商品类名称修改商品分类，实现图片url返回不加域名
    def get_serializer(self, *args, **kwargs):
        # print(kwargs)
        req_data = kwargs.copy()
        data = kwargs.get("data")
        if data:
            data = data.copy()
        if data:
            category_name = data.get("category_name")
            if category_name:
                category_obj = Category.objects.filter(name=category_name).first()
                if category_obj:
                    data.update({"category_id": category_obj.id})
                    req_data.update({"data": data})
        serializer_class = self.get_serializer_class()
        # kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **req_data)


# 商品分页
class PageListGoodsApiView(ListAPIView):
    serializer_class = GoodListSerializers
    permission_classes = [GoodsPermission]

    # 此处不定义过滤器，简单
    def get_queryset(self):
        goods = Goods.objects.all()
        user_name = self.request.query_params.get("query")
        page_size = self.request.query_params.get("page_size")
        query_category = self.request.query_params.get("query_category")
        # 为了防止商家查看其它商家的商品
        user = self.request.user
        if user and user.role == SELLER:
            user_name = user.name
        # print(user_name)
        # 指定每页大小
        if page_size:
            self.paginator.page_size = page_size

        if user_name:
            # 通过用户名来搜索商品
            user = User.objects.filter(name=user_name)

            try:
                u_id = user.first().id
            except:
                return []
            goods = goods.filter(u_id=u_id)
        if query_category:
            category_obj = Category.objects.get(name=query_category)
            goods = goods.filter(category_id=category_obj.id)
        return goods.order_by("id")

    def get_serializer_context(self):
        # print(self.request.path)
        return {
            # 'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }