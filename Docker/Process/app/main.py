import os
import boto3
import csv

def write_to_bucket():
    # Grab data from environment
    aux_bucket = os.environ["AUX_BUCKET"]
    job_number = os.environ.get("AWS_BATCH_JOB_ARRAY_INDEX", "?")

    s3 = boto3.client("s3")
    data = s3.get_object(
        Bucket=aux_bucket,
        Key="list.csv")["Body"].read().decode('utf-8')

    accounts = []
    for row in csv.reader(data.split(",")):
        accounts.append(row[0])

    print("File data:", data, type(data))
    print(f"File body: {accounts}")

    file_name = f"Text{job_number}.txt"
    body = f"This is the account info: {accounts[int(job_number)]}"

    s3.put_object(
        Bucket=aux_bucket,
        Key=file_name,
        Body=body,
        ContentType=f"text/txt"
    )


if __name__ == '__main__':
    write_to_bucket()
