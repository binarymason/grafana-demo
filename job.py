import possible

class Job(object):
    def __init__(self, *, name, chaos):
        self.name           = name
        self.num_bytes      = possible.bytes()
        self.num_seconds    = possible.seconds()
        self.num_exceptions = possible.exceptions(chaos)
        self.num_records    = possible.records(chaos)
        self.succeeded      = True


