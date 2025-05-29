import boto3

sqs = boto3.client(
    'sqs',
    endpoint_url='http://localstack:4566'
)

QUEUE_URL_INPUT = sqs.get_queue_url(QueueName='new-image-input.fifo')['QueueUrl']
QUEUE_URL_PROCESSED = sqs.get_queue_url(QueueName='new-image-processed.fifo')['QueueUrl']

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
