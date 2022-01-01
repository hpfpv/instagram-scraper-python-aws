from flask import Flask, jsonify, request, render_template
import json
import time as timeos
import logging
from instaScraper import get_stories_tagged, download_stories
from instaScraper.modules.download import profile_picture, story_media

from instaScraper.modules.stories import story_time_str, connect, post_story

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__, 
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
# CORS(app)

@app.route("/", methods=["GET", "POST"])
def init():
    return render_template('init.html')

def stories_response(account_to_mention):
   logger.info("Account to mention", account_to_mention)
   stories = get_stories_tagged.get_followers_stories_if_mentionned(account_to_mention)
   
   if(stories):
      logger.info(stories)
      response = []
      for story in stories:
         story_owner = story["node"]["owner"]["username"]
         story_id = story["node"]["id"]
         story_owner_profile_pic_url = story["node"]["owner"]["profile_pic_url"]
         story_is_video = story["node"]["is_video"]
         taken_at_timestamp = story["node"]["taken_at_timestamp"]
         time = story_time_str(taken_at_timestamp)
         if story_is_video:
               story_video_url = story["node"]["video_resources"][0]["src"]
               story_media_url = story_video_url
               story_display_url = story["node"]["display_url"]
               story_duration = story["node"]["video_duration"] * 1000
         else:
               story_video_url = ""
               story_display_url = story["node"]["display_url"]
               story_media_url = story_display_url
               story_duration = 5000

         profile_picture(story_owner_profile_pic_url, story_owner)
         story_media(story_video_url, story_display_url, story_is_video, story_id)

         data = {
               'story_id': story_id,
               'story_time': time,
               'user': story_owner,
               # "story_owner_profile_pic_url": story_owner_profile_pic_url,
               # 'path_to_profile_pic': path_to_profile_pic,
               'is_video': story_is_video,
               "story_media_url": story_media_url,
               'media': story_id,
               'time': story_duration
         }

         response.append(data)
      print(response)
      logger.info(response)
      return response
        
@app.route("/start", methods=['GET', 'POST'])
def start():
    if request.method == "POST":
        account_to_mention = request.form["account_to_mention"]
        response = stories_response(account_to_mention)
        if response :
            return render_template('index.html', stories=response)
        else:
            return render_template('nothing.html')
    else:
        return render_template('init.html')

    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)