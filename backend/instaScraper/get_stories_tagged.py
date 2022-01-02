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
            file = dir + x + ".json"
            f = open(file, "w")
            f.write(json.dumps(new_stories["body"]))
            f.close()
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
            stories = get_followers_stories_if_mentionned(account_to_mention)
            srories_response = formated_response_json(stories)

            response = client.update_item(
                TableName=os.environ['EVENTS_TABLE'],
                Key={
                    'requetsId': {
                        'S': requestId,
                    }
                },
                UpdateExpression="SET response = :b",
                ExpressionAttributeValues={':b': {'S': srories_response}}
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

