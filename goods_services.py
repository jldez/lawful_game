



class Good(object):
    def __init__(self, price):
        self.price = price
        self.owner = None



class House(Good):
    def __init__(self, price):
        super().__init__(price)