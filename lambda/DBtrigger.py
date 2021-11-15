import json
import boto3
from urllib.parse import unquote_plus
import re

instanceID = ['i-034aacd6f54b-----']


def lambda_handler(event, context):
    
    if event['Records'][0]['eventName'] == 'INSERT':
        ec2_client = boto3.client('ec2')
        ec2_client.stop_instances(
                InstanceIds = instanceID
            )
        new_video_key = unquote_plus(event['Records'][0]['dynamodb']['NewImage']['video']['S'])


    # delte input information file
    new_video_txt = re.sub('.webm', '.txt', new_video_key)
    s3_path = "input_info/" + new_video_txt
    s3_client = boto3.client('s3')
    s3_client.delete_object(Bucket = 'youtubepj-newfile', Key = s3_path)

    print("Video Analysis is completed!")
    return {'video name' : new_video_key}