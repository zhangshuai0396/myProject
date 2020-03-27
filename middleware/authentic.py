from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from static.const import FAIL


class LoginAuthenticAOP(MiddlewareMixin):
    # pass
    @staticmethod
    def process_request(request):

        action = request.GET.get("action")
        order_pay_path = '/payapi/order/change/'

        path = request.path

        print(path)

        if path != order_pay_path:

            if action != "login" and action != "register":

                token = request.GET.get("token")
                u_id = cache.get(token)

                if not u_id:
                    data = {
                        "status": FAIL,
                        "msg": "请登陆",
                    }
                    return JsonResponse(data=data)
