import csv
from io import StringIO
import random
import string
import boto3


def write_to_bucket():
    file_name = f"list.csv"

    # Create csv file with a list
    data = ["avion", "barco", "coche"]

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
    client = session.client('batch', region_name="eu-central-1")

    # Create unique name for the job (this does not need to be unique)
    job1Name = 'job1' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    # Grab data from environment
    jobqueue = "batch-poc-job-queue-dev"
    jobdef = "batch-poc-job-definition-process-dev"

    jobProcess = client.submit_job(
        jobName=job1Name,
        jobQueue=jobqueue,
        jobDefinition=jobdef,
        arrayProperties={
            "size": len(data)
        })
    """
    ,
        containerOverrides={
            'command': ['echo', "This is a submitted", "echo", "${AWS_BATCH_JOB_ARRAY_INDEX}"]
        },
        dependsOn=[
            {
                'type': 'SEQUENTIAL'
            },
        ]
    )
    """
    print("Job submitted correctly")
if __name__ == '__main__':
    write_to_bucket()
