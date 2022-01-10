
from instaScraper.modules.stories import get_followers_stories, check_for_new_stories, story_time_str
from instaScraper.modules.download import profile_picture, story_media
from instaloader import exceptions as Exceptions

import os
import requests
import boto3
import json
from datetime import datetime
import logging
import sys

client = boto3.client('dynamodb', region_name='us-east-1')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# def get_followers_stories_if_mentionned(account_to_mention):
#     """
#         Stores story items data if featured account is mentionned

#     """

#     webbucket = os.environ['WEB_BUCKET']
#     bucketurl = f'https://{webbucket}.s3.amazonaws.com/'
#     s3 = boto3.client('s3')

#     log = {}
#     log["function"] = "get_followers_stories_if_mentionned"
    
#     # Get stories of followers
#     gotStories = False
#     maxretries = 0
#     while gotStories == False:
#     # Create Instaloader Instance
#         try:
            
#             stories = get_followers_stories(account_to_mention)
#         except (Exceptions.ConnectionException, Exceptions.BadCredentialsException, Exceptions.InvalidArgumentException) as err:
#             maxretries +=1
#             message = {
#                     "function": "get_followers_stories_if_mentionned/get_stories",
#                     "error": str(err),
#                 }
#             logger.info(json.dumps(message))
#             if maxretries == 2: 
#                 logger.info("maximum attemps. stoping request now")
#                 sys.exit(1)
#         else:
#             gotStories = True
#             logger.info(json.dumps("Followers stories ok"))
    

#     current_date_time = datetime.now().strftime("%d-%m-%Y-%H:%M:%S")

#     # Check for newest stories and save them when mentionned
#     dir = "data/logs/" + account_to_mention + "/all"
#     new_stories = check_for_new_stories(stories, account_to_mention)
#     response = []
#     if new_stories["status"] == True:
#         log["message"] = "New stories found"
#         logger.info(json.dumps(log))
#         filekey = f"{dir}/{current_date_time}.json"
#         file = f"{current_date_time}.json"
#         s3.put_object(
#             Body=str(json.dumps(new_stories["body"])),
#             Bucket=webbucket,
#             Key=filekey,
#         )
#         # open(file, "w").write(json.dumps(new_stories["body"]))
#         # data = {'key': filekey}
#         # files = {'file': open(file, 'rb')}
#         # s3file = requests.post(bucketurl, data, files)
#         # os.remove(file)
#         response = new_stories["body"]
#         return {
#                 "status": True, 
#                 "body": response
#             }
#     else:
#         log["message"] = "No new stories"
#         logger.info(json.dumps(log))
#         return {
#                 "status": False, 
#                 "body": response
#             }

# def formated_response_json(stories):
#     response = []
#     if(stories["status"] == True):
#         for story in stories["body"]:
#             story_owner = story["node"]["owner"]["username"]
#             story_id = story["node"]["id"]
#             story_owner_profile_pic_url = story["node"]["owner"]["profile_pic_url"]
#             story_is_video = story["node"]["is_video"]
#             taken_at_timestamp = story["node"]["taken_at_timestamp"]
#             time = story_time_str(taken_at_timestamp)
#             if story_is_video:
#                 story_video_url = story["node"]["video_resources"][0]["src"]
#                 story_media_url = story_video_url
#                 story_display_url = story["node"]["display_url"]
#                 story_duration = story["node"]["video_duration"] * 1000
#             else:
#                 story_video_url = ""
#                 story_display_url = story["node"]["display_url"]
#                 story_media_url = story_display_url
#                 story_duration = 5000

#             profile_picture(story_owner_profile_pic_url, story_owner)
#             story_media(story_video_url, story_display_url, story_is_video, story_id)

#             data = {
#                 'story_id': story_id,
#                 'story_time': time,
#                 'user': story_owner,
#                 'is_video': story_is_video,
#                 "story_media_url": story_media_url,
#                 'media': story_id,
#                 'time': story_duration
#             }
#             response.append(data)
#         logger.info(response)
#     return json.dumps(response)

def lambda_handler(event, context):
    logger.info(event)
    for record in event ['Records']:
        if record['eventName'] == 'INSERT':
            requestId = record['dynamodb']['NewImage']['requestId']['S']
            account_to_mention = record['dynamodb']['NewImage']['account']['S']

        # try:
            storiesJson = check_for_new_stories(account_to_mention)
        # except Exception as e:
        #     logger.info(e)
        #     response = client.update_item(
        #         TableName=os.environ['EVENTS_TABLE'],
        #         Key={
        #             'requestId': {
        #                 'S': requestId,
        #             }
        #         },
        #         UpdateExpression="SET request_state = :s",
        #         ExpressionAttributeValues={
        #             ':s': {'S': "error"}
        #         }
        #     )
        #     response = {}
        #     response["Update"] = "Success"
        # else:
            response = client.update_item(
                TableName=os.environ['EVENTS_TABLE'],
                Key={
                    'requestId': {
                        'S': requestId,
                    }
                },
                UpdateExpression="SET stories = :s, request_state = :c",
                ExpressionAttributeValues={
                    ':s': {'S': json.dumps(storiesJson)},
                    ':c': {'S': "completed"}
                }
            )
            response = {}
            response["Update"] = "Success"
        return response
            

