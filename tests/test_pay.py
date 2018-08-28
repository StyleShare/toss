from datetime import timedelta
from uuid import uuid4

import pytest
import requests_mock

import toss.exc

from toss.client import TossPayClient
from toss.entity import Payment
from toss.response import (APIError, ApprovedResult, CancelledResult,
                           PurchasedResult, RefundedResult)


def test_purchase():
    c = TossPayClient(development=True)
    order_id = str(uuid4())

    with pytest.raises(ValueError):
        c.purchase(order_id + '&', 40000, 'test', '', True)

    with pytest.raises(ValueError):
        c.purchase(order_id, 40000, 'test', '', True,
                   expired_time=timedelta(hours=1, minutes=1))

    with pytest.raises(toss.exc.NotAutoExecutable):
        c.purchase(order_id, 40000, 'test', '', True,
                   auto_execute=True)

    result = c.purchase(order_id, 40000, 'test', '', True)

    assert result.pay_token is not None
    assert result.purchase_url is not None

    order_id = str(uuid4())
    result = c.purchase(order_id, 40000, 'test', '', True,
                        auto_execute=True, result_callback='test')

    assert result.pay_token is not None
    assert result.purchase_url is not None
    assert isinstance(result, PurchasedResult)

    with pytest.raises(APIError) as result:
        c.purchase(order_id, 0, 'test', '', True,
                   auto_execute=True, result_callback='test')
        assert result.data["status"] == 200
        assert result.data["code"] == -1
        assert result.msg == '요청한 값이 부족하거나 올바르지 않습니다. amount는 0보다 커야 합니다.'
        assert result.data["errorCode"] == 'COMMON_INVALID_PARAMETER'


def test_get_payment():
    pay_token = "N4GOTJB5eR3Tnx8kJeVp90"

    c = TossPayClient(development=True)
    result = c.get_payment(pay_token)

    assert isinstance(result, Payment)


def test_purchase_result():
    c = TossPayClient(development=True)
    order_id = str(uuid4())

    purchase_result = c.purchase(order_id, 40000, 'test', '', True)

    payment = c.get_payment(purchase_result.pay_token)

    assert isinstance(payment, Payment)
    assert payment.amount == 40000
    assert payment.product_desc == 'test'
    assert payment.pay_status == 'PAY_STANDBY'


def test_confirm_purchase():
    c = TossPayClient(development=True)
    order_id = str(uuid4())
    purchase_result = c.purchase(order_id, 40000, 'test', '', True)
    payment = c.get_payment(purchase_result.pay_token)

    with pytest.raises(APIError) as approved_result:
        c.approve(payment.pay_token)
        assert approved_result.msg == '사용자 정보가 존재하지 않습니다.'

    result = c.purchase(order_id, 40000, 'test', '', True)
    payment = c.get_payment(result.pay_token)
    token = payment.pay_token

    with requests_mock.Mocker() as m:
        # NOTE: toss user-side auth 가 자동화될 수가 없어 mocking 으로 우회
        m.post('https://pay.toss.im/api/v1/execute',
               text='{"code":0,"approvalTime":"2016-11-16 13:59:59"}')
        approved_result = c.approve(token)

    assert isinstance(approved_result, ApprovedResult)


def test_cancel_purchase():
    c = TossPayClient(development=True)
    order_id = str(uuid4())
    purchase_result = c.purchase(order_id, 40000, 'test', '', True)
    payment = c.get_payment(purchase_result.pay_token)

    cancelled_result = c.cancel(payment.pay_token, 'test cancel')

    assert isinstance(cancelled_result, CancelledResult)

    order_id = str(uuid4())
    pr = c.purchase(order_id, 40000, 'test', '', True, auto_execute=True,
                    result_callback='test')
    payment = c.get_payment(pr.pay_token)
    token = payment.pay_token
    cancelled_result = c.cancel(token, 'test cancel')

    assert isinstance(cancelled_result, CancelledResult)

    order_id = str(uuid4())
    result = c.purchase(order_id, 40000, 'test', '', True)
    payment = c.get_payment(result.pay_token)
    token = payment.pay_token

    with requests_mock.Mocker() as m:
        # NOTE: toss user-side auth 가 자동화될 수가 없어 mocking 으로 우회
        m.post('https://pay.toss.im/api/v1/execute',
               text='{"code":0,"approvalTime":"2016-11-16 13:59:59"}')
        c.approve(token)
        # NOTE: 승인이 되어 결제가 완료된 시점에서는 취소가 불가능함
        m.post('https://pay.toss.im/api/v1/cancel',
               text='{"code": -1, "errorCode": "CANCEL_IMPOSSIBLE_STATUS", '
                    '"status": 200, "msg": "취소가 불가능한 상태입니다."}')
        with pytest.raises(APIError) as cancelled_result:
            c.cancel(token, 'test')
            assert isinstance(cancelled_result, APIError)
            assert cancelled_result.data[
                       'errorCode'] == 'CANCEL_IMPOSSIBLE_STATUS'  # noqa


def test_cancel_refund():
    c = TossPayClient(development=True)
    order_id = str(uuid4())
    purchase_result = c.purchase(order_id, 40000, 'test', '', True)
    payment = c.get_payment(purchase_result.pay_token)
    with pytest.raises(APIError) as refund_result:
        c.refund(payment.pay_token, 40000, 0)
        assert isinstance(refund_result, APIError)

    # NOTE: toss user-side auth 가 자동화될 수가 없어 mocking 으로 우회
    # NOTE: 이후는 승인되었다고 가정

    token = payment.pay_token

    with requests_mock.Mocker() as m:
        m.post('https://pay.toss.im/api/v1/refunds',
               text='{"code": 0, "refundNo": "b764f9ec-a113-401d-9db8-'
                    '532a36c0986b", "approvalTime": "2018-08-27 13:25:11"}')
        refunded_result = c.refund(token, 40000, 0)
        assert isinstance(refunded_result, RefundedResult)


def test_payment_entity():
    c = TossPayClient(development=True)
    order_id = str(uuid4())
    purchase_result = c.purchase(order_id, 40000, 'test', '', True)

    payment = c.get_payment(purchase_result.pay_token)

    assert isinstance(payment, Payment)

    assert payment.available_actions == ['CANCEL']
    cancelled_result = payment.cancel('test')
    assert isinstance(cancelled_result, CancelledResult)
    assert payment.available_actions == []
