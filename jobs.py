import random


class Job(object):

    def __init__(self, person, salary, required_education=None):
        self.person = person
        self.salary = salary
        self.years_completed = 0

    def update(self):
        self.years_completed += 1
        self.person.money += self.salary



class Farmer(Job):

    def __init__(self, person, salary=2e4):
        super().__init__(person, salary)


class Student(Job):

    def __init__(self, person, salary=0):
        super().__init__(person, salary)
        self.domain = 'general'

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

