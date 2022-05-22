from secret_file import Access_key_ID , Secret_access_key
import boto3

def get_sqs_client():
    sqs = boto3.client('sqs', region_name='us-east-1',
                    aws_access_key_id=Access_key_ID, 
                    aws_secret_access_key=Secret_access_key)
    return sqs

def send_message(Prediction_msg, image_name):
    queue_url = 'https://sqs.us-east-1.amazonaws.com/670431221643/face-recogntion-response-queue'

# Send message to SQS queue
    sqs = get_sqs_client()
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageAttributes={
            'ImageName': {
                'DataType': 'String',
                'StringValue': image_name
            }
        },
        MessageBody=(
             Prediction_msg
        )
    )


def get_message():
    queue_url = 'https://sqs.us-east-1.amazonaws.com/670431221643/face-recogntion-request-queue'

    #recieve message to SQS queue
    sqs = get_sqs_client()
    response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    WaitTimeSeconds=0
    )
    if (len(response.get('Messages', [])) != 0):
        message = response['Messages'][0]
        image_name = message['MessageAttributes']['ImageName']['StringValue']
        receipt_handle = message['ReceiptHandle']
        return message['Body'], receipt_handle , image_name
    else:
        return None, None, None

def delete_recent(receipt_handle):
    queue_url = 'https://sqs.us-east-1.amazonaws.com/670431221643/face-recogntion-request-queue'

    #recieve message to SQS queue
    sqs = get_sqs_client()
    
    sqs.delete_message( QueueUrl=queue_url, ReceiptHandle=receipt_handle )


def get_queue_length():
    queue_url = 'https://sqs.us-east-1.amazonaws.com/670431221643/face-recogntion-request-queue'
    sqs = get_sqs_client()
    
    response = sqs.get_queue_attributes(
                QueueUrl = queue_url ,
                AttributeNames=['All'] 
    )
    
    return int(response['Attributes']['ApproximateNumberOfMessages'])