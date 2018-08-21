class APIResponse:

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ErrorResponse(APIResponse):

    def __init__(self, msg, **kwargs):
        self.msg = msg
        super(ErrorResponse, self).__init__(**kwargs)