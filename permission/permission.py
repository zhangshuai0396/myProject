from django.core.cache import cache
from rest_framework.permissions import BasePermission

from address.models import Address
from good.models import Goods
from goodcar.models import Goodcar
from order.models import Order
from static.const import SELLER, BUYER, ADMIN
from user.models import User


# 用户 管理员 权限--->地址
class AddressPermission(BasePermission):
    def has_permission(self, request, view):
        # 若使用认证类认证 可以用request.user来获取用户信息
        token = request.query_params.get("token")
        u_id = cache.get(token)
        # 中间件已认证过 此处无需捕获异常
        user = User.objects.get(id=u_id)
        # 防止买家用户权限越界
        # print(request.__dict__)
        # print(request.data)
        if user.role == BUYER:

            address_id = request.parser_context.get("kwargs").get("pk")
            # 防止增权限越界
            u_id = request.data.get("u_id")
            if u_id:
                if int(u_id) != user.id:
                    return False
            u_name = request.data.get("user_name")
            if u_name:
                if u_name != user.name:
                    return False
            # 防止删改查权限越界
            if address_id:
                address_obj = Address.objects.get(id=address_id)
                if user.id != address_obj.u_id:
                    return False
        if user.role == SELLER:
            return False
        return True


# 管理员买家权限
class AdminBuyerPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.query_params.get("token")
        u_id = cache.get(token)
        user = User.objects.get(id=u_id)
        request.user = user
        if user.role == SELLER:
            return True
        return True


# 商家 管理员权限 -->商品
# 用户 只能 查看
class GoodsPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.query_params.get("token")
        u_id = cache.get(token)
        user = User.objects.get(id=u_id)
        request.user = user
        if user.role == SELLER:
            good_id = request.parser_context.get("kwargs").get("pk")
            # 防止增权限越界
            u_id = request.data.get("u_id")
            if u_id:
                if int(u_id) != user.id:
                    return False
            u_name = request.data.get("user_name")
            if u_name:
                if u_name != user.name:
                    return False
            # 防止删改查权限越界
            if good_id:
                good_obj = Goods.objects.get(id=good_id)
                if user.id != good_obj.u_id:
                    return False
        if user.role == BUYER:
            req_method = request._request.method
            if req_method != "GET":
                return False
        return True


class CategoryPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.query_params.get("token")
        u_id = cache.get(token)
        # print(u_id)
        # print(token)
        user = User.objects.get(id=u_id)
        # print(user.role)
        if user.role == BUYER or user.role == SELLER:
            req_method = request._request.method
            if req_method != "GET":
                return False
        return True


class GoodCarPermission(BasePermission):

    def has_permission(self, request, view):
        token = request.query_params.get("token")
        u_id = cache.get(token)
        user = User.objects.get(id=u_id)
        request.user = user
        if user.role == SELLER:
            return False
        # 防止买家越权其它买家
        if user.role == BUYER:
            u_id = request.data.get("u_id")
            goodCar_id = request.parser_context.get("kwargs").get("pk")
            if u_id:
                if int(u_id) != user.id:
                    return False
            if goodCar_id:
                goodCar_obj = Goodcar.objects.get(id=goodCar_id)
                if user.id != goodCar_obj.u_id:
                    return False
        return True


class OrderPermission(BasePermission):

    def has_permission(self, request, view):
        token = request.query_params.get("token")
        u_id = cache.get(token)
        user = User.objects.get(id=u_id)
        request.user = user
        if user.role == SELLER:
            return False
        # 防止买家越权其它买家
        if user.role == BUYER:
            u_id = request.data.get("u_id")
            order_id = request.parser_context.get("kwargs").get("pk")
            if u_id:
                if int(u_id) != user.id:
                    return False
            if order_id:
                order_obj = Order.objects.get(id=order_id)
                if user.id != order_obj.u_id:
                    return False
        return True