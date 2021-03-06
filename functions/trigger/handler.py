try:
    import unzip_requirements  # noqa: F401
except ImportError:
    pass

import base64
import datetime
import os

import boto3
from botocore.exceptions import ClientError

'''
This lambda handler submits a job to a AWS Batch queue.
JobQueue, and JobDefinition environment variables must be set. 
These environment variables are intended to be set to the Name, not the Arn. 
'''


def get_secret(secret_name, region_name, user_password=None):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret


def lambda_handler(event, context):
    # Grab data from environment
    jobqueue = os.environ['JOB_QUEUE']
    jobdef_start = os.environ['JOB_DEFINITION_START']

    """
    # Get Secrets
    secret_location = os.environ["TEST_SECRET"]
    region = "eu-central-1"

    secreto = json.loads(get_secret(secret_location, region, user_password=True))
    """

    # Set up a batch client
    session = boto3.session.Session()
    client = session.client('batch')

    jobname = "StartJob"

    # Submit the job
    job = client.submit_job(
        jobName=jobname,
        jobQueue=jobqueue,
        jobDefinition=jobdef_start
    )

    print("Started Job: {}".format(job['jobName']))

    response = {
        "statusCode": 200,
        "body": f"Start job was submitted: {datetime.datetime.now()}"
    }
    return response
