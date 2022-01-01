from instapy_cli import client

import logging
import json
import sys
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)



def connect(user, passwd):
    
    log = {}
    log["function"] = "post_to_story_connect"
    log["message"] = "client api initialization"
    print(log)
    logger.info(log)
    # try:
    api = client(user, passwd)
    # except (ClientError, ClientConnectionError) as err:
    #     log["message"] = str(err)
    #     logger.info(json.dumps(log))
    #     print (json.dumps(log))
    #     # sys.exit(1)
    
    return api

def post_story(username, password, story_id, is_video):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    log = {}
    log["function"] = "post_to_story"
    dir = 'web/static/media'
    video_file = f"{dir}/{story_id}.mp4"
    display_file = f"{dir}/{story_id}.jpg"
    cookie_path = f"instaScraper/assets/cookies/{username}_ig.json"
    cookie = None
    if os.path.exists(cookie_path):
        cookie = json.dumps(json.load(open(cookie_path)))
        
    if is_video :
        if cookie != None :
            with client(username, password, cookie=cookie) as cli:
                cli.upload(video_file, story=True)
        else:
            with client(username, password, cookie_file=cookie_path, write_cookie_file=True) as cli:
                cli.upload(video_file, story=True)
    else:
        if cookie != None:
            with client(username, password, cookie=cookie) as cli:
                cli.upload(display_file, story=True)
        else:
            with client(username, password, cookie_file=cookie_path, write_cookie_file=True) as cli:
                cli.upload(display_file, story=True)

post_story("229eaglemotion", "229motioneagle", "2733058097780584357", False)
# print(os.getcwd())