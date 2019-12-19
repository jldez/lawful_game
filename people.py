import random
import numpy as np
import jobs
import government

MAJORITY_AGE = 18
TAX_RATE = 0.3


class Population(object):

    def __init__(self, n_start:int=1):
        self.persons = [Person(self) for n in range(n_start)]
        self.government = government.Government(self)
        for p in self:
            p.age = random.choice(range(20,80))
        self.set_mortality_rates()
        self.set_natality_rate()
        self.stats_names = ['Population','Mean age','Single males','Single females','Couples','Kids','Mean money']
        self.update_status()

    def update(self):
        [p.update() for p in self]
        self.government.update()
        self.update_status()

    def update_status(self):
        self.stats = {name:0 for name in self.stats_names}
        self.single_males = []
        self.single_females = []
        self.couples = []
        self.kids = []
        self.job_stats = {name:0 for name in jobs.JOBS}
        self.job_stats['student'] = 0
        for p in self:
            self.stats['Population'] += 1
            self.stats['Mean age'] += p.age
            self.stats['Mean money'] += p.money
            if p.couple is None and p.sex == 1 and p.age >= MAJORITY_AGE:
                self.stats['Single males'] += 1
                self.single_males.append(p)
            if p.couple is None and p.sex == 0 and p.age >= MAJORITY_AGE:
                self.stats['Single females'] += 1
                self.single_females.append(p)
            if p.couple is not None and p.couple not in self.couples:
                self.stats['Couples'] += 1
                self.couples.append(p.couple)
            if p.age < MAJORITY_AGE:
                self.stats['Kids'] += 1
                self.kids.append(p)
            if p.job is not None:
                self.job_stats[p.job.name] += 1
        try:
            self.stats['Mean age'] /= self.stats['Population']
            self.stats['Mean money'] /= self.stats['Population']
        except:
            self.stats['Mean age'] = 0
            self.stats['Mean money'] = 0

        # print(self.stats['Population'] - (self.stats['Single males']+self.stats['Single females']+2*self.stats['Couples']+self.stats['Kids']))


    def set_mortality_rates(self):
        ages = np.arange(100)
        func = np.exp(ages/10)
        self.mortality_rates = func/np.max(func)

    def set_natality_rate(self):
        self.natality_rate = 0.3

    def __len__(self):
        return len(self.persons)

    def __getitem__(self, index):
        return self.persons[index]



class Couple(object):

    def __init__(self, father, mother):
        self.father = father
        self.mother = mother
        self.love = int(np.round(random.gauss(50,20)))
        self.age = 0

    @property
    def kids(self):
        return list(set(self.father.kids + self.mother.kids))

    def update(self):

        self.love = np.clip(self.love + int(np.round(random.gauss(0,10))),0,100)

        if int(np.round(random.gauss(20,5))) > self.love:
            self.break_up()

        nb_desired_kids = int(np.round((self.father.number_of_desired_kids + self.mother.number_of_desired_kids)/2))
        if self.mother.age <= 55 and nb_desired_kids > 0:
            if self.father.population.natality_rate > random.random():
                # print('baby')
                self.father.number_of_desired_kids -= 1
                self.mother.number_of_desired_kids -= 1
                baby = Person(self.father.population)
                self.father.population.persons.append(baby)

        self.age += 1

    def break_up(self):
        # print('break')
        self.father.couple = None
        self.mother.couple = None
        del self

                    



class Person(object):

    def __init__(self, population:Population):
        self.population = population
        self.sex = random.choice([0,1])
        self.age = 0
        self.sex_appeal = int(np.clip(random.gauss(50,20),0,100))
        self.couple = None
        self.number_of_desired_kids = int(np.round(random.gauss(3,1.5)))
        self.job = None
        self.money = 0
        self.education = {}
        self.experience = {}

    def update(self):

        if random.random() < self.population.mortality_rates[self.age]:
            self.die()
            return None

        if self.sex == 1 and (self.age >= MAJORITY_AGE):
            if self.couple is not None:
                self.couple.update()
            else: 
                self.match()

        if self.job is not None:
            self.job.update()
            try: 
                self.money -= int(self.job.salary*TAX_RATE)
                self.population.government.money += int(self.job.salary*TAX_RATE)
            except: pass
        elif self.age == 5:
            self.job = jobs.Student(person=self)
        elif self.age >= 14:
            self.job = jobs.find_job(self)

        self.age += 1

    def die(self):
        # print('die')
        if self.couple is not None:
            if self.sex == 0:
                self.couple.father.couple = None
            elif self.sex == 1:
                self.couple.mother.couple = None
            
        self.population.persons.remove(self)
        del self

    def match(self):
        self.population.update_status() #FIXME : inefficient to recalculate everything, but necessary to avoid matching with dead people
        candidates = self.population.single_females
        candidates = [c for c in candidates if (c.age >= self.age/2 + 7) and (self.age >= c.age/2 + 7) and (c.age >= MAJORITY_AGE)]
        if len(candidates) > 0:
            match = random.choice(candidates)
            if np.abs(self.sex_appeal-match.sex_appeal) < 20 and random.random()>0.8 and match.couple is None:
                # print('match')
                self.couple = Couple(father=self, mother=match)
                match.couple = self.couple
                
        