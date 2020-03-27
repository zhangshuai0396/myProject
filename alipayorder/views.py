from alipay import AliPay
from django.http import JsonResponse
from rest_framework.views import APIView

from good.models import Goods
from myProject.settings import PRIVATE_KEY, ALIPAY_PUBLIC_KEY
from order.models import Order, Goodorder
from static.const import APP_ID, ALIPAY_GATEWAY, ACCOUNT_PAID


class OrderPayAPIView(APIView):

    @staticmethod
    def post(request):
        # 初始化
        alipay = AliPay(
            appid=APP_ID,
            app_notify_url="http://39.105.151.213:8080/#/buyer/order",  # 默认回调url
            app_private_key_string=PRIVATE_KEY,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=ALIPAY_PUBLIC_KEY,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

        order_id = request.POST.get("order_id")
        order = Order.objects.get(id=order_id)
        total_price = order.total_price

        good_order_list = Goodorder.objects.filter(order_id=order_id)
        subject = ""
        for goodorder in good_order_list:
            good = Goods.objects.get(id=goodorder.good_id)
            subject = subject + ' ' + good.name

        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        # subject = "测试订单1230"
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.id,
            total_amount=str(total_price),
            subject=subject,
            # return_url="http://192.168.10.101:8080/#/buyer/order", #返回商家 get
            return_url="http://39.105.151.213:8080/#/buyer/order",  # 返回商家 get
            notify_url="http://39.105.151.213/payapi/order/change/"  # post 传递信息
        )
        print(order.id)
        url = ALIPAY_GATEWAY + order_string
        return JsonResponse(data={"payurl": url})


class OrderChangeAPIView(APIView):

    @staticmethod
    def post(request):
        alipay = AliPay(
            appid=APP_ID,
            app_notify_url="http://39.105.151.213:8080/#/buyer/order",  # 默认回调url
            app_private_key_string=PRIVATE_KEY,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=ALIPAY_PUBLIC_KEY,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )
        data = request.data.copy()
        signature = data.pop("sign")
        order_id = data.get("out_trade_no")
        # print(data)
        # 由于接收到的是列表，所以此处改为signature[0] sign_type列表在源码中修改的
        success = alipay.verify(data, signature[0])
        if success:
            # 支付成功修改订单状态
            print("success")
            order_obj = Order.objects.get(id=order_id)
            order_obj.status = ACCOUNT_PAID
            order_obj.save()
            # 减少购物车商品数量
            # 通过订单号找到商品订单  再找到商品
            goodsorder = Goodorder.objects.filter(order_id=order_obj.id)
            for goodorder in goodsorder:
                good = Goods.objects.get(id=goodorder.good_id)
                if good.num >= goodorder.buy_good_num:
                    good.num -= goodorder.buy_good_num
                    good.save()

            return JsonResponse(data={"success": "success"})
        return JsonResponse(data={"failure": "failure"})
