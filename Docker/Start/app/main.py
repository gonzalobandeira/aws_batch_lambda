import csv
import os
from io import StringIO

import boto3


def write_to_bucket():
    # Grab data from environment
    jobqueue = os.environ['JOB_QUEUE']
    jobdef_process = os.environ['JOB_DEFINITION_PROCESS']
    region = os.environ['REGION']

    # Create csv file with a list
    data = ["avion", "barco", "coche"]
    file_name = f"list.csv"
    csv_buffer = StringIO()
    wr = csv.writer(csv_buffer, quoting=csv.QUOTE_ALL)
    wr.writerow(data)

    s3 = boto3.client("s3")
    s3.put_object(
        Bucket="poc-batch-gbandeira",
        Key=file_name,
        Body=csv_buffer.getvalue(),
    )
    print(f"File {file_name} saved correctly")

    # Submit the jobs according to length of the list
    # Set up a batch client
    session = boto3.session.Session()
    client = session.client('batch', region_name=region)

    jobname = "ProcessJob"

    job = client.submit_job(
        jobName=jobname,
        jobQueue=jobqueue,
        jobDefinition=jobdef_process,
        arrayProperties={
            "size": len(data)
        }
    )

    print(f"{job['jobName']} submitted correctly")


if __name__ == '__main__':
    write_to_bucket()
