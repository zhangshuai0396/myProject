from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response

from good.models import Goods
from goodcar.models import Goodcar
from permission.permission import GoodCarPermission
from static.const import BUYER
from user.models import User
from user.serializer import GoodCarListSerializers


# 商品添加(用户)
class GoodCarApiView(CreateAPIView):
    serializer_class = GoodCarListSerializers
    queryset = Goodcar.objects.all()
    permission_classes = [GoodCarPermission]
    def post(self, request, *args, **kwargs):
        good_id = request.data.get("good_id")
        u_id = request.data.get("u_id")
        good_car = Goodcar.objects.filter(u_id=u_id).filter(good_id=good_id).first()
        if good_car:
            good = Goods.objects.get(id=good_id)
            if good and good.num > good_car.buy_good_num:
                # 重复添加购物车商品时，+1
                good_car.buy_good_num += 1
                good_car.save()
                # 添加购物车时商品数量不减少，，生成订单时 才能减少
                # good.num -= 1
                # good.save()
                return JsonResponse(data={'id': good_car.id})
            else:
                return JsonResponse(data={})

        else:
            return self.create(request, *args, **kwargs)



# 单个购物车商品(只能更新购买数量)
class SingleGoodCarApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoodCarListSerializers
    queryset = Goodcar.objects.all()
    permission_classes = [GoodCarPermission]

    def patch(self, request, *args, **kwargs):
        # 修改购物车数量 的 判断
        buy_good_num = request.data.get("buy_good_num")
        good_car_id = request.parser_context.get("kwargs").get("pk")
        good_id = Goodcar.objects.get(id=good_car_id).good_id
        good_obj = Goods.objects.get(id=good_id)
        if buy_good_num and int(buy_good_num) > good_obj.num:
            return JsonResponse(data={})

        return self.partial_update(request, *args, **kwargs)




# 购物车商品分页
class PageListGoodCarApiView(ListAPIView):
    serializer_class = GoodCarListSerializers
    permission_classes = [GoodCarPermission]

    # 此处不定义过滤器，简单
    def get_queryset(self):
        goods = Goodcar.objects.all()
        user_name = self.request.query_params.get("query")
        page_size = self.request.query_params.get("page_size")
        user = self.request.user
        if user and user.role == BUYER:
            user_name = user.name
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
        return goods.order_by("id")
