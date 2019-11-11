import argparse
import time
import sys
from pipeline import Pipeline
from prometheus_client import start_http_server, Gauge, Summary, Counter


parser = argparse.ArgumentParser(description="run a pipeline")
parser.add_argument("--chaos", type=float, default=0.0)
args = parser.parse_args()
chaos = args.chaos

if not isinstance(chaos, float) or chaos > 1.0:
    print("chaos argument should be a float between 0.0 and 1.0")
    sys.exit(1)


UP = Gauge('pipeline_job_status', 'status of data pipelines jobs', ['job_name'])
BYTES_PROCESSED = Gauge("pipeline_bytes_processed", "number of bytes processed for a job", ["job_name" ])
TOTAL_BYTES = Counter("pipeline_processed_bytes_total", "number of total bytes processed")
EXCEPTIONS = Gauge("pipeline_exceptions_raised", "number of exceptions raised for a job", ["job_name"])
RECORDS = Gauge("pipeline_imported_records", "number of records imported from a job", ["job_name"])
TOTAL_RECORDS = Counter("pipeline_imported_records_total", "number of total records imported")
JOB_SECONDS = Gauge("pipeline_job_seconds", "number of seconds for a job to run", ["job_name"])

if __name__ == '__main__':
    start_http_server(1234)

    while True:
        p = Pipeline(num_jobs=5, chaos=chaos)
        for job in p.run():
            UP.labels(job.name).set(job.succeeded)
            BYTES_PROCESSED.labels(job.name).set(job.num_bytes)
            TOTAL_BYTES.inc(job.num_bytes)
            EXCEPTIONS.labels(job.name).set(job.num_exceptions)
            RECORDS.labels(job.name).set(job.num_records)
            TOTAL_RECORDS.inc(job.num_records)
            JOB_SECONDS.labels(job.name).set(job.num_seconds)
        time.sleep(15)
