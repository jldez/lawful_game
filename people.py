import random
import numpy as np
import names
import jobs
import government
import goods_services

MAJORITY_AGE = 18
MIN_WORKING_AGE = 14
FOOD_PRICE = 5e3
LOGEMENT_PRICE = 5e3
NATALITY_RATE = 0.3
LIFE_EXPECTANCY = 80
MORTALITY_RATE = 0.1
MENOPAUSE_AGE = 55


class Population(object):

    def __init__(self, n_start:int=1):
        self.persons = [Person(self) for n in range(n_start)]
        self.government = government.Government(self)
        for p in self:
            p.age = random.choice(range(20,80))
        self.stats_names = ['Population','Age','Money','Health', 'Happiness','Single males','Single females','Couples','Kids']
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
            self.stats['Age'] += p.age
            self.stats['Money'] += p.money
            self.stats['Health'] += p.health
            self.stats['Happiness'] += p.happiness
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
            self.stats['Age'] /= self.stats['Population']
            self.stats['Money'] /= self.stats['Population']
            self.stats['Health'] /= self.stats['Population']
            self.stats['Happiness'] /= self.stats['Population']
        except:
            self.stats['Age'] = 0
            self.stats['Money'] = 0
            self.stats['Health'] = 0
            self.stats['Happiness'] = 0

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
        if self.mother.age <= MENOPAUSE_AGE and nb_desired_kids > 0:
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

    def break_up(self, history_log=True):
        for p in [self.father, self.mother]:
            p.couple = None
            if 'house' in p.belongings:
                p.belongings.pop('house') #For now, simply lose the house if the couple breaks up
            if history_log:
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
        self.job_aspiration = None
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
        self.belongings = {}

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
        elif self.age >= MIN_WORKING_AGE and self.age < self.population.government.retirement_age:
            self.job = jobs.find_job(self)

        self.health_decay()
        if self.health <= 0:
            self.die()
            return None

        if self.population.food > 0:
            self.pay(FOOD_PRICE)
            self.population.food -= 1
            self.age += 1
        else: 
            self.die()
            return None

        if 'house' not in self.belongings:
            self.pay(LOGEMENT_PRICE)

        if self.age >= MAJORITY_AGE:
            self.buy_stuff()

    def pay(self, amount):
        if self.age >= MAJORITY_AGE:
            self.money -= amount
        else:
            if self.father is not None and self.mother is not None:
                self.father.money -= amount/2
                self.mother.money -= amount/2
            elif self.father is not None and self.mother is None:
                self.father.money -= amount
            elif self.mother is not None and self.father is None:
                self.mother.money -= amount
            else:
                self.money -= amount

    def buy_stuff(self):
        if 'house' not in self.belongings and self.couple is not None and len(goods_services.AVAILABLE_GOODS['houses'])>0:
            house = goods_services.AVAILABLE_GOODS['houses'][0]
            if self.couple.money >= house.price:
                goods_services.AVAILABLE_GOODS['houses'].pop(0)
                for p in [self.couple.father,self.couple.mother]:
                    p.pay(house.price/2)
                    p.belongings['house'] = house
                    p.history.append('Bought as house')


    @property
    def score(self):
        score = np.clip(self.age, 0, 100) + np.clip(self.money/1e4, 0, 100) - np.clip(100 - self.health, 0, 100)
        return np.clip(score, 10, 100)
    @property
    def color(self):
        if self.age < MAJORITY_AGE:
            return [0.8, 0.8, 0.1] #yellow
        else:
            if self.sex == 0:
                return [1, 0.3, 0.3] #red
            elif self.sex == 1:
                return [0.3, 0.3, 1] #blue
    @property
    def happiness(self):
        happiness = 50
        if self.money < 0:
            happiness -= 10
        if self.job is not None:
            if self.job == self.job_aspiration:
                happiness += 20
            else:
                happiness -= 10
        if self.health < 50:
            happiness -= 10
        if self.couple is not None:
            if self.couple.love > 50:
                happiness += 10
            else:
                happiness -= 10
        if 'house' in self.belongings:
            happiness += 10
        return np.clip(happiness, 0, 100)

    def health_decay(self):
        # Aging
        self.health -= random.random()*100*np.exp(np.log(MORTALITY_RATE)/(LIFE_EXPECTANCY-100)*(self.age-100))
        # Sickness
        if random.random() < 0.1:
            self.health -= random.random()*30

    def die(self):
        if self.couple is not None:
            if self.sex == 0:
                self.couple.father.history.append(f'Widowed after {self.couple.age} years of marriage')
            elif self.sex == 1:
                self.couple.mother.history.append(f'Widowed after {self.couple.age} years of marriage')
            self.couple.break_up(history_log=False)

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
                
        