import boto3
import time

def uploadToS3():
    folder_of_the_day = time.strftime(r"%Y/%m/%d/")
    full_path = folder_of_the_day + "data.json"
    client = boto3.resource('s3')
    work_bucket = client.Bucket(name="insta-trends")
    work_bucket.upload_file(
        Filename=".\\data.json",
        Key=full_path
    )