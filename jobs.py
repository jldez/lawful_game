import random
import numpy as np

MINIMUM_WAGE = 2e4
HEALTHCARE_PRICE = 1e3


class Job(object):

    def __init__(self, person, salary, promotion_name=None):
        self.person = person
        self.salary = salary
        self.years_completed = 0
        self.promotion_name = promotion_name

    def update(self):
        self.person.money += self.salary
        self.add_experience()

        if self.promotion_name is not None:
            self.check_for_promotion()

        if self.person.age >= self.person.population.government.retirement_age:
            self.person.population.job_stats[self.name] -= 1
            self.person.job = None
            self.person.history.append(f'Retired at {self.person.age}')

        elif self.name is not 'Student':
            #Check if too many workers on that job
            if self.person.population.job_stats[self.name] > np.floor(JOBS[self.name]['proportion']*len(self.person.population)):
                self.person.population.job_stats[self.name] -= 1
                self.person.job = None
                self.person.history.append(f'Fired from {self.name} job at {self.person.age}')

            else:
                self.salary = min(self.salary*1.02, JOBS[self.name]['max_salary'])

    def add_experience(self):
        self.years_completed += 1
        if self.name is not 'Student':
            try: self.person.experience[self.domain] += 1
            except: self.person.experience[self.domain] = 1

    def check_for_promotion(self):
        if self.person.population.job_stats[self.promotion_name] < np.floor(JOBS[self.promotion_name]['proportion']*len(self.person.population)):
            if is_qualified(self.person, JOBS[self.promotion_name]):
                self.person.population.job_stats[self.person.job.name] -= 1 #remove count from previous job
                self.person.job = JOBS[self.promotion_name]['class'](self.person) #change to new job
                self.person.population.job_stats[self.person.job.name] += 1 #add count to new job
                self.person.history.append(f'Promoted to {self.promotion_name} at {self.person.age}')



class Farmer(Job):
    def __init__(self, person):
        self.name = 'Farmer'
        self.domain = 'farming'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Farmer, self).update()
        self.person.population.food += 10 + min(self.person.experience[self.domain],10)

class Cook(Job):
    def __init__(self, person):
        self.name = 'Cook'
        self.domain = 'cooking'
        super().__init__(person, salary=JOBS[self.name]['base_salary'], promotion_name='Chef')
        
class Chef(Job):
    def __init__(self, person):
        self.name = 'Chef'
        self.domain = 'cooking'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    
class Secretary(Job):
    def __init__(self, person):
        self.name = 'Secretary'
        self.domain = 'bureaucracy'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Journalist(Job):
    def __init__(self, person):
        self.name = 'Journalist'
        self.domain = 'journalism'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Scientist(Job):
    def __init__(self, person):
        self.name = 'Scientist'
        self.domain = 'science'
        super().__init__(person, salary=JOBS[self.name]['base_salary'], promotion_name='Professor')

class Professor(Job):
    def __init__(self, person):
        self.name = 'Professor'
        self.domain = 'science'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Teacher(Job):
    def __init__(self, person):
        self.name = 'Teacher'
        self.domain = 'teaching'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Lawyer(Job):
    def __init__(self, person):
        self.name = 'Lawyer'
        self.domain = 'law'
        super().__init__(person, salary=JOBS[self.name]['base_salary'], promotion_name='Judge')

class Judge(Job):
    def __init__(self, person):
        self.name = 'Judge'
        self.domain = 'law'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class HealthJob(Job):
    def update(self):
        super(HealthJob, self).update()
        patient = random.choice(self.person.population)
        patient.health = np.clip(patient.health+self.health_recovery, 0, 100)
        patient.money -= self.health_recovery*HEALTHCARE_PRICE*(1-patient.population.government.public_healthcare)
        patient.population.government.money -= self.health_recovery*HEALTHCARE_PRICE*patient.population.government.public_healthcare

class Nurse(HealthJob):
    def __init__(self, person):
        self.name = 'Nurse'
        self.domain = 'medecine'
        self.health_recovery = 10
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Doctor(HealthJob):
    def __init__(self, person):
        self.name = 'Doctor'
        self.domain = 'medecine'
        self.health_recovery = 20
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Surgeon(HealthJob):
    def __init__(self, person):
        self.name = 'Surgeon'
        self.domain = 'medecine'
        self.health_recovery = 30
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Architect(Job):
    def __init__(self, person):
        self.name = 'Architect'
        self.domain = 'engineering'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Cashier(Job):
    def __init__(self, person):
        self.name = 'Cashier'
        self.domain = 'cashing'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Deputee(Job):
    def __init__(self, person):
        self.name = 'Deputee'
        self.domain = 'politics'
        super().__init__(person, salary=JOBS[self.name]['base_salary'], promotion_name='Minister')
    def update(self):
        self.person.population.government.money -= self.salary
        super(Deputee, self).update()

class Minister(Job):
    def __init__(self, person):
        self.name = 'Minister'
        self.domain = 'politics'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        self.person.population.government.money -= self.salary
        super(Minister, self).update()

class Salesman(Job):
    def __init__(self, person):
        self.name = 'Salesman'
        self.domain = 'finance'
        super().__init__(person, salary=JOBS[self.name]['base_salary'], promotion_name='Businessman')

class Businessman(Job):
    def __init__(self, person):
        self.name = 'Businessman'
        self.domain = 'finance'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])



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
        person.history.append(f'Hired as {name} at {person.age}')
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
                self.person.history.append(f'Started to study {self.domain}')
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
            self.person.history.append(f'Finished school at {self.person.age}')
            self.person.job = None
            del self
