import instaloader
from instaloader import exceptions as Exceptions
import functools 
from datetime import datetime, timedelta
import json
import random
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def cache(seconds: int, maxsize: int = 128, typed: bool = False):
    def wrapper_cache(func):
        func = functools.lru_cache(maxsize=maxsize, typed=typed)(func)
        func.delta = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.delta

        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.delta

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
# Search and return active scraper randomly
def get_scraper():
    with open(f"instaScraper/assets/scrapers.json") as f:
        data = f.read()
    scrapers = json.loads(data)
    active = False
    while active == False:
        random_scraper= random.choice(scrapers)
        if random_scraper["status"] == "active":
            active = True
            username = random_scraper["username"] 
            password = random_scraper["password"]

    scraper = {
        "username": username,
        "password": password,
    }
    return scraper
    
# Instaloader Instances initiation
@cache(seconds=3600, maxsize=1)
def get_instance():
    """
        Creates Instaloader instance with a random scraper from the scraper List
        Returns instance
    """
    success = False
    while success == False:
        scraper = get_scraper()
        username = str(scraper['username'])
        password = str(scraper['password'])
        try:
            random_instance = instaloader.Instaloader()
            random_instance.login(user=username, passwd=password)
        except (Exceptions.ConnectionException, Exceptions.BadCredentialsException, Exceptions.InvalidArgumentException) as err:
            message = {
                "function": "get_instance",
                "error": str(err),
                "details": f"scraper: {username}"
            }
            print (json.dumps(message))
            logger.info(json.dumps(message))
        else:
            success = True
            message = {
                "function": "get_instance",
                "status": "instance is successfully created",
                "details": f"scraper: {username}"
            }
            print (json.dumps(message))
            logger.info(json.dumps(message))

    return random_instance