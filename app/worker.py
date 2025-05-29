from .services import s3_service, sqs_service
from .image_processor import binarize_image

def process_message():
    messages = sqs_service.receive_messages(sqs_service.QUEUE_URL_INPUT)
    if not messages:
        print("No messages to process.")
        return

    for msg in messages:
        filename = msg['Body']
        print(f"Processing {filename}")

        image_bytes = s3_service.download_file('image-input', filename)
        processed_image = binarize_image(image_bytes)

        s3_service.upload_file('image-output', filename, 
                               file_data=bytes(processed_image))

        sqs_service.send_message(sqs_service.QUEUE_URL_PROCESSED, filename)
        sqs_service.delete_message(sqs_service.QUEUE_URL_INPUT, msg['ReceiptHandle'])
