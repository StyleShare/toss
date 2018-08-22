class APIResponse:

    def __new__(cls, *args, **kwargs):
        if kwargs["code"] == -1:
            return super(cls, APIError).__new__(APIError)
        return super(APIResponse, cls).__new__(cls)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class APIError(APIResponse):

    def __init__(self, msg, **kwargs):
        self.msg = msg
        super(APIError, self).__init__(**kwargs)
