from random import randint

class Job(object):
    def __init__(self, *, name, chaos):
        self.name        = name
        self.num_bytes   = randint(1000,10000)
        self.num_seconds = randint(1,60)
        self.succeeded   = True

        if something_happened(chaos):
            self.num_exceptions = randint(50,100)
            self.num_records    = randint(100, 1000)
        else:
            self.num_exceptions = randint(0,49)
            self.num_records    = randint(10000,15000)

def something_happened(probability):
    """given a probability of 0.0 - 1.0 returns True or False"""
    i = randint(1,10) / 10
    return i <= probability

