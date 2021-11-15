import sys
sys.path.append('packages')
import boto3
import json

from boto3.dynamodb.conditions import Key

import numpy as np
from collections import Counter
import random

# get user history
def get_user_history(userID):
    '''
    input : userID_string
    output : 
        response : [{'pk', 'video', 'video_info'}]
            description : data from DB
    '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('youtube_table_v2')

    response = table.query(
        KeyConditionExpression = Key('pk').eq(userID)
    )['Items']
    
    for row in response:
        key_name = list(row['video_info'].keys())[0]
        row['video_info'][key_name] = np.frombuffer(row['video_info'][key_name].value, dtype = 'float32')
    
    return response



# class_voting
def voting(response):
    '''
    Parameters: 
        response: [{ 'pk' : 'user#1', 
            'video' : '#10', 
            'video_info' : {'class#game' : (vectors)}}]
    Returns: class(str)
    '''
    temp = [i['video_info'].keys() for i in response]
    clses = [list(i)[0] for i in temp]
    
    x = Counter(clses).most_common()

    if x[0][1] == x[1][1]:
        class_str = random.choice(x[:2])[0]
    else:
        class_str = x[0][0] 

    return class_str 



# get_class_videos
def get_class_videos(class_str):
    '''
    parameters : 
        class_str : class_string
    return : 
        video_id : [str]
            description : video number or video id
        video_vectors : Ndarray(float)
            shape : (n, 2048)
    '''
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('youtube_table_v2')

    response = table.query(
        KeyConditionExpression = Key('pk').eq(class_str)
    )['Items']

    video_id = []
    video_vectors = np.zeros(shape = (1, 2048))
    for row in response:
        video_id.append(row['video'])
        tmp = np.frombuffer(row['vector'].value, dtype = 'float32')
        video_vectors = np.append(video_vectors, tmp.reshape(1,-1), axis = 0)
    
    video_vectors = np.delete(video_vectors, 0, axis=0)

    return video_id, video_vectors


# mean_history_vector
def mean_history_vector(class_str, response):
    '''
    parameters : 
        class_str = voted_class : str_class category
        response : history_list 
            description : [{user_history}]
    return :
        mean_vector : Ndarray(float)
            description : (1, 2048)
    '''
    voted_vector_arr = np.zeros(shape = (1,2048))
    for history in response:
        key_name = list(history['video_info'].keys())[0]
        if key_name == class_str:
            voted_vector_arr = np.append(voted_vector_arr, history['video_info'][key_name].reshape(1,-1), axis = 0)
    
    voted_vector_arr = np.delete(voted_vector_arr, 0, axis = 0)

    mean_vector = np.mean(voted_vector_arr, axis = 0)
    mean_vector = mean_vector.reshape(1, -1)

    return mean_vector



# recommend_video_dot product
def recommendation(video_id, video_vectors, mean_vectors):
    '''
    Parameters:
        video_id: [str]
            format: #1
        video_vectors: ndarray(float)
            shape: (n, 2048)
        mean_vectors: ndarray(float)
            shape: (1, 2048)
    Return:
        rank5_video_id: [str] * 5
    '''
    dic_list = []
    for i in range(len(video_id)):
        dic = {}
        dic[video_id[i]] = video_vectors[i]
        dic_list.append(dic)


    x = list(np.dot(video_vectors, mean_vectors.reshape(2048, 1)))
    '''
    description : (n, 2048) * (2048, 1) 
         return : (n, 1) '''

    sorted_idx_vec = sorted(list(zip(x, video_id)), reverse=True)
    rank5 = sorted_idx_vec[:5]

    rank5_video_id = []

    for i in range(len(rank5)):
        k = rank5[i][1]
        rank5_video_id.append(k)

    return rank5_video_id

def get_rank5_videos(class_str, rank5_video_id):
    '''
    Parameters:
        rank5_video_id[str]
    Returns:
        url(str)
    '''
    folder = class_str[6:]
    s3_client = boto3.client('s3')
    url_list = []
    
    for idx, vid in enumerate(rank5_video_id):
        vid = vid.replace('#', "-")
        response_url = s3_client.generate_presigned_url(
            'get_object',
            Params = {
                'Bucket' : 'youtubepj-v3',

                'Key' : '{}/{}'.format(folder, folder+ vid + '.webm')},

            ExpiresIn = 3600
        )
        url_list.append(response_url)

    return url_list

def duplication_del(selected_cls, user_hist, vid_id, vid_vec):
    seen_vids_in_cls = [i['video'] for i in user_hist if list(i['video_info'].keys())[0]==selected_cls]
    
    seen_vids_set = set(seen_vids_in_cls)
    vid_id_set = set(vid_id)
    not_seen_vid_id = list(vid_id_set - seen_vids_set)

    not_seen_vid_vec = np.zeros(shape=(1,2048))# vid_vec
    for i, id_ in enumerate(vid_id):
        if id_ in not_seen_vid_id:
            not_seen_vid_vec = np.append(not_seen_vid_vec, vid_vec[i].reshape(1, -1), axis = 0)

    not_seen_vid_vec = np.delete(not_seen_vid_vec, 0, axis = 0)
    return not_seen_vid_id, not_seen_vid_vec