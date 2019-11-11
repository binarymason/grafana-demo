from job import Job

class Pipeline(object):
    def __init__(self, *, num_jobs, chaos=0, max_exceptions=50):
        self.chaos          = chaos
        self.is_working     = True
        self.max_exceptions = max_exceptions
        self.num_jobs       = num_jobs
        self.processed_jobs = 0
        self.failed_jobs    = 0

    def run(self):
        for idx in range(self.num_jobs):
            j = Job(name=f"job-{idx}", chaos = self.chaos)
            self.processed_jobs += 1
            self.is_working = j.num_exceptions < self.max_exceptions
            if not self.is_working:
                self.failed_jobs += 1
                j.succeeded = False 

            yield j


            #  if not self.is_working:
            #      print("--------------")
            #      print("pipeline working", self.is_working)
            #      print("bytes", j.num_bytes)
            #      print("seconds", j.num_seconds)
            #      print("records", j.num_records)
            #      print("exceptions", j.num_exceptions)
