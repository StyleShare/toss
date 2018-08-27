

class BaseEntity:

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Payment(BaseEntity):
    def __init__(self, pay_token: str, pay_status: str, order_no: str,
                 amount: int,
                 amount_taxable: int, amount_tax_free: int, amount_vat: int,
                 amount_service_fee: int, time_created:str,
                 time_pay_complete: str,
                 time_pay_cancel: str, product_desc: str, has_owner: bool,
                 available_actions: list,
                 refunds: list, metadata: str, **kwargs):
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
        super(Payment, self).__init__(**kwargs)
