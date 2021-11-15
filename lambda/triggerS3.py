import boto3
import json
import base64
from urllib.parse import unquote_plus
import re


NEW_FILE_BUCKET_NAME = "youtubepj-newfile"
DATA_BUCKET_NAME = "youtubepj-v3"
USER_DATA_FILE_KEY = "config/user-data"
INPUT_INFO_DIR = "inputs/"


def lambda_handler(event, context):

    
    record = event["Records"][0]
    bucket = record['s3']['bucket']['name']
    key = unquote_plus(record['s3']['object']['key'], encoding='utf-8')

   

    ec2_client = boto3.client('ec2', region_name= 'ap-northeast-2')  #ec2_config['region'])
    s3_client = boto3.client('s3')

    # start EC2
    if bucket == NEW_FILE_BUCKET_NAME and key.startswith(f"{INPUT_INFO_DIR}/"):
        # write a key written text file
        key_name = re.sub('.webm', '', key)
        key_name = re.sub('input/', '', key_name)
        file_name = str(key_name) + ".txt"
        s3_path = "input_info/" + file_name

        s3 = boto3.resource("s3")
        s3.Bucket(NEW_FILE_BUCKET_NAME).put_object(Key=s3_path, Body = key)


        # copy new video file to data bucket
        copysource = bucket + key
        s3_client.copy_object(Bucket = DATA_BUCKET_NAME, 
                              CopySource=copysource,
                              Key = key)
    return { "ec2_state" : "Model is analyzing your video now"}

