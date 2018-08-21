from datetime import timedelta
from uuid import uuid4

import pytest

import tosspay


def test_purcahse():
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

    order_id = str(uuid4())
