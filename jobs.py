import random
import numpy as np


class Job(object):

    def __init__(self, person, salary):
        self.person = person
        self.salary = salary
        self.years_completed = 0

    def update(self):
        self.years_completed += 1
        self.person.money += self.salary
        self.salary *= 1.02

    def check_for_promotion(self, promotion_name):
        if self.person.population.job_stats[promotion_name] < JOBS[promotion_name]['proportion']*len(self.person.population):
            if is_qualified(self.person, JOBS[promotion_name]):
                self.person.population.job_stats[self.person.job.name] -= 1
                self.person.job = JOBS[promotion_name]['class'](self.person)
                self.person.population.job_stats[self.person.job.name] += 1



class Farmer(Job):
    def __init__(self, person):
        self.name = 'farmer'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    
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
        super(Scientist, self).update()
        try: self.person.experience['science'] += 1
        except: self.person.experience['science'] = 1
        self.check_for_promotion('professor')

class Professor(Job):
    def __init__(self, person):
        self.name = 'professor'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Professor, self).update()
        try: self.person.experience['science'] += 1
        except: self.person.experience['science'] = 1

class Lawyer(Job):
    def __init__(self, person):
        self.name = 'lawyer'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Lawyer, self).update()
        try: self.person.experience['law'] += 1
        except: self.person.experience['law'] = 1
        self.check_for_promotion('judge')

class Judge(Job):
    def __init__(self, person):
        self.name = 'judge'
        super().__init__(person, salary=JOBS[self.name]['base_salary'])
    def update(self):
        super(Judge, self).update()
        try: self.person.experience['law'] += 1
        except: self.person.experience['law'] = 1


JOBS = {
    'farmer':     {'class':Farmer,    'requirements':None,                                                    'base_salary':2e4, 'proportion':0.1},
    'secretary':  {'class':Secretary, 'requirements':{'education':{'general':12}},                            'base_salary':3e4, 'proportion':0.05},
    'journalist': {'class':Journalist,'requirements':{'education':{'communication':3}},                       'base_salary':3e4, 'proportion':0.02},
    'scientist':  {'class':Scientist, 'requirements':{'education':{'science':5}},                             'base_salary':6e4, 'proportion':0.03},
    'professor':  {'class':Professor, 'requirements':{'education':{'science':5},'experience':{'science':10}}, 'base_salary':1e5, 'proportion':0.01},
    'lawyer':     {'class':Lawyer,    'requirements':{'education':{'law':3}},                                 'base_salary':1e5, 'proportion':0.01},
    'judge':      {'class':Judge,     'requirements':{'education':{'law':3},    'experience':{'law':10}},     'base_salary':3e5, 'proportion':0.001},
}


def find_job(person):

    requirements_met = []

    total_population = len(person.population)

    for name in JOBS:
        if person.population.job_stats[name] < JOBS[name]['proportion']*total_population:

            if is_qualified(person, JOBS[name]):
                requirements_met.append(name)

    if len(requirements_met) > 0:
        best_job, best_salary = None, 0
        for name in requirements_met:
            if JOBS[name]['base_salary'] > best_salary:
                best_salary = JOBS[name]['base_salary']
                best_job = JOBS[name]['class']
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
