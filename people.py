import random
import numpy as np
import names
import jobs
import government

MAJORITY_AGE = 18
FOOD_PRICE = 5e3
NATALITY_RATE = 0.3
LIFE_EXPECTANCY = 80
MORTALITY_RATE = 0.1


class Population(object):

    def __init__(self, n_start:int=1):
        self.persons = [Person(self) for n in range(n_start)]
        self.government = government.Government(self)
        for p in self:
            p.age = random.choice(range(20,80))
        self.stats_names = ['Population','Mean age','Mean money','Mean health','Single males','Single females','Couples','Kids']
        self.food = n_start*5
        self.update_status()

    def update(self):
        random.shuffle(self.persons)
        [p.update() for p in self]
        self.food -= int(self.food*0.2) #food decay
        self.government.update()
        self.update_status()

    def update_status(self):
        self.stats = {name:0 for name in self.stats_names}
        self.single_males = []
        self.single_females = []
        self.couples = []
        self.workers = {name:[] for name in jobs.JOBS}
        self.workers['Student'] = []
        self.unemployed = []
        self.retired = []
        self.kids = []
        self.job_stats = {name:0 for name in jobs.JOBS}
        self.job_stats['Student'] = 0
        self.job_stats['Unemployed'] = 0
        self.job_stats['Retired'] = 0
        self.positions = []
        self.scores = []
        self.colors = []
        for p in self:
            self.stats['Population'] += 1
            self.stats['Mean age'] += p.age
            self.stats['Mean money'] += p.money
            self.stats['Mean health'] += p.health
            if p.couple is None and p.sex == 1 and p.age >= MAJORITY_AGE:
                self.stats['Single males'] += 1
                self.single_males.append(p)
                p.status = 'single male'
            if p.couple is None and p.sex == 0 and p.age >= MAJORITY_AGE:
                self.stats['Single females'] += 1
                self.single_females.append(p)
                p.status = 'single female'
            if p.couple is not None:
                self.stats['Couples'] += 1
                self.couples.append(p.couple)
                p.status = 'married male' if p.sex==1 else 'married female'
            if p.age < MAJORITY_AGE:
                self.stats['Kids'] += 1
                self.kids.append(p)
                p.status = 'male kid' if p.sex==1 else 'female kid'
            if p.job is not None:
                self.job_stats[p.job.name] += 1
                self.workers[p.job.name].append(p)
            elif p.age >= MAJORITY_AGE and p.age < self.government.retirement_age:
                self.job_stats['Unemployed'] += 1
                self.unemployed.append(p)
            if p.age >= self.government.retirement_age:
                self.job_stats['Retired'] += 1
                self.retired.append(p)
            self.positions.append(p.xy)
            self.scores.append(p.score)
            self.colors.append(p.color)
        self.stats['Couples'] = int(self.stats['Couples']/2)
        self.couples = set(self.couples)
        self.positions = np.array(self.positions)
        self.scores = np.array(self.scores)
        try:
            self.stats['Mean age'] /= self.stats['Population']
            self.stats['Mean money'] /= self.stats['Population']
            self.stats['Mean health'] /= self.stats['Population']
        except:
            self.stats['Mean age'] = 0
            self.stats['Mean money'] = 0
            self.stats['Mean health'] = 0

    def __len__(self):
        return len(self.persons)

    def __getitem__(self, index):
        return self.persons[index]



class Couple(object):

    def __init__(self, father, mother):
        self.father = father
        self.mother = mother
        self.love = int(np.round(random.gauss(50,20)))
        self.father.history.append(f'Married at {self.father.age}')
        self.mother.history.append(f'Married at {self.mother.age}')
        self.age = 0

    @property
    def kids(self):
        return list(set(self.father.kids + self.mother.kids))
    @property 
    def money(self):
        return self.father.money + self.mother.money

    def update(self):

        self.love = np.clip(self.love + int(np.round(random.gauss(0,10))),0,100)

        if int(np.round(random.gauss(20,3))) > self.love:
            self.break_up()

        nb_desired_kids = int(np.round((self.father.number_of_desired_kids + self.mother.number_of_desired_kids)/2))
        if self.mother.age <= 55 and nb_desired_kids > 0:
            if NATALITY_RATE > random.random() and self.money > 0:
                baby = Person(self.father.population)
                baby.name = baby.name.split(' ')[0] + ' ' + self.father.name.split(' ')[1]
                baby.father = self.father
                baby.mother = self.mother
                self.father.population.persons.append(baby)
                for parent in [self.father, self.mother]:
                    parent.number_of_desired_kids -= 1
                    parent.kids.append(baby)
                    parent.history.append(f'Had baby at {parent.age}')
        
        self.age += 1

    def break_up(self):
        for p in [self.father, self.mother]:
            p.couple = None
            p.history.append(f'Divorced after {self.age} years of marriage')
        del self

                    



class Person(object):

    def __init__(self, population:Population):
        self.population = population
        self.sex = random.choice([0,1])
        self.name = names.get_full_name(gender='male') if self.sex==1 else names.get_full_name(gender='female')
        self.age = 0
        self.sex_appeal = int(np.clip(random.gauss(50,20),0,100))
        self.couple = None
        self.number_of_desired_kids = int(np.round(random.gauss(3,1.5)))
        self.job = None
        self.money = 0
        self.health = 100
        self.education = {}
        self.experience = {}
        self.xy = (random.random(), random.random())
        self.status = None
        self.father = None
        self.mother = None
        self.kids = []
        self.history = []

    def update(self):

        if self.sex == 1 and (self.age >= MAJORITY_AGE):
            if self.couple is not None:
                self.couple.update()
            else: 
                self.match()

        if self.job is not None:
            self.job.update()
            try: 
                self.money -= self.job.salary*self.population.government.tax_rate
                self.population.government.money += self.job.salary*self.population.government.tax_rate
            except: pass
        elif self.age == 5:
            self.job = jobs.Student(person=self)
        elif self.age >= 14 and self.age < self.population.government.retirement_age:
            self.job = jobs.find_job(self)

        self.health_decay()
        if self.health <= 0:
            self.die()
            return None

        if self.population.food > 0:
            if self.age >= MAJORITY_AGE:
                self.money -= FOOD_PRICE
            else:
                if self.father is not None:
                    self.father.money -= FOOD_PRICE/2
                else:
                    self.population.government.money -= FOOD_PRICE/2
                if self.mother is not None:
                    self.mother.money -= FOOD_PRICE/2
                else:
                    self.population.government.money -= FOOD_PRICE/2
            self.population.food -= 1
            self.age += 1
        else: 
            self.die()
            return None

    @property
    def score(self):
        score = np.clip(self.age,0,100) + np.clip(self.money/1e4,0,100)
        return score
    @property
    def color(self):
        if self.age < MAJORITY_AGE:
            return [0.8,0.8,0.1] #yellow
        else:
            if self.sex==0:
                return [1,0.3,0.3] #red
            elif self.sex == 1:
                return [0.3,0.3,1] #blue

    def health_decay(self):
        self.health -= random.random()*100*np.exp(np.log(MORTALITY_RATE)/(LIFE_EXPECTANCY-100)*(self.age-100))

    def die(self):
        if self.couple is not None:
            if self.sex == 0:
                self.couple.father.couple = None
                self.couple.father.history.append(f'Widowed after {self.couple.age} years of marriage')
            elif self.sex == 1:
                self.couple.mother.couple = None
                self.couple.mother.history.append(f'Widowed after {self.couple.age} years of marriage')

        for parent in [self.father, self.mother]:
            if parent is not None:
                parent.kids.remove(self)

        for kid in self.kids:
            if self.sex==0:
                kid.mother = None
            elif self.sex==1:
                kid.father = None
            
        self.population.persons.remove(self)
        del self

    def match(self):
        candidates = self.population.single_females
        candidates = [c for c in candidates if (c.age >= self.age/2 + 7) and (self.age >= c.age/2 + 7) and (c.age >= MAJORITY_AGE)]
        if len(candidates) > 0:
            match = random.choice(candidates)
            if np.abs(self.sex_appeal-match.sex_appeal) < 20 and random.random()>0.8 and match.couple is None:
                self.couple = Couple(father=self, mother=match)
                match.couple = self.couple
                
        