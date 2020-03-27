import traceback

from django.test import TestCase

# Create your tests here.
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

from alipay.aop.api.domain.AlipayTradeCreateModel import AlipayTradeCreateModel
from alipay.aop.api.request.AlipayTradeCreateRequest import AlipayTradeCreateRequest
from alipay.aop.api.response.AlipayTradeCreateResponse import AlipayTradeCreateResponse

from myProject.settings import PRIVATE_KEY, ALIPAY_PUBLIC_KEY
from static.const import ALIPAY_GATEWAY, APP_ID

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')

if __name__ == '__main__':
    # 实例化客户端
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = ALIPAY_GATEWAY
    alipay_client_config.app_id = APP_ID
    alipay_client_config.app_private_key = PRIVATE_KEY
    alipay_client_config.alipay_public_key = ALIPAY_PUBLIC_KEY
    client = DefaultAlipayClient(alipay_client_config, logger)

    # model = AlipayTradePagePayModel()
    # model.out_trade_no = order_id
    # model.total_amount = str(order.total_price)
    # model.subject = "天天生鲜订单支付"
    # model.timeout_express = str(settings.ALIPAY_TIMEOUT_MINUTE) + 'm'

    # 构造请求参数对象
    model = AlipayTradeCreateModel()
    model.out_trade_no = "xxx789dq"
    model.total_amount = "88.8"
    model.subject = "Iphone6 16"
    # model.buyer_id = "2088102180105521"
    model.timeout_express = str(6000)
    request = AlipayTradeCreateRequest(biz_model=model)
    response_content = None
    # 执行API调用
    try:
        # response_content = client.execute(request)
        response_content = client.page_execute(request, http_method='GET')
        print(response_content)
    except Exception as e:
        # print(traceback.format_exc())
        pass
    # if not response_content:
    #     print("failed execute")
    # else:
    #     # 解析响应结果
    #     response = AlipayTradeCreateResponse()
    #     response.parse_response_content(response_content)
    #     # 响应成功的业务处理
    #     if response.is_success():
    #         # 如果业务成功，可以通过response属性获取需要的值
    #         print("get response trade_no:" + response.trade_no)
    #     # 响应失败的业务处理
    #     else:
    #         # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
    #         print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)