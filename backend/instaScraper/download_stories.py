"""
    Download stories of specified instagram accounts

"""
import instaloader
from instaloader import exceptions as Exceptions
from instaScraper.modules.instance import get_instance
import os
import sys
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
def download_stories(accounts):
    """
        Download stories from instagram profiles specified in accounts
    """

    os.chdir("insta-scraper/stories")
    instance = get_instance()

    userIDs = []

    for account in accounts:
        profile = instaloader.Profile.from_username(instance.context, username=account)
        print (profile.userid)
        userIDs.append(profile.userid)

    logger.info(userIDs)
    try:
        instance.download_stories(userids=userIDs)
    except (Exceptions.ProfileNotExistsException, Exceptions.PrivateProfileNotFollowedException) as err:
        message = {
                "function": "download_stories",
                "error": str(err)
            }
        logger.info(json.dumps(message))
        print (json.dumps(message))
        sys.exit(1)

def handler():
    accounts = ["229eaglemotion"]
    download_stories(accounts)

if __name__ == "__main__":
    handler()