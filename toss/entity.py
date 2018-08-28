import inflection


class BaseEntity:

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Payment(BaseEntity):
    def __init__(self, pay_token: str, pay_status: str, order_no: str,
                 amount: int,
                 amount_taxable: int, amount_tax_free: int, amount_vat: int,
                 amount_service_fee: int, time_created: str,
                 time_pay_complete: str,
                 time_pay_cancel: str, product_desc: str, has_owner: bool,
                 available_actions: list,
                 refunds: list, metadata: str,
                 client=None,
                 **kwargs):
        self.pay_token = pay_token
        self.pay_status = pay_status
        self.order_no = order_no
        self.amount = amount
        self.amount_taxable = amount_taxable
        self.amount_tax_free = amount_tax_free
        self.amount_vat = amount_vat
        self.amount_service_fee = amount_service_fee
        self.time_created = time_created
        self.time_pay_complete = time_pay_complete
        self.time_pay_cancel = time_pay_cancel
        self.product_desc = product_desc
        self.has_owner = has_owner
        self.available_actions = available_actions
        self.refunds = refunds
        self.metadata = metadata
        self._client = client
        super(Payment, self).__init__(**kwargs)

    def approve(self, amount: int=None, order_no: str=None):
        result = self._client.approve(self.pay_token, amount, order_no)
        self._refresh()
        return result

    def cancel(self, reason: str):
        result = self._client.cancel(self.pay_token, reason)
        self._refresh()
        return result

    def refund(self,
               amount: int,
               amount_tax_free: int,
               refund_no: str = None,
               reason: str = None,
               amount_taxable: int = None,
               amount_vat: int = None,
               amount_service_fee: int = None):
        result = self._client.refund(self.pay_token, amount, amount_tax_free,
                                     refund_no, reason, amount_taxable,
                                     amount_vat, amount_service_fee)
        self._refresh()
        return result

    def _refresh(self):
        result = self._client.request('post', 'status',
                                      {'payToken': self.pay_token})

        params = dict((inflection.underscore(k), v)
                      for k, v in result.data.items())
        print('refresh')
        self.__init__(client=self._client, **params)
