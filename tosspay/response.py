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
