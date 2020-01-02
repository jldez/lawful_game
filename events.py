import random
import numpy as np


class Event(object):

    def __init__(self, duration=1):
        self.duration = duration

    likelihood = 1

    def __call__(self, population):
        self.duration -= 1
        return population

    def terminate(self, population):
        return population



class BabyBoom(Event):
    def __init__(self):
        super().__init__(duration=5)
        self.description = 'Baby boom!'

    def __call__(self, population):
        if self.duration == 5:
            for p in population:
                p.number_of_desired_kids += random.choice([0,1,2,3])
            population.natality_rate += 0.3
        super().__call__(population)
        return population

    def terminate(self, population):
        population.natality_rate -= 0.3
        super().terminate(population)
        return population


class ColdEpidemia(Event):
    def __init__(self):
        super().__init__(duration=1)
        self.description = 'A cold is spreading.'

    def __call__(self, population):
        for p in population:
            p.health -= random.choice([0,10])
        super().__call__(population)
        return population


class Plague(Event):
    # To do : real epidemia spreading, percolation, etc.
    def __init__(self):
        super().__init__(duration=5)
        self.description = 'The plague is spreading.'

    likelihood = 0.5

    def __call__(self, population):
        for p in population:
            p.health -= np.random.choice([0,90],p=[0.9,0.1])
        super().__call__(population)
        return population


class FoodContamination(Event):
    def __init__(self):
        super().__init__(duration=random.choice([1,2,3,4,5,6,7,8,9,10]))
        self.fraction = random.choice([0.3,0.5,0.7])
        adjective = '' 
        if self.fraction == 0.5:
            adjective += 'badly '
        if self.fraction == 0.7:
            adjective += 'very badly '
        self.description = f'The food is {adjective}contaminated for {self.duration} years.'
        self.active = False

    def __call__(self, population):
        if not self.active:
            population.food_decay += self.fraction
            self.active = True
        for p in population:
            p.health -= np.random.choice([0,10],p=[1-self.fraction, self.fraction])
        super().__call__(population)
        return population

    def terminate(self, population):
        population.food_decay -= self.fraction
        return population


EVENTS_POOL = [BabyBoom, ColdEpidemia, Plague, FoodContamination]
EVENTS_PROB = np.array([event.likelihood for event in EVENTS_POOL])
EVENTS_PROB = EVENTS_PROB/np.sum(EVENTS_PROB)
