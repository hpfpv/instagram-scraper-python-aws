from instaScraper.modules.instance import get_instance
from instaScraper.modules.stories import get_followers_stories, check_for_new_stories, story_time_str
from instaScraper.modules.download import profile_picture, story_media

import os
import boto3
import json
from datetime import datetime
import logging

client = boto3.client('dynamodb', region_name='us-east-1')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

bucket = os.environ['STORIES_BUCKET']
s3 = boto3.client('s3')

def get_followers_stories_if_mentionned(account_to_mention):
    """
        Stores story items data if featured account is mentionned

    """
    log = {}
    log["function"] = "get_followers_stories_if_mentionned"

    
    # Create Instaloader Instance
    instance = get_instance()

    # Get stories of followers
    stories = get_followers_stories(instance, account_to_mention)

    current_date_time = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")

    # Check for newest stories and save them when mentionned
    dir = "instaScraper/tagged-stories/"
    new_stories = check_for_new_stories(stories, account_to_mention)
    response = []
    if new_stories["status"] == True:
        log["message"] = "New stories found"
        logger.info(json.dumps(log))
        for x in [current_date_time, "latest"]:
            filekey = dir + x + ".json"
            s3.put_object(Bucket=bucket, Key=filekey, Body=str(json.dumps(new_stories["body"])))
        response = new_stories["body"]
        return {
                "status": True, 
                "body": response
            }
    else:
        log["message"] = "No new stories"
        logger.info(json.dumps(log))
        return {
                "status": False, 
                "body": response
            }
def formated_response_json(stories):
    logger.info(stories)
    response = []
    if(stories["status"] == True):
        for story in stories["body"]:
            story_owner = story["node"]["owner"]["username"]
            story_id = story["node"]["id"]
            story_owner_profile_pic_url = story["node"]["owner"]["profile_pic_url"]
            story_is_video = story["node"]["is_video"]
            taken_at_timestamp = story["node"]["taken_at_timestamp"]
            time = story_time_str(taken_at_timestamp)
            if story_is_video:
                story_video_url = story["node"]["video_resources"][0]["src"]
                story_media_url = story_video_url
                story_display_url = story["node"]["display_url"]
                story_duration = story["node"]["video_duration"] * 1000
            else:
                story_video_url = ""
                story_display_url = story["node"]["display_url"]
                story_media_url = story_display_url
                story_duration = 5000

            profile_picture(story_owner_profile_pic_url, story_owner)
            story_media(story_video_url, story_display_url, story_is_video, story_id)

            data = {
                'story_id': story_id,
                'story_time': time,
                'user': story_owner,
                # "story_owner_profile_pic_url": story_owner_profile_pic_url,
                # 'path_to_profile_pic': path_to_profile_pic,
                'is_video': story_is_video,
                "story_media_url": story_media_url,
                'media': story_id,
                'time': story_duration
            }
            response.append(data)
        logger.info(response)
    return json.dumps(response)

def lambda_handler(event, context):
    logger.info(event)
    for record in event ['Records']:
        if record['eventName'] == 'INSERT':
            requestId = record['dynamodb']['NewImage']['requestId']['S']
            account_to_mention = record['dynamodb']['NewImage']['account']['S']
            # stories = get_followers_stories_if_mentionned(account_to_mention)
            stories = {"status": True, "body": [{'node': {'audience': 'MediaAudience.DEFAULT', '__typename': 'GraphStoryVideo', 'id': '2731478126261253082', 'dimensions': {'height': 1137, 'width': 640}, 'display_resources': [{'src': 'https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e15/268325729_750579929667364_4176218990049020135_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=104&_nc_ohc=iS0YG2gsS-AAX_BczQ1&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-206xMPyG3Fy1VF2I-9z7JwfZgN9gdqDV0AU-6Kx506A&oe=61C0872D&_nc_sid=21929d', 'config_width': 640, 'config_height': 1137}, {'src': 'https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e15/268325729_750579929667364_4176218990049020135_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=104&_nc_ohc=iS0YG2gsS-AAX_BczQ1&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-206xMPyG3Fy1VF2I-9z7JwfZgN9gdqDV0AU-6Kx506A&oe=61C0872D&_nc_sid=21929d', 'config_width': 750, 'config_height': 1332}, {'src': 'https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e15/268325729_750579929667364_4176218990049020135_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=104&_nc_ohc=iS0YG2gsS-AAX_BczQ1&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-206xMPyG3Fy1VF2I-9z7JwfZgN9gdqDV0AU-6Kx506A&oe=61C0872D&_nc_sid=21929d', 'config_width': 1080, 'config_height': 1918}], 'display_url': 'https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e15/268325729_750579929667364_4176218990049020135_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=104&_nc_ohc=iS0YG2gsS-AAX_BczQ1&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-206xMPyG3Fy1VF2I-9z7JwfZgN9gdqDV0AU-6Kx506A&oe=61C0872D&_nc_sid=21929d', 'media_preview': 'ABgqtrU6tiqwOamGKxTOhlrzKKr5oq+YixUDYqUPVYen8qeCfpWRoWc96KjU0UxFXNKDTFp1AiVTRS0Uij//2Q==', 'gating_info': None, 'fact_check_overall_rating': None, 'fact_check_information': None, 'sharing_friction_info': {'should_have_sharing_friction': False, 'bloks_app_url': None}, 'media_overlay_info': None, 'sensitivity_friction_info': None, 'taken_at_timestamp': 1639837585, 'expiring_at_timestamp': 1639923985, 'story_cta_url': None, 'story_view_count': None, 'is_video': True, 'owner': {'id': '255391219', 'profile_pic_url': 'https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-19/s150x150/69239464_2715622995147419_7869939009076592640_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=111&_nc_ohc=a9xERC0RLVoAX81oZty&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT9BSIP6fybyX7Ot0IPBONtlflatO5mIFMah2JsjwDxuPg&oe=61C44BFA&_nc_sid=21929d', 'username': '229eaglemotion', 'followed_by_viewer': False, 'requested_by_viewer': False}, 'tracking_token': 'eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiMDZmYTI4YTRlZDYzNDBkNTg0MWU0ZjBhMDVkZWVlNmUyNzMxNDc4MTI2MjYxMjUzMDgyIiwic2VydmVyX3Rva2VuIjoiMTYzOTgzNzYxNDg0NHwyNzMxNDc4MTI2MjYxMjUzMDgyfDUwNzU0MjIyNzA3fGE4MWJkYmM5NTJmYTY5ZDBmMDkwYWJmYzkzYWU3MDJhZjRiNjNhNjNmOGE0MDFhYjJiMDJhNGVhMjdkMzNiY2YifSwic2lnbmF0dXJlIjoiIn0=', 'has_audio': True, 'overlay_image_resources': None, 'video_duration': 2.09, 'video_resources': [{'src': 'https://instagram.fcoo1-2.fna.fbcdn.net/v/t50.12441-16/267669894_1088701278572441_1590994383961152622_n.mp4?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=105&_nc_ohc=TlwyXbiOa6kAX8Nj5us&edm=AHlfZHwBAAAA&ccb=7-4&oe=61C03E21&oh=00_AT-HDS2adHWgNNKqOgGQ0rEMIUG-M_5adGXSXkRkAyYGXQ&_nc_sid=21929d', 'config_width': 480, 'config_height': 852, 'mime_type': 'video/mp4; codecs="avc1.42E01E, mp4a.40.2"', 'profile': 'BASELINE'}], 'tappable_objects': [{'__typename': 'GraphTappableMention', 'x': 0.5, 'y': 0.27811094452773605, 'width': 0.32007999999999903, 'height': 0.044977511244377, 'rotation': 0.0, 'custom_title': None, 'attribution': None, 'username': '229eaglemotion', 'full_name': '229eaglemotion', 'is_private': False}], 'story_app_attribution': None, 'edge_media_to_sponsor_user': {'edges': []}, 'muting_info': None}, 'instaloader': {'version': '4.8.2', 'node_type': 'StoryItem'}}, {'node': {'audience': 'MediaAudience.DEFAULT', '__typename': 'GraphStoryImage', 'id': '2730293655191842125', 'dimensions': {'height': 1334, 'width': 750}, 'display_resources': [{'src': 'https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/sh0.08/e35/p640x640/268445457_1367745210331147_8589600088301699084_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=Qqq-1z9oObUAX89hiy3&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-C7JrYZlTWjG2FMHg8x37sE6b_-TW6AQ7YrRpYxAWKdg&oe=61BE5903&_nc_sid=21929d', 'config_width': 640, 'config_height': 1138}, {'src': 'https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e35/268445457_1367745210331147_8589600088301699084_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=Qqq-1z9oObUAX89hiy3&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_y_YXEgUGimKvcGolnonas6ysyd5sIrTaC-CBa7CmXIw&oe=61BDCF1B&_nc_sid=21929d', 'config_width': 750, 'config_height': 1334}, {'src': 'https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e35/268445457_1367745210331147_8589600088301699084_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=Qqq-1z9oObUAX89hiy3&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_y_YXEgUGimKvcGolnonas6ysyd5sIrTaC-CBa7CmXIw&oe=61BDCF1B&_nc_sid=21929d', 'config_width': 1080, 'config_height': 1920}], 'display_url': 'https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e35/268445457_1367745210331147_8589600088301699084_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=Qqq-1z9oObUAX89hiy3&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_y_YXEgUGimKvcGolnonas6ysyd5sIrTaC-CBa7CmXIw&oe=61BDCF1B&_nc_sid=21929d', 'media_preview': 'ABgq5qiiigAooooAKKKKACiiigAooooAKKKKAP/Z', 'gating_info': None, 'fact_check_overall_rating': None, 'fact_check_information': None, 'sharing_friction_info': {'should_have_sharing_friction': False, 'bloks_app_url': None}, 'media_overlay_info': None, 'sensitivity_friction_info': None, 'taken_at_timestamp': 1639696382, 'expiring_at_timestamp': 1639782782, 'story_cta_url': None, 'story_view_count': None, 'is_video': False, 'owner': {'id': '255391219', 'profile_pic_url': 'https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-19/s150x150/69239464_2715622995147419_7869939009076592640_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=111&_nc_ohc=a9xERC0RLVoAX81oZty&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT86OB_d0-AzZQ8hEYoPkAVfF12zbZdgxk7HCSD2OLikQA&oe=61C251BA&_nc_sid=21929d', 'username': 'hpfpv', 'followed_by_viewer': False, 'requested_by_viewer': False}, 'tracking_token': 'eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiZmQ3NGI2ZTFlZTM1NDE2M2E2YTIzNzM5N2IzOTJmM2YyNzMwMjkzNjU1MTkxODQyMTI1Iiwic2VydmVyX3Rva2VuIjoiMTYzOTY5OTMwMjU3OHwyNzMwMjkzNjU1MTkxODQyMTI1fDUwNzU0MjIyNzA3fDY1MTRkNjUyZGRiZDNhZmNiMWVlZTdhMzIwZmIyYTg1YzNmOTNhMGM4ZjYzMTlhYzQ3Y2IwZTk2OGY5MmU1YTUifSwic2lnbmF0dXJlIjoiIn0=', 'tappable_objects': [{'__typename': 'GraphTappableMention', 'x': 0.5, 'y': 0.27811094452773605, 'width': 0.32007999999999903, 'height': 0.044977511244377, 'rotation': 0.0, 'custom_title': None, 'attribution': None, 'username': '229eaglemotion', 'full_name': '229eaglemotion', 'is_private': False}], 'story_app_attribution': None, 'edge_media_to_sponsor_user': {'edges': []}, 'muting_info': None}, 'instaloader': {'version': '4.8.2', 'node_type': 'StoryItem'}}, {'node': {'audience': 'MediaAudience.DEFAULT', '__typename': 'GraphStoryImage', 'id': '2729916333045328299', 'dimensions': {'height': 1334, 'width': 750}, 'display_resources': [{'src': 'https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/sh0.08/e35/p640x640/268430240_648286416303865_1516137624972219047_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=101&_nc_ohc=pTOrC1zKXpsAX-dMaN0&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-IVvTdxXeE3zGN8XjiI8Irk74aRFrFdyyEliOxyO5g_Q&oe=61BE0FFA&_nc_sid=21929d', 'config_width': 640, 'config_height': 1138}, {'src': 'https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e35/268430240_648286416303865_1516137624972219047_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=101&_nc_ohc=pTOrC1zKXpsAX-dMaN0&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT8ftXSM2RiCuyRVgLv0OX1JWrFI3jqcLpONx8svLm27kA&oe=61BE5314&_nc_sid=21929d', 'config_width': 750, 'config_height': 1334}, {'src': 'https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e35/268430240_648286416303865_1516137624972219047_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=101&_nc_ohc=pTOrC1zKXpsAX-dMaN0&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT8ftXSM2RiCuyRVgLv0OX1JWrFI3jqcLpONx8svLm27kA&oe=61BE5314&_nc_sid=21929d', 'config_width': 1080, 'config_height': 1920}], 'display_url': 'https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e35/268430240_648286416303865_1516137624972219047_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=101&_nc_ohc=pTOrC1zKXpsAX-dMaN0&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT8ftXSM2RiCuyRVgLv0OX1JWrFI3jqcLpONx8svLm27kA&oe=61BE5314&_nc_sid=21929d', 'media_preview': 'ABgq1aKKKACiiigAooooAKKKKACiiigAooooA//Z', 'gating_info': None, 'fact_check_overall_rating': None, 'fact_check_information': None, 'sharing_friction_info': {'should_have_sharing_friction': False, 'bloks_app_url': None}, 'media_overlay_info': None, 'sensitivity_friction_info': None, 'taken_at_timestamp': 1639651405, 'expiring_at_timestamp': 1639737805, 'story_cta_url': None, 'story_view_count': None, 'is_video': False, 'owner': {'id': '255391219', 'profile_pic_url': 'https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-19/s150x150/69239464_2715622995147419_7869939009076592640_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=111&_nc_ohc=a9xERC0RLVoAX81oZty&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT86OB_d0-AzZQ8hEYoPkAVfF12zbZdgxk7HCSD2OLikQA&oe=61C251BA&_nc_sid=21929d', 'username': 'hpfpv', 'followed_by_viewer': False, 'requested_by_viewer': False}, 'tracking_token': 'eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiZmQ3NGI2ZTFlZTM1NDE2M2E2YTIzNzM5N2IzOTJmM2YyNzI5OTE2MzMzMDQ1MzI4Mjk5Iiwic2VydmVyX3Rva2VuIjoiMTYzOTY5OTMwMjU3N3wyNzI5OTE2MzMzMDQ1MzI4Mjk5fDUwNzU0MjIyNzA3fDhhZDQ2NzUwMzFlYTk5MDdjYmNlYTEyZWY5MDY1NWIxYjk3NmU0OTA1OTkxNzJmZTE5ZGEyYmQxOTM1ODUyNjkifSwic2lnbmF0dXJlIjoiIn0=', 'tappable_objects': [{'__typename': 'GraphTappableMention', 'x': 0.5, 'y': 0.42503748125937, 'width': 0.32007999999999903, 'height': 0.044977511244377, 'rotation': 0.0, 'custom_title': None, 'attribution': None, 'username': '229eaglemotion', 'full_name': '229eaglemotion', 'is_private': False}], 'story_app_attribution': None, 'edge_media_to_sponsor_user': {'edges': []}, 'muting_info': None}, 'instaloader': {'version': '4.8.2', 'node_type': 'StoryItem'}}]}

            stories_response = formated_response_json(stories)

            response = client.update_item(
                TableName=os.environ['EVENTS_TABLE'],
                Key={
                    'requestId': {
                        'S': requestId,
                    }
                },
                UpdateExpression="SET stories = :b",
                ExpressionAttributeValues={':b': {'S': stories_response}}
            )
            response = {}
            response["Update"] = "Success"
            return json.dumps(response)
            # return {
            #     'statusCode': 200,
            #     'headers': {
            #         'Access-Control-Allow-Origin': 'https://instastories.houessou.com',
            #         'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            #         'Access-Control-Allow-Methods': 'GET',
            #         'Content-Type': 'application/json'
            #     },
            #     'body': json.dumps(response)
            # }

