import instaloader
from instaloader import exceptions as Exceptions
from instaloader import structures

from instaScraper.modules.download import profile_picture, story_media
from instaScraper.modules.instance import cache, get_instance

from instagram_private_api import Client, ClientCompatPatch
from instagram_private_api.errors import (
    ErrorHandler, ClientError,
    ClientLoginRequiredError, ClientCookieExpiredError,
    ClientConnectionError
)
from datetime import datetime, timedelta, timezone

import logging
import json
import sys
from urllib.parse import urlparse as compat_urllib_parse_urlparse
from urllib.request import urlopen
import urllib.request as compat_urllib_request

import requests
import boto3
import botocore
import os
import json

import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@cache(seconds=300)
def get_followers(account_to_mention):
    """
        Returns a List of userIds of specified account followers
        Uses its own Instaloader instance since account needs to be logged in to retrieve followers
        Take an instance and the account as parameters
    """

    log = {}
    log["function"] = "get_followers"
    log["message"] = "retrieving followers"

    logger.info(log)
    maxretries = 0
    gotFollowers = False
    while gotFollowers == False:
        try:
            instance = get_instance()
            profile = instaloader.Profile.from_username(instance.context, username=account_to_mention)
            followers_iterator = profile.get_followers()
        except (Exceptions.ProfileNotExistsException) as err:
            log["message"] = str(err)
            logger.info(json.dumps(log))
            sys.exit(1)
        except (Exceptions.ConnectionException, Exceptions.BadCredentialsException, Exceptions.InvalidArgumentException) as err:
            maxretries +=1
            message = {
                    "function": "get_followers",
                    "error": str(err),
                }
            logger.info(json.dumps(message))
            if maxretries == 2: 
                logger.info("maximum attemps. stopping request now")
                sys.exit(1)
        else:
            gotFollowers = True
            logger.info(json.dumps("Followers ok"))

    userIds = []
    for account in followers_iterator:
        userIds.append(account.userid)

    return userIds
    
# @cache(seconds=600)
def get_followers_stories(account_to_mention):
    """
        Return stories of speficies userIds
        Stories as Instaloader Structure
    """
    log = {}
    log["function"] = "get_followers_stories"
    log["message"] = f"retriving account {account_to_mention} followers' stories"
    logger.info(json.dumps(log))
    userIds = get_followers(account_to_mention)
    maxretries = 0
    gotStories = False
    while gotStories == False:
        try:
            instance = get_instance()
            stories = instance.get_stories(userids=userIds)
        except (Exceptions.ProfileNotExistsException) as err:
            log["message"] = str(err)
            logger.info(json.dumps(log))
            sys.exit(1)
        except (Exceptions.ConnectionException, Exceptions.BadCredentialsException, Exceptions.InvalidArgumentException) as err:
            maxretries +=1
            message = {
                    "function": "get_followers_stories",
                    "error": str(err),
                }
            logger.info(json.dumps(message))
            if maxretries == 2: 
                logger.info("maximum attemps. stopping request now")
                sys.exit(1)
        else:
            gotStories = True
            logger.info(json.dumps("Followers stories ok"))

    return stories


def check_for_new_stories(account_to_mention):
    """
        Returns True if new stories are found
        Also retruns dict of new stories items
    """

    log = {}
    log["function"] = "check_for_new_stories"
    log["message"] = f"checking for new stories"
    logger.info(json.dumps(log))

    webbucket = os.environ['WEB_BUCKET']
    bucketurl = f'https://{webbucket}.s3.amazonaws.com/'
    s3 = boto3.client('s3')

    stories = get_followers_stories(account_to_mention)

    dir_history = "data/logs/" + account_to_mention + "/history"
    dir_all = "data/logs/" + account_to_mention + "/all"
    response = []
    fullStoryJson = []
    last_scrapped_s3_key = f"{dir_all}/last_scrap_time.txt"

    try:
        s3.head_object(Bucket=webbucket, Key=last_scrapped_s3_key)
    except botocore.exceptions.ClientError as e:
        if int(e.response['Error']['Code']) == 404:
            # The object does not exist.
            last_scraped = datetime.utcnow() - timedelta(days=1)
        else:
            logger.info("error accessing the s3 bucket. check bucket policy")
            logger.info(e.response['Error'])
    else:
        last_scraped = datetime.strptime(s3.get_object(Bucket=webbucket, Key=last_scrapped_s3_key)["Body"], "%Y-%m-%d-%H:%M:%S")

    for story in stories:
        # getting latest scrap time
        # story_last_item_utc = story.latest_media_utc()
        story_last_item_utc = datetime.utcfromtimestamp(story._node['latest_reel_media'])
        # cheking is story is newer than latest scrap time
        if last_scraped < story_last_item_utc:
            for storyItem in story.get_items():
                storyItemJson  = structures.get_json_structure(storyItem)
                if last_scraped < datetime.utcfromtimestamp(storyItemJson["node"]["taken_at_timestamp"]):
                    for x in storyItemJson["node"]["tappable_objects"]:
                        if x["__typename"] == "GraphTappableMention":
                            if x["username"] == account_to_mention:
                                logger.info(f"New stories Found where {account_to_mention} is mentionned")
                                fullStoryJson.append(storyItemJson)
                                story_owner = storyItemJson["node"]["owner"]["username"]
                                story_id = storyItemJson["node"]["id"]
                                story_owner_profile_pic_url = storyItemJson["node"]["owner"]["profile_pic_url"]
                                story_is_video = storyItemJson["node"]["is_video"]
                                taken_at_timestamp = storyItemJson["node"]["taken_at_timestamp"]
                                time = story_time_str(taken_at_timestamp)

                                if story_is_video:
                                    story_video_url = storyItemJson["node"]["video_resources"][0]["src"]
                                    story_media_url = story_video_url
                                    story_display_url = storyItemJson["node"]["display_url"]
                                    story_duration = storyItemJson["node"]["video_duration"] * 1000
                                else:
                                    story_video_url = ""
                                    story_display_url = storyItemJson["node"]["display_url"]
                                    story_media_url = story_display_url
                                    story_duration = 5000

                                profile_picture(story_owner_profile_pic_url, story_owner)
                                story_media(story_video_url, story_display_url, story_is_video, story_id)

                                data = {
                                    'story_id': story_id,
                                    'story_time': time,
                                    'user': story_owner,
                                    'is_video': story_is_video,
                                    "story_media_url": story_media_url,
                                    'media': story_id,
                                    'time': story_duration
                                }
                                response.append(data)

                                # saving storyItemJson to S3 for logs
                                filekey_history = f"{dir_history}/{story_owner}/{story_id}.json"
                                try:
                                    s3.head_object(Bucket=webbucket, Key=filekey_history)
                                except botocore.exceptions.ClientError as e:
                                    if int(e.response['Error']['Code']) == 404:
                                        # The object does not exist.
                                        s3.put_object(
                                            Body=str(json.dumps(storyItemJson)),
                                            Bucket=webbucket,
                                            Key=filekey_history,
                                        )
                                    else:
                                        logger.info("error accessing the s3 bucket. check bucket policy")
                                        logger.info(e.response['Error'])
                            else:
                                # logger.info(f"Story Item {id} not mentionning {account_to_mention}")
                                pass
                        else:
                            # logger.info(f"Story Item {id} has no mentions")
                            pass

    # saving storiesJson scraped now for logs
    current_date_time = datetime.utcnow().strftime("%Y-%m-%d-%H:%M:%S")
    if response != []:
        filekey_all = f"{dir_all}/{current_date_time}.json"
        s3.put_object(
            Body=fullStoryJson,
            Bucket=webbucket,
            Key=filekey_all,
        )
    
    # updating latest scrap time
    s3.put_object(
        Body=current_date_time,
        Bucket=webbucket,
        Key=last_scrapped_s3_key,
    )

    logger.info("new_stories")
    logger.info(response)
    return response

def story_time_str(story_time_taken):
    import time
    import datetime 

    response = ""
    story_time = datetime.datetime.fromtimestamp(story_time_taken)
    ct = datetime.datetime.now()

    timeago = (ct - story_time).total_seconds()
    day = int(timeago / (24 * 3600))
    hour = int(((timeago / (24 * 3600) - day) * 24))
    minutes = int((((timeago / (24 * 3600) - day) * 24) - hour) * 60)
    if day > 0 :
        response += f"{day}d"
    else:
        if hour > 0:
            response += f"{hour}h"
        else:
            response += f"{minutes}m"

    return response



def strip_url_params(thumbnail_url):
        o = compat_urllib_parse_urlparse(thumbnail_url)
        return '{scheme}://{host}{path}'.format(
            scheme=o.scheme,
            host=o.netloc,
            path=o.path
        )


def connect(user, passwd):
    log = {}
    log["function"] = "post_to_story_connect"
    log["message"] = "client api initialization"
    print(log)
    logger.info(log)
    try:
        api = Client(user, passwd)
    except (ClientError, ClientConnectionError) as err:
        log["message"] = str(err)
        logger.info(json.dumps(log))
        print (json.dumps(log))
        sys.exit(1)
    
    return api

def post_story(story_id, media_url, is_video, client):
    log = {}
    log["function"] = "post_to_story"

    if is_video :
        video_info_res = urlopen(media_url)
        video_info = json.loads(video_info_res.read().decode('utf8'))
        mp4_info = video_info['files']['mp4']

        video_url = ('https:' if mp4_info['url'].startswith('//') else '') + mp4_info['url']
        video_size = (mp4_info['width'], mp4_info['height'])
        thumbnail_url = ('https:' if video_info['thumbnail_url'].startswith('//') else '') + video_info['thumbnail_url']
        # remove height param
        thumbnail_url = strip_url_params(thumbnail_url)
        duration = mp4_info['duration']

        # requires UA
        video_req = compat_urllib_request.Request(
            video_url, headers={'user-agent': 'Mozilla/5.0'})
        video_res = urlopen(video_req)
        video_data = video_res.read()
        thumb_res = urlopen(thumbnail_url)
        thumb_data = thumb_res.read()
        results = client.post_video_story(video_data, video_size, duration, thumb_data)
         
        if results.get('status') == 'ok':
            log["message"] = f"{story_id} reposted successfully"
        else:
            log["message"] = f"{story_id} could not be reposted"

    else:
        res = urlopen(media_url)
        photo_data = res.read()
        size = (1080, 1920)
        results = client.post_photo_story(photo_data, size)

        if results.get('status') == 'ok':
            log["message"] = f"{story_id} reposted successfully"
        else:
            log["message"] = f"{story_id} could not be reposted"
    
    print(log)
    logger.info(log)
