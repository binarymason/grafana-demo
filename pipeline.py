from job import Job

class Pipeline(object):
    def __init__(self, *, num_jobs, chaos=0, max_exceptions=50, max_failure_rate=.5):
        self.num_jobs         = num_jobs
        self.chaos            = chaos
        self.max_exceptions   = max_exceptions
        self.max_failure_rate = max_failure_rate
        self.processed_jobs   = 0
        self.failed_jobs      = 0
        self.is_working       = True

    def run(self):
        for idx in range(self.num_jobs):
            j = Job(name=f"job-{idx}", chaos=self.chaos)
            self.processed_jobs += 1
            if self.has_failing_job(j):
                j.succeeded = False
                self.failed_jobs += 1

            yield j

            if self.has_too_many_failed_jobs():
                self.is_working = False
                return

    def has_failing_job(self, job):
        return job.num_exceptions >= self.max_exceptions

    def has_too_many_failed_jobs(self):
        return (self.failed_jobs / self.num_jobs) >= self.max_failure_rate


