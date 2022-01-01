from instaScraper.modules.instance import get_instance
from instaScraper.modules.stories import get_followers_stories, check_for_new_stories
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
            