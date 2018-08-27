import re


def validate_order_number(order_no: str) -> None:
    if len(order_no) > 50:
        raise ValueError("`order_no` length should be lesser than 50")
    if not re.match('^(\w|[_\-:.^@\'])+$', order_no):
        raise ValueError("`order_no` is not valid pattern")
