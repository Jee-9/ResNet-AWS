import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    sqs = boto3.resource("sqs")
    queue = sqs.get_queue_by_name(QueueName='queue-test')
    
    response = queue.send_message(
        MessageBody="message event"
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
