import instaloader
from instaloader import exceptions as Exceptions
from instaloader import structures
from instaScraper.modules.instance import cache

from instagram_private_api import Client, ClientCompatPatch
from instagram_private_api.errors import (
    ErrorHandler, ClientError,
    ClientLoginRequiredError, ClientCookieExpiredError,
    ClientConnectionError
)
import logging
import json
import sys
from urllib.parse import urlparse as compat_urllib_parse_urlparse
from urllib.request import urlopen
import urllib.request as compat_urllib_request
from io import BytesIO

import os
import json
from collections import defaultdict
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

@cache(seconds=300)
def get_followers(instance, account_to_mention):
    """
        Returns a List of userIds of specified account followers
        Uses its own Instaloader instance since account needs to be logged in to retrieve followers
        Take an instance and the account as parameters
    """

    log = {}
    log["function"] = "get_followers"
    log["message"] = "retrieving followers"

    print(log)
    logger.info(log)
    try:
        profile = instaloader.Profile.from_username(instance.context, username=account_to_mention)
        followers_iterator = profile.get_followers()
    except (Exceptions.ProfileNotExistsException) as err:
        log["message"] = str(err)
        logger.info(json.dumps(log))
        print (json.dumps(log))
        sys.exit(1)

    userIds = []
    for account in followers_iterator:
        userIds.append(account.userid)

    log["message"] = "followers ok"

    print(log)
    logger.info(log)

    return userIds
    
# @cache(seconds=600)
def get_followers_stories(instance, account_to_mention):
    """
        Return stories of speficies userIds
        Stories as Instaloader Structure
    """
    log = {}
    log["function"] = "get_followers_stories"
    log["message"] = f"retriving account {account_to_mention} followers' stories"
    print(json.dumps(log))
    logger.info(json.dumps(log))

    userIds = get_followers(instance, account_to_mention)

    try:
        stories = instance.get_stories(userids=userIds)
    except (Exceptions.ProfileNotExistsException) as err:
        log["message"] = str(err)
        logger.info(json.dumps(log))
        print (json.dumps(log))
        sys.exit(1)
    
    return stories


def check_for_new_stories(stories, account_to_mention):
    """
        Returns True if new stories are found
        Also retruns dict of new stories items
    """

    log = {}
    log["function"] = "check_for_new_stories"
    log["message"] = f"checking for new stories"
    print(json.dumps(log))
    logger.info(json.dumps(log))

    dir = "instaScraper/tagged-stories/"
    result = 0
    response = []
    for story in stories:
        try:
            for storyItem in story.get_items():
                storyItemJson  = structures.get_json_structure(storyItem)
                owner = str(storyItemJson["node"]["owner"]["username"])
                id = str(storyItemJson["node"]["id"])
                for x in storyItemJson["node"]["tappable_objects"]:
                    if x["__typename"] == "GraphTappableMention":
                        if x["username"] == account_to_mention:
                            file = dir + ".temp/" + owner + "-" + id + ".json"
                            if os.path.exists(file) == False:
                                result += 1
                                f = open(file, "w")
                                f.write(json.dumps(storyItemJson))
                                f.close()
                                response.append(storyItemJson)
                            else:
                                # print(f"Story Item {id} from username {owner} has already been processed")
                                logger.info(f"Story Item {id} from username {owner} has already been processed")
                        else:
                            # print(f"Story Item {id} not mentionning {account_to_mention}")
                            logger.info(f"Story Item {id} not mentionning {account_to_mention}")
                    else:
                        # print(f"Story Item {id} has no mentions")
                        logger.info(f"Story Item {id} has no mentions")
        except (Exceptions.LoginRequiredException, Exceptions.PrivateProfileNotFollowedException) as err:
            log["message"] = str(err)
            logger.info(json.dumps(log))
            print (json.dumps(log))
            sys.exit(1)
    if result > 0:
        return {
                "status": True, 
                "body": response
            }
    else:
        return {
                "status": False, 
                "body": response
            }


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
        # if hour > 0:
        #     if hour == 1:
        #         response += f", {hour} hour"
        #     else:
        #         response += f", {hour} hours"
        # if minutes > 0:
        #     response += f", {minutes} min"
    else:
        if hour > 0:
            response += f"{hour}h"
            # if minutes > 0:
            #     response += f", {minutes} min"
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
