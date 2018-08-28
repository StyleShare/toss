from toss.exc import TossPayException


class APIResponse:

    def __new__(cls, *args, **kwargs):
        if kwargs["code"] == -1:
            raise super(cls, APIError).__new__(APIError)
        return super(APIResponse, cls).__new__(cls)

    def __init__(self, **kwargs):
        self.data = kwargs


class APIError(APIResponse, TossPayException):

    def __init__(self, msg: str, **kwargs):
        self.msg = msg
        super(APIError, self).__init__(**kwargs)


class PurchasedResult(APIResponse):
    def __init__(self, pay_token: str, purchase_url: str, *args, **kwargs):
        self.pay_token = pay_token
        self.purchase_url = purchase_url
        super(PurchasedResult, self).__init__(**kwargs)


class ApprovedResult(APIResponse):

    def __init__(self, code: str, approved_at: str, **kwargs):
        self.code = code
        self.approved_at = approved_at
        super(ApprovedResult, self).__init__(**kwargs)


class CancelledResult(APIResponse):
    pass


class RefundedResult(APIResponse):

    def __init__(self, code: str, refund_no: str, approved_at: str, **kwargs):
        self.code = code
        self.refund_no = refund_no
        self.approved_at = approved_at
        super(RefundedResult, self).__init__(**kwargs)
