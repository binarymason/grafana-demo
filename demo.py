import argparse
import time
import sys
import logging
from pipeline import Pipeline
from prometheus_client import start_http_server, Gauge, Counter

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

parser = argparse.ArgumentParser(description="run a pipeline")
parser.add_argument("--chaos", type=float, default=0.0)
args = parser.parse_args()
chaos = args.chaos

if not isinstance(chaos, float) or chaos > 1.0:
    print("ERROR: chaos argument should be a float between 0.0 and 1.0")
    sys.exit(1)

BYTES_PROCESSED = Gauge("pipeline_bytes_processed", "number of bytes processed for a job", ["job_name" ])
EXCEPTIONS      = Gauge("pipeline_exceptions_raised", "number of exceptions raised for a job", ["job_name"])
JOB_SECONDS     = Gauge("pipeline_job_seconds", "number of seconds for a job to run", ["job_name"])
RECORDS         = Gauge("pipeline_imported_records", "number of records imported from a job", ["job_name"])
TOTAL_BYTES     = Counter("pipeline_processed_bytes_total", "number of total bytes processed")
TOTAL_RECORDS   = Counter("pipeline_imported_records_total", "number of total records imported")
UP              = Gauge('pipeline_job_status', 'status of data pipelines jobs', ['job_name'])

EXPORTER_PORT  = 1234
SLEEP_INTERVAL = 15
if __name__ == '__main__':
    start_http_server(EXPORTER_PORT)
    logging.info(f"chaos level (chances that things will go wrong): {chaos}")
    logging.info(f"exporter listening on port {EXPORTER_PORT}")

    while True:
        logging.info("+ running pipeline...")
        p = Pipeline(num_jobs=5, chaos=chaos)
        for job in p.run():
            BYTES_PROCESSED.labels(job.name).set(job.num_bytes)
            EXCEPTIONS.labels(job.name).set(job.num_exceptions)
            JOB_SECONDS.labels(job.name).set(job.num_seconds)
            RECORDS.labels(job.name).set(job.num_records)
            TOTAL_BYTES.inc(job.num_bytes)
            TOTAL_RECORDS.inc(job.num_records)
            UP.labels(job.name).set(job.succeeded)
            logging.info(f"--> job succeeded: {job.succeeded}")
        logging.info(f"==> pipeline is considered to be working: {p.is_working}")
        logging.info(f"(sleeping for {SLEEP_INTERVAL} seconds)")
        time.sleep(SLEEP_INTERVAL)
