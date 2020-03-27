from django.core.cache import cache
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response

from good.models import Goods
from goodcar.models import Goodcar
from order.models import Goodorder, Order, Orderaddress
from permission.permission import OrderPermission
from static.const import SELLER, BUYER
from user.models import User
from user.serializer import OrderSerializers


class CreateOrderAPIView(CreateAPIView):
    permission_classes = [OrderPermission]

    def create(self, request, *args, **kwargs):

        u_id = request.data.get("u_id")
        if u_id:
            goodscar = Goodcar.objects.filter(u_id=u_id).filter(is_select=1)
            order = Order()
            order.u_id = u_id
            order.save()
            total_price = 0
            for goodcar in goodscar:
                goodOrder = Goodorder()
                goodOrder.good_id = goodcar.good_id
                goodOrder.order_id = order.id
                goodOrder.buy_good_num = goodcar.buy_good_num
                goodOrder.save()
                good = Goods.objects.get(id=goodcar.good_id)
                total_price += goodcar.buy_good_num * good.price

            order.total_price = total_price
            order.save()
            # 购物车中的数据添加到ordergood中后，就删除购物车数据
            goodscar.delete()
            requestOrderAddress = request.data.get("order_address")
            orderAddress = Orderaddress()
            orderAddress.order_address = requestOrderAddress
            orderAddress.order_id = order.id
            # 保存一份地址数据，以免用户地址修改影响订单地址
            orderAddress.save()
            serializer = OrderSerializers(order)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


# 单个订单(只能更新订单状态，总价，地址，)
class SingleOrderApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializers
    queryset = Order.objects.all()
    permission_classes = [OrderPermission]

    def patch(self, request, *args, **kwargs):
        order_address = request.data.get("order_address")
        order_id = request.parser_context.get("kwargs").get("pk")
        if order_address:
            orderAddress = Orderaddress.objects.get(order_id=order_id)
            orderAddress.order_address = order_address
            orderAddress.save()
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        order_id = request.parser_context.get("kwargs").get("pk")
        # 删除订单时 删除订单地址，订单商品
        order_address = Orderaddress.objects.get(order_id=order_id)
        order_address.delete()
        goodorder = Goodorder.objects.filter(order_id=order_id)
        goodorder.delete()
        return self.destroy(request, *args, **kwargs)


# 订单分页
class PageListOrderApiView(ListAPIView):
    serializer_class = OrderSerializers
    permission_classes = [OrderPermission]

    # 此处不定义过滤器，简单
    def get_queryset(self):
        goods = Order.objects.all()
        user_name = self.request.query_params.get("query")
        page_size = self.request.query_params.get("page_size")
        # 买家用户只能看自己的订单
        user = self.request.user
        if user and user.role == BUYER:
            user_name = user.name
        # 指定每页大小
        if page_size:
            self.paginator.page_size = page_size

        if user_name:
            # 通过用户名来搜索订单
            user = User.objects.filter(name=user_name)
            try:
                u_id = user.first().id
            except:
                return []
            goods = goods.filter(u_id=u_id)
        return goods.order_by("id")
