import jobs

INTEREST_RATE = 0.03


class Government(object):

    def __init__(self, population):
        self.population = population
        self.money = 0
        self.tax_rate = 0.3
        self.social_welfare = 1e4
        self.retirement_age = 65

    def update(self):

        if self.money < 0:
            self.money += self.money*INTEREST_RATE
        
        for p in self.population.unemployed:
            p.money += self.social_welfare
            self.money -= self.social_welfare
