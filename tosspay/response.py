class APIResponse:

    def __new__(cls, *args, **kwargs):
        if kwargs["code"] == -1:
            return super(cls, APIError).__new__(APIError)
        return super(APIResponse, cls).__new__(cls)

    def __init__(self, **kwargs):
        self.data = kwargs


class APIError(APIResponse):

    def __init__(self, msg, **kwargs):
        self.msg = msg
        super(APIError, self).__init__(**kwargs)


class PurchaseResult(APIResponse):
    def __init__(self, pay_token, purchase_url, client=None, *args, **kwargs):
        self.pay_token = pay_token
        self.purchase_url = purchase_url
        self._client = client
        super(PurchaseResult, self).__init__(**kwargs)

    @property
    def payment(self):
        return self._client.get_payment(self.pay_token)


class ApprovedResult(APIResponse):

    def __init__(self, code, approved_at, **kwargs):
        self.code = code
        self.approved_at = approved_at
        super(ApprovedResult, self).__init__(**kwargs)


class CancelledResult(APIResponse):

    pass


class RefundedResult(APIResponse):

    def __init__(self, code, refund_no, approved_at, **kwargs):
        self.code = code
        self.refund_no = refund_no
        self.approved_at = approved_at
        super(RefundedResult, self).__init__(**kwargs)
