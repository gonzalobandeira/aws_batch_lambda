import os
import random
import string

import boto3

'''
This lambda handler submits a job to a AWS Batch queue.
JobQueue, and JobDefinition environment variables must be set. 
These environment variables are intended to be set to the Name, not the Arn. 
'''


def lambda_handler(event, context):
    # Grab data from environment
    jobqueue = os.environ['JOB_QUEUE']
    jobdef = os.environ['JOB_DEFINITION']

    # Create unique name for the job (this does not need to be unique)
    job1Name = 'job1' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

    # Set up a batch client
    session = boto3.session.Session()
    client = session.client('batch')

    # Submit the job
    job1 = client.submit_job(
        jobName=job1Name,
        jobQueue=jobqueue,
        jobDefinition=jobdef,
        containerOverrides={
            'command': ['echo', "This is a submitted job"]
        }
    )
    print("Started Job: {}".format(job1['jobName']))

    response = {
        "statusCode": 200,
        "body": "Job submitted"
    }

    return response
