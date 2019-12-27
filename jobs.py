import random
import numpy as np

MINIMUM_WAGE = 2e4
RETIREMENT_AGE = 65


class Job(object):

    def __init__(self, person, salary):
        self.person = person
        self.salary = salary
        self.years_completed = 0

    def update(self):
        self.person.money += self.salary
        self.years_completed += 1

        if self.person.age >= RETIREMENT_AGE:
            self.person.population.job_stats[self.name] -= 1
            self.person.job = None

        elif self.name is not 'Student':
            #Check if too many workers on that job
            if self.person.population.job_stats[self.name] > np.floor(JOBS[self.name]['proportion']*len(self.person.population)):
                self.person.population.job_stats[self.name] -= 1
                self.person.job = None

            else:
                self.salary = min(self.salary*1.02, JOBS[self.name]['max_salary'])

    def check_for_promotion(self, promotion_name):
        if self.person.population.job_stats[promotion_name] < np.floor(JOBS[promotion_name]['proportion']*len(self.person.population)):
            if is_qualified(self.person, JOBS[promotion_name]):
                self.person.population.job_stats[self.person.job.name] -= 1 #remove count from previous job
                self.person.job = JOBS[promotion_name]['class'](self.person) #change to new job
                self.person.population.job_stats[self.person.job.name] += 1 #add count to new job



class Farmer(Job):
    def __init__(self, person):
        self.name = 'Farmer'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Farmer, self).update()
        self.person.population.food += 10

class Cook(Job):
    def __init__(self, person):
        self.name = 'Cook'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        self.check_for_promotion('Chef')
        super(Cook, self).update()
        try: self.person.experience['cooking'] += 1
        except: self.person.experience['cooking'] = 1
        
class Chef(Job):
    def __init__(self, person):
        self.name = 'Chef'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Chef, self).update()
        try: self.person.experience['cooking'] += 1
        except: self.person.experience['cooking'] = 1
    
class Secretary(Job):
    def __init__(self, person):
        self.name = 'Secretary'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Journalist(Job):
    def __init__(self, person):
        self.name = 'Journalist'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Journalist, self).update()
        try: self.person.experience['communication'] += 1
        except: self.person.experience['communication'] = 1

class Scientist(Job):
    def __init__(self, person):
        self.name = 'Scientist'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        self.check_for_promotion('Professor')
        super(Scientist, self).update()
        try: self.person.experience['science'] += 1
        except: self.person.experience['science'] = 1

class Professor(Job):
    def __init__(self, person):
        self.name = 'Professor'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Professor, self).update()
        try: self.person.experience['science'] += 1
        except: self.person.experience['science'] = 1

class Teacher(Job):
    def __init__(self, person):
        self.name = 'Teacher'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Lawyer(Job):
    def __init__(self, person):
        self.name = 'Lawyer'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        self.check_for_promotion('Judge')
        super(Lawyer, self).update()
        try: self.person.experience['law'] += 1
        except: self.person.experience['law'] = 1

class Judge(Job):
    def __init__(self, person):
        self.name = 'Judge'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Judge, self).update()
        try: self.person.experience['law'] += 1
        except: self.person.experience['law'] = 1

class Nurse(Job):
    def __init__(self, person):
        self.name = 'Nurse'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Nurse, self).update()
        try: self.person.experience['medecine'] += 1
        except: self.person.experience['medecine'] = 1

class Doctor(Job):
    def __init__(self, person):
        self.name = 'Doctor'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Doctor, self).update()
        try: self.person.experience['medecine'] += 1
        except: self.person.experience['medecine'] = 1

class Surgeon(Job):
    def __init__(self, person):
        self.name = 'Surgeon'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Surgeon, self).update()
        try: self.person.experience['medecine'] += 1
        except: self.person.experience['medecine'] = 1

class Architect(Job):
    def __init__(self, person):
        self.name = 'Architect'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Architect, self).update()
        try: self.person.experience['engineering'] += 1
        except: self.person.experience['engineering'] = 1

class Cashier(Job):
    def __init__(self, person):
        self.name = 'Cashier'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Deputee(Job):
    def __init__(self, person):
        self.name = 'Deputee'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        self.check_for_promotion('Minister')
        self.person.population.government.money -= self.salary
        super(Deputee, self).update()
        try: self.person.experience['politics'] += 1
        except: self.person.experience['politics'] = 1

class Minister(Job):
    def __init__(self, person):
        self.name = 'Minister'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        self.person.population.government.money -= self.salary
        super(Minister, self).update()

class Salesman(Job):
    def __init__(self, person):
        self.name = 'Salesman'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        self.check_for_promotion('Businessman')
        super(Salesman, self).update()
        try: self.person.experience['finance'] += 1
        except: self.person.experience['finance'] = 1

class Businessman(Job):
    def __init__(self, person):
        self.name = 'Businessman'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Businessman, self).update()
        try: self.person.experience['finance'] += 1
        except: self.person.experience['finance'] = 1


JOBS = {
    'Farmer':     {'class':Farmer,     'requirements':None,                                                    'base_salary':3e4,          'max_salary':3e4,              'proportion':0.1},
    'Cook':       {'class':Cook,       'requirements':None,                                                    'base_salary':MINIMUM_WAGE, 'max_salary':MINIMUM_WAGE*1.2, 'proportion':0.1},
    'Chef':       {'class':Chef,       'requirements':                          {'experience':{'cooking':10}}, 'base_salary':5e4,          'max_salary':1e5,              'proportion':0.02},
    'Secretary':  {'class':Secretary,  'requirements':{'education':{'general':12}},                            'base_salary':3e4,          'max_salary':5e4,              'proportion':0.05},
    'Journalist': {'class':Journalist, 'requirements':{'education':{'communication':3}},                       'base_salary':3e4,          'max_salary':7e4,              'proportion':0.02},
    'Scientist':  {'class':Scientist,  'requirements':{'education':{'science':3}},                             'base_salary':6e4,          'max_salary':8e4,              'proportion':0.03},
    'Professor':  {'class':Professor,  'requirements':{'education':{'science':5},'experience':{'science':10}}, 'base_salary':1e5,          'max_salary':2e5,              'proportion':0.01},
    'Teacher':    {'class':Teacher,    'requirements':{'education':{'general':12}},                            'base_salary':5e4,          'max_salary':7e4,              'proportion':0.07},
    'Lawyer':     {'class':Lawyer,     'requirements':{'education':{'law':3}},                                 'base_salary':1e5,          'max_salary':2e5,              'proportion':0.01},
    'Judge':      {'class':Judge,      'requirements':{'education':{'law':3},    'experience':{'law':10}},     'base_salary':2e5,          'max_salary':3e5,              'proportion':0.001},
    'Nurse':      {'class':Nurse,      'requirements':{'education':{'medecine':3}},                            'base_salary':4e4,          'max_salary':8e4,              'proportion':0.08},
    'Doctor':     {'class':Doctor,     'requirements':{'education':{'medecine':5}},                            'base_salary':2e5,          'max_salary':3e5,              'proportion':0.04},
    'Surgeon':    {'class':Surgeon,    'requirements':{'education':{'medecine':8}},                            'base_salary':3e5,          'max_salary':5e5,              'proportion':0.02},
    'Architect':  {'class':Architect,  'requirements':{'education':{'engineering':3}},                         'base_salary':7e4,          'max_salary':1e5,              'proportion':0.03},
    'Cashier':    {'class':Cashier,    'requirements':None,                                                    'base_salary':MINIMUM_WAGE, 'max_salary':MINIMUM_WAGE*1.2, 'proportion':0.05},
    'Deputee':    {'class':Deputee,    'requirements':None,                                                    'base_salary':8e4,          'max_salary':8e4,              'proportion':0.01},
    'Minister':   {'class':Minister,   'requirements':{'experience':{'politics':12}},                          'base_salary':15e4,         'max_salary':15e4,             'proportion':0.002},
    'Salesman':   {'class':Salesman,   'requirements':{'education': {'finance':1}},                            'base_salary':4e4,          'max_salary':8e4,              'proportion':0.07},
    'Businessman':{'class':Businessman,'requirements':{'education': {'finance':3}, 'experience':{'finance':5}},'base_salary':1e5,          'max_salary':5e5,              'proportion':0.03},
}
# print(sum([JOBS[n]['proportion'] for n in JOBS]))


def find_job(person):

    requirements_met = []

    total_population = len(person.population)

    for name in JOBS:
        if person.population.job_stats[name] < np.floor(JOBS[name]['proportion']*total_population):

            if is_qualified(person, JOBS[name]):
                requirements_met.append(name)

    if len(requirements_met) > 0:
        best_job, best_salary = None, 0
        for name in requirements_met:
            if JOBS[name]['base_salary'] > best_salary:
                best_salary = JOBS[name]['base_salary']
                best_job = JOBS[name]['class']
        person.population.job_stats[name] += 1
        return best_job(person)
    else:
        return None

def is_qualified(person, job):
    qualified = True
    if job['requirements'] is not None:
        if 'education' in job['requirements']:
            for domain in job['requirements']['education']:
                if domain not in person.education:
                    qualified = False
                    continue
                if person.education[domain] < job['requirements']['education'][domain]:
                    qualified = False
        if 'experience' in job['requirements']:
            for domain in job['requirements']['experience']:
                if domain not in person.experience:
                    qualified = False
                    continue
                if person.experience[domain] < job['requirements']['experience'][domain]:
                    qualified = False
    return qualified



class Student(Job):

    def __init__(self, person, salary=0):
        super().__init__(person, salary)
        self.domain = 'general'
        self.name = 'Student'

    def update(self):
        super(Student, self).update()
        end_studies = False
        try: self.person.education[self.domain] += 1
        except: self.person.education[self.domain] = 1
        if self.person.age >= 14 and self.person.age < 18 and random.random() < 0.1:
            end_studies = True
        elif self.person.age == 18:
            if random.random() < 0.3:
                end_studies = True
            else:
                self.domain = random.choice(['science',
                                             'communication',
                                             'finance',
                                             'engineering',
                                             'medecine',
                                             'law',
                                            ])
        elif self.person.age > 18:
            if self.person.age < 20:
                if random.random() < 0.1:
                    end_studies = True
            elif self.person.age < 25:
                if random.random() < 0.2:
                    end_studies = True
            elif self.person.age >= 25:
                if random.random() < 0.4:
                    end_studies = True
            elif self.person.age >= 30:
                end_studies = True
            
        if end_studies:
            self.person.job = None
            del self
