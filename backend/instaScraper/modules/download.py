import requests
import urllib.request
import os
import json
from functools import lru_cache
from pymediainfo import MediaInfo
import logging
import boto3
import botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

webbucket = os.environ['WEB_BUCKET']
s3 = boto3.client('s3')
bucketurl = f'https://{webbucket}.s3.amazonaws.com/'

# @lru_cache(maxsize=128)
def profile_picture(requestId, url, filename):

    log = {}
    log["function"] = "profile_picture"
    log["requestId"] = requestId

    dir = 'data/profile'
    filekey = f"{dir}/{filename}.jpg"
    file = f"{filename}.jpg"

    try:
        s3.head_object(Bucket=webbucket, Key=filekey)
    except botocore.exceptions.ClientError as e:
        if int(e.response['Error']['Code']) == 404:
            # The object does not exist.
            log["status"] = "Downloading profile picture"
            logger.info(json.dumps(log))
            profile_response = requests.get(url, stream=True).raw
            try: 
                s3.upload_fileobj(profile_response, webbucket, filekey)
                log["status"] = "completed"
                logger.info(json.dumps(log))
            except botocore.exceptions.ClientError as e:
                log["status"] = f"error: {e.response['Error']}"
                logger.info(json.dumps(log))
    else:
        log["status"] = "completed"
        logger.info(json.dumps(log))

# @lru_cache(maxsize=128)
def story_media(requestId, video, display, is_video, filename):

    log = {}
    log["function"] = "story_media"
    log["requestId"] = requestId

    dir = 'data/media'
    video_filekey = f"{dir}/{filename}.mp4"
    display_filekey = f"{dir}/{filename}.jpg"
    video_file = f"{filename}.mp4"
    display_file = f"{filename}.jpg"

    if is_video:
        try:
            s3.head_object(Bucket=webbucket, Key=video_filekey)
        except botocore.exceptions.ClientError as e:
            if int(e.response['Error']['Code']) == 404:
            # The object does not exist.
                log["status"] = "Downloading story media"
                logger.info(json.dumps(log))
                video_response = requests.get(video, stream=True).raw
                try:
                    s3.upload_fileobj(video_response, webbucket, video_filekey)
                    log["status"] = "completed"
                    logger.info(json.dumps(log))
                except botocore.exceptions.ClientError as e:
                    log["status"] = f"error: {e.response['Error']}"
                    logger.info(json.dumps(log))
                
                display_response = requests.get(display, stream=True).raw
                try:
                    s3.upload_fileobj(display_response, webbucket, display_filekey)
                except botocore.exceptions.ClientError as e:
                    log["status"] = f"error: {e.response['Error']}"
                    logger.info(json.dumps(log))
        else:
            log["status"] = "completed"
            logger.info(json.dumps(log))
    else:
        try:
            s3.head_object(Bucket=webbucket, Key=display_filekey)
        except botocore.exceptions.ClientError as e:
            if int(e.response['Error']['Code']) == 404:
            # The object does not exist.
                log["status"] = "Downloading story media"
                logger.info(json.dumps(log))
                display_response = requests.get(display, stream=True).raw
                try:
                    s3.upload_fileobj(display_response, webbucket, display_filekey)
                    log["status"] = "completed"
                    logger.info(json.dumps(log))
                except botocore.exceptions.ClientError as e:
                    log["status"] = f"error: {e.response['Error']}"
                    logger.info(json.dumps(log))
        else:
            log["status"] = "completed"
            logger.info(json.dumps(log))
                    
            
