import requests
import urllib.request
import os
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
def profile_picture(url, filename):
    logger.info('Start download profile')
    dir = 'data/profile'
    filekey = f"{dir}/{filename}.jpg"
    file = f"{filename}.jpg"
    try:
        s3.head_object(Bucket=webbucket, Key=filekey)
    except botocore.exceptions.ClientError as e:
        if int(e.response['Error']['Code']) == 404:
            # The object does not exist.
            profile_response = requests.get(url, stream=True).raw
            try: 
                s3.upload_fileobj(profile_response, webbucket, filekey)
            except botocore.exceptions.ClientError as e:
                logger.info(e.response['Error'])
            # open(file, 'wb').write(localfile.content)
            # data = {'key': filekey}
            # files = {'file': localfile}
            # s3file = requests.post(bucketurl, data, files)
            # os.remove(file)
    logger.info('End download profile')

# @lru_cache(maxsize=128)
def story_media(video, display, is_video, filename):
    logger.info('Start download media')
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
                video_response = requests.get(video, stream=True).raw
                try:
                    s3.upload_fileobj(video_response, webbucket, video_filekey)
                except botocore.exceptions.ClientError as e:
                    logger.info(e.response['Error'])
                # open(video_filekey, 'wb').write(r.content)
                # data = {'key': video_filekey}
                # files = {'file': r}
                # s3file = requests.post(bucketurl, data, files)
                # os.remove(video_file)
                
                display_response = requests.get(display, stream=True).raw
                try:
                    s3.upload_fileobj(display_response, webbucket, display_filekey)
                except botocore.exceptions.ClientError as e:
                    logger.info(e.response['Error'])
                # open(display_filekey, 'wb').write(r2.content)
                # data2 = {'key': display_filekey}
                # files2 = {'file': r2}
                # s3file2 = requests.post(bucketurl, data2, files2)
                # os.remove(display_file)
    else:
        try:
            s3.head_object(Bucket=webbucket, Key=display_filekey)
        except botocore.exceptions.ClientError as e:
            if int(e.response['Error']['Code']) == 404:
            # The object does not exist.
                display_response = requests.get(display, stream=True).raw
                try:
                    s3.upload_fileobj(display_response, webbucket, display_filekey)
                except botocore.exceptions.ClientError as e:
                    logger.info(e.response['Error'])
                # open(display_filekey, 'wb').write(r3.content)
                # data3 = {'key': display_filekey}
                # files3 = {'file': r3}
                # s3file3 = requests.post(bucketurl, data3, files3)
                # os.remove(display_file)
    logger.info('End download media')
            
