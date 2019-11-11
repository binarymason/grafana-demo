import random

def bytes():
    return random.randint(1000,10000)

def seconds():
    return random.randint(1,60)

def records(chaos):
    if something_happened(chaos):
        return random.randint(100, 1000)
    else:
        return random.randint(10000,15000)

def exceptions(chaos):
    if something_happened(chaos):
        return random.randint(50,100)
    else:
        return random.randint(0, 49)

def something_happened(probability):
    """given a probability of 0.0 - 1.0 returns True or False"""

    i = random.randint(1,10) / 10
    #  print(i, "<=", probability, i <= probability)
    return i <= probability
