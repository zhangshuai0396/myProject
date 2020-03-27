import uuid

from django.contrib import auth
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.views import APIView

from address.models import Address
from goodcar.models import Goodcar
from order.models import Order, Orderaddress, Goodorder
from static.const import ADMIN, SUCCESS, FAIL, BUYER
from user.serializer import LoginSerializers
from user.models import User


class LoginView(APIView):

    @staticmethod
    def get_u_object(request):
        token = request.GET.get("token")
        u_id = cache.get(token)
        user = User.objects.get(id=u_id)
        return user, token

    @staticmethod
    def post(request):
        action = request.GET.get("action")
        if action == "login":
            u_name = request.POST.get("name")
            u_password = request.POST.get("password")
            users = User.objects.filter(name=u_name).filter(password=u_password)
            user = users.first()
            if user:
                token = uuid.uuid4().hex
                cache.set(token, user.id, timeout=60 * 60 * 10)
                data = {
                    "status": SUCCESS,
                    "token": token,
                    "msg": "登录成功",
                    "role": user.role,
                    "u_id": user.id,
                }
            else:
                data = {
                    "status": FAIL,
                    "msg": "登录失败",
                }
            return JsonResponse(data=data)
        elif action == "update":
            u_name = request.POST.get("name")
            u_password = request.POST.get("password")
            u_role = request.POST.get("role")
            user = LoginView.get_u_object(request)[0]
            if user.role == ADMIN:
                u_id = request.POST.get("uid")
                print(u_id)
                user = User.objects.get(id=u_id)
            if u_name:
                user.name = u_name
            if u_password:
                user.password = u_password
            if u_role and u_role != str(ADMIN):
                user.role = u_role
            try:
                user.save()
                data = {
                    "status": SUCCESS,
                    "msg": "修改成功",
                }
            except:
                data = {
                    "status": FAIL,
                    "msg": "修改失败",
                }
            return JsonResponse(data=data)

        elif action == "register":
            u_name = request.POST.get("name")
            u_password = request.POST.get("password")
            u_role = request.POST.get("role")
            try:
                if int(u_role) == ADMIN:
                    return JsonResponse(data={"msg": "不能注册管理员"})
                user = User()
                user.name = u_name
                user.password = u_password
                user.role = int(u_role)
                user.save()
                data = {
                    "status": SUCCESS,
                    "msg": "注册成功",
                }
            except:
                data = {
                    "status": FAIL,
                    "msg": "注册失败",
                }
            return JsonResponse(data=data)
        else:
            data = {
                "status": FAIL,
                "msg": "失败",
            }
            return JsonResponse(data=data)

    def get(self, request):
        action = request.GET.get("action")
        # 只有超级管理员可删除
        if action == "delete":
            user = LoginView.get_u_object(request)[0]
            if user.role != ADMIN:
                return JsonResponse(data={"msg": "不是管理员"})
            u_id = request.GET.get("uid")
            try:
                user = User.objects.get(id=u_id)
                if user.id == BUYER:
                    # 删除用户的同时还要删除 地址，
                    Address.objects.filter(u_id=u_id).delete()
                    # 删除购物车
                    Goodcar.objects.filter(u_id=u_id).delete()
                    # 删除订单系列
                    order = Order.objects.filter(u_id=u_id)
                    order_address = Orderaddress.objects.get(order_id=order.id)
                    order_address.delete()
                    goodorder = Goodorder.objects.filter(order_id=order.id)
                    goodorder.delete()
                user.delete()
                data = {
                    "status": SUCCESS,
                    "msg": "删除成功"
                }
            except:
                data = {
                    "status": SUCCESS,
                    "msg": "删除失败"
                }
            return JsonResponse(data=data)

        elif action == "layout":
            token = request.GET.get("token")
            cache.delete(token)
            data = {
                "status": SUCCESS,
                "msg": "退出成功",
            }
            return JsonResponse(data=data)
        else:
            data = {
                "status": FAIL,
                "msg": "失败",
            }
            return JsonResponse(data=data)


class UserListView(APIView):
    # 带上静态修饰就只有一个参数，而不带需要两个含self
    @staticmethod
    def get(request):
        user = LoginView.get_u_object(request)[0]
        if user.role != ADMIN:
            data = {
                "status": FAIL,
                "msg": "没有权限"
            }
            return JsonResponse(data=data)
        page_query = request.GET.get("query")
        users = User.objects.all().exclude(role=ADMIN).order_by("id")
        if page_query:
            users = users.filter(name__contains=page_query)
        page_num = request.GET.get("page_num")
        # if page_num:
        current_page = request.GET.get("page")
        page_obj = Paginator(users, page_num)
        try:
            users_obj = page_obj.page(current_page)
        except:
            users_obj = page_obj.page(1)
        userSerializer = LoginSerializers(users_obj, many=True)
        pages_num = page_obj.num_pages
        print(pages_num)
        data = {
            "status": SUCCESS,
            "user": userSerializer.data,
            "msg": "显示成功",
            "pages_num": pages_num,
        }
        return JsonResponse(data=data)


class UserDetailView(APIView):
    @staticmethod
    def get(request):
        user = LoginView.get_u_object(request)[0]
        u_id = user.id
        if user.role == ADMIN:
            u_id = request.GET.get("uid")
        user = User.objects.filter(id=u_id).exclude(role=ADMIN)
        if user.first():
            userSerializer = LoginSerializers(user.first())
            data = {
                "status": SUCCESS,
                "user": userSerializer.data,
                "msg": "查询成功"
            }
        else:
            data = {
                "status": FAIL,
                "msg": "查询失败"
            }
        return JsonResponse(data=data)