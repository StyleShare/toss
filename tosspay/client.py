import datetime
import json
from urllib.parse import urljoin

import pytz
import requests

from tosspay.exc import NotAutoExecutable
from tosspay.response import APIResponse, APIError
from tosspay.validator import validate_order_number


class TossPayClient:

    base_url = 'https://pay.toss.im/'
    api_version = 'v1'
    production_api_key = 'sk_test_apikey1234567890'
    development_api_key = 'sk_test_apikey1234567890'
    sandbox_key = 'sk_test_apikey1234567890'
    development = True

    def __init__(self, production_api_key=None, development_api_key=None,
                 development=True):
        self.production_api_key = production_api_key or self.sandbox_key
        self.development_api_key = development_api_key or self.sandbox_key
        self.development = development

    @property
    def api_key(self):
        if self.development:
            return self.development_api_key
        return self.production_api_key

    def build_url(self, uri):
        return urljoin(self.base_url,
                       urljoin('/api/{}/'.format(self.api_version), uri))

    def request(self, method, uri, params):
        params['apiKey'] = self.api_key
        result = getattr(requests, method)(self.build_url(uri), data=params)

        try:
            jsonized = result.json()
        except json.decoder.JSONDecodeError:
            return APIError('unsupported api response',
                            response=result.text)

        return APIResponse(**jsonized)

    def purchase(self, order_no, amount, product_desc, ret_url, cash_receipt,
                 amount_tax_free=0, auto_execute=False, amount_taxable=0,
                 amount_vat=0, amount_service_fee=0,
                 expired_time=datetime.timedelta(minutes=15),
                 result_callback='', escrow=False,
                 checkout_type='web', ars_auth_skippable='Y',
                 user_phone='', partner_id='',
                 metadata='', ret_cancel_url=''):

        if not result_callback and auto_execute:
            raise NotAutoExecutable
        if expired_time > datetime.timedelta(hours=1):
            raise ValueError("`expired_time` exceeds 1 hour")

        validate_order_number(order_no)

        basic_params = {
            "orderNo": order_no,
            "amount": amount,
            "productDesc": product_desc,
            "autoExecute": auto_execute or None,
            "retUrl": ret_url,
            "amountTaxable": amount_taxable or None,
            "amountTaxFree": amount_tax_free,
            "amountVat": amount_vat or None,
            "amountServiceFee": amount_service_fee or None,
            "expiredTime": (
                datetime.datetime.now(
                    tz=pytz.timezone('Asia/Seoul')) + expired_time
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "resultCallback": result_callback or None,
            "escrow": escrow or None,
            "cashReceipt": cash_receipt or None,
            "checkoutType": checkout_type or None,
            "arsAuthSkippable": ars_auth_skippable or None,
            "userPhone": user_phone or None,
            "partnerId": partner_id or None,
            "metadata": metadata or None,
            "retCancelUrl": ret_cancel_url or None
        }

        filtered = {}

        for k, v in basic_params.items():
            if v is not None:
                filtered[k] = v

        result = self.request('post', 'payments', filtered)
        return result
