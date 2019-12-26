


SOCIAL_WELFARE = 1e4
INTEREST_RATE = 0.03


class Government(object):

    def __init__(self, population):
        self.population = population
        self.money = 0

    def update(self):

        if self.money < 0:
            self.money -= self.money*INTEREST_RATE
        
        for p in self.population.unemployed:
            p.money += SOCIAL_WELFARE
            self.money -= SOCIAL_WELFARE
