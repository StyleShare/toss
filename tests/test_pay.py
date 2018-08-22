from datetime import timedelta
from uuid import uuid4

import pytest

import tosspay
from tosspay.response import APIError


def test_purchase():
    c = tosspay.TossPayClient(development=True)
    order_id = str(uuid4())

    with pytest.raises(ValueError):
        c.purchase(order_id + '&', 40000, 'test', '', True)

    with pytest.raises(ValueError):
        c.purchase(order_id, 40000, 'test', '', True,
                   expired_time=timedelta(hours=1, minutes=1))

    with pytest.raises(tosspay.exc.NotAutoExecutable):
        c.purchase(order_id, 40000, 'test', '', True,
                   auto_execute=True)

    result = c.purchase(order_id, 40000, 'test', '', True)

    assert result.status == 200
    assert result.code == 0
    assert result.payToken is not None

    order_id = str(uuid4())
    result = c.purchase(order_id, 40000, 'test', '', True,
                        auto_execute=True, result_callback='test')

    assert result.status == 200
    assert result.code == 0
    assert result.payToken is not None

    result = c.purchase(order_id, 0, 'test', '', True,
                        auto_execute=True, result_callback='test')
    assert isinstance(result, APIError)
    assert result.status == 200
    assert result.code == -1
    assert result.msg == '요청한 값이 부족하거나 올바르지 않습니다. amount는 0보다 커야 합니다.'
    assert result.errorCode == 'COMMON_INVALID_PARAMETER'
