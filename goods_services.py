

AVAILABLE_GOODS = {'houses':[]}


class Good(object):
    def __init__(self, price):
        self.price = price


class House(Good):
    def __init__(self):
        super().__init__(price=2e5)


