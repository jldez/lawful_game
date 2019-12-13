import random
import numpy as np

MAJORITY_AGE = 18



class Population(object):

    def __init__(self, n_start:int=1):
        self.persons = [Person(self) for n in range(n_start)]
        for p in self:
            p.age = random.choice(range(80))
        self.set_mortality_rates()
        self.set_natality_rate()

    def update(self):
        [p.update() for p in self]

    def set_mortality_rates(self):
        ages = np.arange(100)
        func = np.exp(ages/10)
        self.mortality_rates = func/np.max(func)

    def set_natality_rate(self):
        self.natality_rate = 0.2

    @property
    def singles(self):
        singles = {'males':[], 'females':[]}
        for p in self:
            if p.family is None:
                if p.sex == 0:
                    singles['females'].append(p)
                elif p.sex == 1:
                    singles['males'].append(p)
        return singles

    @property
    def families(self):
        families = []
        for p in self:
            if p.family is not None:
                families.append(p.family)
        return set(families)

    def __len__(self):
        return len(self.persons)

    def __getitem__(self, index):
        return self.persons[index]



class Family(object):

    def __init__(self, father, mother):
        self.father = father
        self.mother = mother
        self.kids = []
        self.number_of_desired_kids = int(random.gauss(2,1))

    def update(self):
        if self.father is not None and self.mother is not None:
            if self.mother.age <= 55 and len(self.kids) < self.number_of_desired_kids:
                if random.random() < self.father.population.natality_rate:
                    baby = Person(self.father.population, family=self)
                    self.kids.append(baby)
                    self.father.population.persons.append(baby)

        for kid in self.kids:
            if kid.age >= MAJORITY_AGE:
                kid.family = None
                self.number_of_desired_kids -= 1
        self.kids = [kid for kid in self.kids if kid.age < MAJORITY_AGE]

        if len(self.kids) == 0:
            if self.father is None:
                self.mother.family = None
            if self.mother is None:
                self.father.family = None

                    



class Person(object):

    def __init__(self, population:Population, family:Family=None):
        self.population = population
        self.sex = random.choice([0,1])
        self.age = 0
        self.family = family

    def update(self):

        if random.random() < self.population.mortality_rates[self.age]:
            self.die()
            return None

        if self.family is not None and self.sex == 0:
            self.family.update()
        else: 
            self.match()

        self.age += 1

    def die(self):
        self.population.persons.remove(self)
        if self.family is not None:
            try:
                self.family.kids.remove(self)
            except:
                if self.sex == 0:
                    self.family.mother = None
                elif self.sex == 1:
                    self.family.father = None
        del self

    def match(self):
        singles = self.population.singles
        candidates = singles['males'] if self.sex == 0 else singles['females']
        candidates = [c for c in candidates if (c.age >= self.age/2 + 7) and (self.age >= c.age/2 + 7) and (c.age >= MAJORITY_AGE)]
        if len(candidates) > 0:
            match = random.choice(candidates)
            if random.random() > 0.3:
                father = self if self.sex == 1 else match
                mother = self if self.sex == 0 else match
                self.family = Family(father, mother)
                
        







