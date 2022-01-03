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
    dir = 'profile/'
    filekey = f"{dir}/{filename}.jpg"
    file = f"{filename}.jpg"
    try:
        s3.get_object(Bucket=webbucket, Key=filekey)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            localfile = requests.get(url, allow_redirects=True)
            open(file, 'wb').write(localfile.content)
            data = {'key': filekey}
            files = {'file': open(file, 'rb')}
            s3file = requests.post(bucketurl, data, files)
            os.remove(file)
    logger.info('End download profile')

# @lru_cache(maxsize=128)
def story_media(video, display, is_video, filename):
    logger.info('Start download media')
    dir = 'media/'
    video_filekey = f"{dir}/{filename}.mp4"
    display_filekey = f"{dir}/{filename}.jpg"
    video_file = f"{filename}.mp4"
    display_file = f"{filename}.jpg"

    if is_video:
        try:
            s3.get_object(Bucket=webbucket, Key=video_filekey)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
            # The object does not exist.
                r = requests.get(video, allow_redirects=True)
                open(video_filekey, 'wb').write(r.content)
                data = {'key': video_filekey}
                files = {'file': open(video_file, 'rb')}
                s3file = requests.post(bucketurl, data, files)
                os.remove(video_file)
                
                r2 = requests.get(display, allow_redirects=True)
                open(display_filekey, 'wb').write(r2.content)
                data2 = {'key': video_filekey}
                files2 = {'file': open(video_file, 'rb')}
                s3file2 = requests.post(bucketurl, data2, files2)
                os.remove(display_file)
    else:
        try:
            s3.get_object(Bucket=webbucket, Key=video_filekey)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
            # The object does not exist.
                r3 = requests.get(display, allow_redirects=True)
                open(display_filekey, 'wb').write(r3.content)
                data3 = {'key': video_filekey}
                files3 = {'file': open(video_file, 'rb')}
                s3file3 = requests.post(bucketurl, data3, files3)
                os.remove(display_file)
    logger.info('End download media')
            
