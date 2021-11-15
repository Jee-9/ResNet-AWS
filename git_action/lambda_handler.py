from lambda_defs import *
import json

# lambda handler
def lambda_handler(event, context):

    path = event['path']
    method = event['httpMethod']

    if path == '/test':
        if method == 'GET': 
            return {
                "statusCode": 200,
                "body": json.dumps(event)
            }

    elif path == '/recommend':
        if method == 'GET':

            #user_id
            user_id = event['queryStringParameters']['userid']

            # user_hist = get_user_history(user_id) 
            user_hist = get_user_history(user_id) # 하드코딩

            # class 선택하기
            selected_cls = voting(user_hist)

            # user history에서 가져온 데이터 mean 찍어서 mean vector 만들기
            user_vec = mean_history_vector(selected_cls, user_hist)

            # 선택된 클래스에 해당하는 video_id랑 video_vector 가져오기
            vid_id, vid_vec = get_class_videos(selected_cls)

            # 중복처리
            not_seen_vid_id, not_seen_vid_vec = duplication_del(selected_cls, user_hist, vid_id, vid_vec)

            # 가져온 video_id와 video_vector, user mean vector 사용해서 5개의 video_id 리턴
            rank5_vid_id = recommendation(not_seen_vid_id, not_seen_vid_vec, user_vec)

            # 5개의 video_id로 presigned_url 써서 영상 리턴하기
            response_list = get_rank5_videos(selected_cls, rank5_vid_id)

            # 각각 할당
            vid1, vid2, vid3, vid4, vid5 = rank5_vid_id
            url1, url2, url3, url4, url5 = response_list

            return {
                "statusCode" : 200,
                "headers": { 
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
                },
                "body" : json.dumps(
                    {
                        vid1 : url1,
                        vid2 : url2,
                        vid3 : url3,
                        vid4 : url4,
                        vid5 : url5
                    }
                )
            }
    