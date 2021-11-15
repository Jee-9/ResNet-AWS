import json
import boto3

region = 'ap-northeast-2'

def lambda_handler(event, context):
    
    path = event['path']
    method = event['httpMethod']
    
    if path == '/upload/youtubepj-v3':
        if method == 'GET':
            bucket_name = event['pathParameters']['bucketname']
            file_name = event['queryStringParameters']['filename'] 
                    
            s3_client = boto3.client('s3')
            response_url = s3_client.generate_presigned_url('put_object', {'Bucket' : bucket_name, 'Key' :file_name},
                                                                        ExpiresIn=3600)
                    # print(bucket_name, file_name)
                    
            return {"statusCode" : 200,
                    "headers":{
                                "Contest-Type" : "application/json",
                                'Access-Control-Allow-Origin': '*'
                                },
                    "body" : response_url
                    }

    else :
        return {"statusCode" : 200,
                "body" :   json.dumps( {
                                        "headers":{
                                                "Contest-Type" : "application/json",
                                                'Access-Control-Allow-Origin': '*'
                                                },
                                        "error" : "Please use the right URL format" } )
                  }