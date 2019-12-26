import random
import numpy as np

MINIMUM_WAGE = 2e4


class Job(object):

    def __init__(self, person, salary):
        self.person = person
        self.salary = salary
        self.years_completed = 0

    def update(self):
        self.person.money += self.salary
        self.years_completed += 1

        if self.name is not 'student':
            #Check if too many workers on that job
            if self.person.population.job_stats[self.name] > np.floor(JOBS[self.name]['proportion']*len(self.person.population)):
                self.person.population.job_stats[self.name] -= 1
                self.person.job = None

            else:
                self.salary *= 1.02

    def check_for_promotion(self, promotion_name):
        if self.person.population.job_stats[promotion_name] < np.floor(JOBS[promotion_name]['proportion']*len(self.person.population)):
            if is_qualified(self.person, JOBS[promotion_name]):
                self.person.population.job_stats[self.person.job.name] -= 1 #remove count from previous job
                self.person.job = JOBS[promotion_name]['class'](self.person) #change to new job
                self.person.population.job_stats[self.person.job.name] += 1 #add count to new job



class Farmer(Job):
    def __init__(self, person):
        self.name = 'farmer'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Farmer, self).update()
        self.person.population.food += 10

class Cook(Job):
    def __init__(self, person):
        self.name = 'cook'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        self.check_for_promotion('chef')
        super(Cook, self).update()
        try: self.person.experience['cooking'] += 1
        except: self.person.experience['cooking'] = 1
        
class Chef(Job):
    def __init__(self, person):
        self.name = 'chef'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Chef, self).update()
        try: self.person.experience['cooking'] += 1
        except: self.person.experience['cooking'] = 1
    
class Secretary(Job):
    def __init__(self, person):
        self.name = 'secretary'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Journalist(Job):
    def __init__(self, person):
        self.name = 'journalist'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Journalist, self).update()
        try: self.person.experience['communication'] += 1
        except: self.person.experience['communication'] = 1

class Scientist(Job):
    def __init__(self, person):
        self.name = 'scientist'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        self.check_for_promotion('professor')
        super(Scientist, self).update()
        try: self.person.experience['science'] += 1
        except: self.person.experience['science'] = 1

class Professor(Job):
    def __init__(self, person):
        self.name = 'professor'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Professor, self).update()
        try: self.person.experience['science'] += 1
        except: self.person.experience['science'] = 1

class Teacher(Job):
    def __init__(self, person):
        self.name = 'teacher'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Lawyer(Job):
    def __init__(self, person):
        self.name = 'lawyer'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        self.check_for_promotion('judge')
        super(Lawyer, self).update()
        try: self.person.experience['law'] += 1
        except: self.person.experience['law'] = 1

class Judge(Job):
    def __init__(self, person):
        self.name = 'judge'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Judge, self).update()
        try: self.person.experience['law'] += 1
        except: self.person.experience['law'] = 1

class Nurse(Job):
    def __init__(self, person):
        self.name = 'nurse'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Nurse, self).update()
        try: self.person.experience['medecine'] += 1
        except: self.person.experience['medecine'] = 1

class Doctor(Job):
    def __init__(self, person):
        self.name = 'doctor'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Doctor, self).update()
        try: self.person.experience['medecine'] += 1
        except: self.person.experience['medecine'] = 1

class Surgeon(Job):
    def __init__(self, person):
        self.name = 'surgeon'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Surgeon, self).update()
        try: self.person.experience['medecine'] += 1
        except: self.person.experience['medecine'] = 1

class Architect(Job):
    def __init__(self, person):
        self.name = 'architect'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Architect, self).update()
        try: self.person.experience['engineering'] += 1
        except: self.person.experience['engineering'] = 1

class Cashier(Job):
    def __init__(self, person):
        self.name = 'cashier'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])

class Deputee(Job):
    def __init__(self, person):
        self.name = 'deputee'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        self.check_for_promotion('minister')
        self.person.population.government.money -= self.salary
        super(Deputee, self).update()
        try: self.person.experience['politics'] += 1
        except: self.person.experience['politics'] = 1

class Minister(Job):
    def __init__(self, person):
        self.name = 'minister'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        self.person.population.government.money -= self.salary
        super(Minister, self).update()


JOBS = {
    'farmer':     {'class':Farmer,    'requirements':None,                                                    'base_salary':MINIMUM_WAGE, 'proportion':0.1},
    'cook':       {'class':Cook,      'requirements':None,                                                    'base_salary':MINIMUM_WAGE, 'proportion':0.1},
    'chef':       {'class':Chef,      'requirements':                          {'experience':{'cooking':10}}, 'base_salary':5e4,          'proportion':0.02},
    'secretary':  {'class':Secretary, 'requirements':{'education':{'general':12}},                            'base_salary':3e4,          'proportion':0.05},
    'journalist': {'class':Journalist,'requirements':{'education':{'communication':3}},                       'base_salary':3e4,          'proportion':0.02},
    'scientist':  {'class':Scientist, 'requirements':{'education':{'science':3}},                             'base_salary':6e4,          'proportion':0.03},
    'professor':  {'class':Professor, 'requirements':{'education':{'science':5},'experience':{'science':10}}, 'base_salary':1e5,          'proportion':0.01},
    'teacher':    {'class':Teacher,   'requirements':{'education':{'general':12}},                            'base_salary':5e4,          'proportion':0.07},
    'lawyer':     {'class':Lawyer,    'requirements':{'education':{'law':3}},                                 'base_salary':1e5,          'proportion':0.01},
    'judge':      {'class':Judge,     'requirements':{'education':{'law':3},    'experience':{'law':10}},     'base_salary':3e5,          'proportion':0.001},
    'nurse':      {'class':Nurse,     'requirements':{'education':{'medecine':3}},                            'base_salary':4e4,          'proportion':0.08},
    'doctor':     {'class':Doctor,    'requirements':{'education':{'medecine':5}},                            'base_salary':2e5,          'proportion':0.04},
    'surgeon':    {'class':Surgeon,   'requirements':{'education':{'medecine':8}},                            'base_salary':3e5,          'proportion':0.02},
    'architect':  {'class':Architect, 'requirements':{'education':{'engineering':3}},                         'base_salary':7e4,          'proportion':0.03},
    'cashier':    {'class':Cashier,   'requirements':None,                                                    'base_salary':MINIMUM_WAGE, 'proportion':0.05},
    'deputee':    {'class':Deputee,   'requirements':None,                                                    'base_salary':8e4,          'proportion':0.01},
    'minister':   {'class':Minister,  'requirements':{'experience':{'politics':12}},                          'base_salary':15e4,         'proportion':0.002},
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
        self.name = 'student'

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
