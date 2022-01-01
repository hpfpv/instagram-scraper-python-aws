import requests
import urllib.request
import os
from functools import lru_cache
from pymediainfo import MediaInfo

# @lru_cache(maxsize=128)
def profile_picture(url, filename):
    dir = 'web/static/profile'
    name = f"{dir}/{filename}.jpg"
    if os.path.exists(name) == False:
        p = requests.get(url, allow_redirects=True)
        open(name, 'wb').write(p.content)
        

# @lru_cache(maxsize=128)
def story_media(video, display, is_video, filename):
    
    dir = 'web/static/media'
    video_file = f"{dir}/{filename}.mp4"
    display_file = f"{dir}/{filename}.jpg"

    if is_video:
        if os.path.exists(video_file) == False:
            r = requests.get(video, allow_redirects=True)
            open(video_file, 'wb').write(r.content)
                
        if os.path.exists(display_file) == False:
            r2 = requests.get(display, allow_redirects=True)
            open(display_file, 'wb').write(r2.content)

        # story_duration = MediaInfo.parse(video_file).tracks[0].duration
    else:
        if os.path.exists(display_file) == False:
            r3 = requests.get(display, allow_redirects=True)
            open(display_file, 'wb').write(r3.content)
            
        # story_duration = 5000
    
    # return story_duration
