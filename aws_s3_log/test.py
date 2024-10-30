import logging
import boto3
from botocore.exceptions import NoCredentialsError
from io import StringIO

# Define your AWS credentials
aws_access_key_id = "aws_access_key_id"
aws_secret_access_key = "aws_secret_access_key"
bucket_name = "bucket_name"
region_name = "region_name"

# Set up S3 client with hardcoded credentials
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name,  # Replace with your AWS region, e.g., 'us-west-1'
)

# Set up logging to stream logs to memory
log_stream = StringIO()
logging.basicConfig(level=logging.INFO, stream=log_stream)
logger = logging.getLogger()


def save_logs_to_s3(log_data, bucket_name, file_name):
    try:
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=log_data)
        print(f"Logs saved to S3 bucket '{bucket_name}' as '{file_name}'")
    except NoCredentialsError:
        print("Credentials not available.")


# Logging example
logger.info("This is a log message")
logger.info("Another log message")

# Save logs to S3
log_data = log_stream.getvalue()
file_name = (
    "logs/log_file.txt"  # Can use dynamic naming like f"logs/{datetime.now()}.txt"
)
save_logs_to_s3(log_data, bucket_name, file_name)
