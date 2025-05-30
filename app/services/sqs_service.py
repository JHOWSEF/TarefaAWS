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

def initialize_queue_urls():
    global QUEUE_URL_INPUT, QUEUE_URL_PROCESSED
    QUEUE_URL_INPUT, QUEUE_URL_PROCESSED = get_queue_urls()


def create_queue_if_not_exists(queue_name):
    try:
        response = sqs.get_queue_url(QueueName=queue_name)
        return response['QueueUrl']
    except ClientError as e:
        if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
            print(f"Fila {queue_name} não existe. Criando fila...")
            sqs.create_queue(
                QueueName=queue_name,
                Attributes={
                    'FifoQueue': 'true',
                    'ContentBasedDeduplication': 'false'
                }
            )
            response = sqs.get_queue_url(QueueName=queue_name)
            return response['QueueUrl']
        else:
            print(f"Erro ao acessar fila {queue_name}: {e}")
            raise

def get_queue_urls():
    queue_url_input = create_queue_if_not_exists('new-image-input.fifo')
    queue_url_processed = create_queue_if_not_exists('new-image-processed.fifo')
    return queue_url_input, queue_url_processed

QUEUE_URL_INPUT = None
QUEUE_URL_PROCESSED = None

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
