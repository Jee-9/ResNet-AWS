import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='queue-test')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        queue.send_messages(
            Entries = [
                {
                'Id' : 'start_analysis', 
                'MessageBody' : key,
                'MessageAttributes' : {
                        'About' : { 
                            'DataType' : 'String',
                            'StringValue' : 'put new video' }
                    }
                }
              ]
            )
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
