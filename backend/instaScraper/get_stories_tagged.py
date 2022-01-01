from instaScraper.modules.instance import get_instance
from instaScraper.modules.stories import get_followers_stories, check_for_new_stories, story_time_str
from instaScraper.modules.download import profile_picture, story_media

import json
from datetime import datetime
import logging

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
    if new_stories["status"] == True:
        log["message"] = "New stories found"
        print(json.dumps(log))
        logger.info(json.dumps(log))
        for x in [current_date_time, "latest"]:
            file = dir + x + ".json"
            f = open(file, "w")
            f.write(json.dumps(new_stories["body"]))
            f.close()

        return new_stories["body"]
    else:
        log["message"] = "No new stories"
        print(json.dumps(log))
        logger.info(json.dumps(log))

def lambda_handler(event, context):
    logger.info(event)
    account_to_mention = str(event['pathParameters']['account_to_mention'])
    logger.info("Account to mention", account_to_mention)
    stories = get_followers_stories_if_mentionned(account_to_mention)
    response = []

    if(stories):
        logger.info(stories)
        for story in stories:
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
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'https://instastories.houessou.com',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(response)
    }

