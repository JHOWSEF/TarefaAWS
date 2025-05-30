import boto3
import os
from botocore.exceptions import ClientError

sqs = boto3.client(
    'sqs',
    endpoint_url=os.getenv('SQS_ENDPOINT', 'http://localstack:4566'),
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'test'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'test')
)


def get_queue_url(queue_name):
    try:
        response = sqs.get_queue_url(QueueName=queue_name)
        return response['QueueUrl']
    except ClientError as e:
        print(f"❌ Queue {queue_name} not found: {e}")
        raise


QUEUE_URL_INPUT = get_queue_url('new-image-input.fifo')
QUEUE_URL_PROCESSED = get_queue_url('new-image-processed.fifo')


def send_message(queue_url, body, group_id='default'):
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=body,
        MessageGroupId=group_id
    )


def receive_messages(queue_url):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=2
    )
    return response.get('Messages', [])


def delete_message(queue_url, receipt_handle):
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
