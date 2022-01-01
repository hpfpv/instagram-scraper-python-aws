from flask import Flask, jsonify, request, render_template
import json
import time as timeos
import logging
from collections import defaultdict
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
   
   # stories =[]
   # timeos.sleep(5)
   # stories = [{"node": {"audience": "MediaAudience.DEFAULT", "__typename": "GraphStoryImage", "id": "2733058097780584357", "dimensions": {"height": 1334, "width": 750}, "display_resources": [{"src": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/sh0.08/e35/p640x640/269680968_1552421765126936_3479985675304239098_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=108&_nc_ohc=d73g8cVjgPsAX_Brj4Y&tn=88XWGoZ_UZspQpVS&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT9rur3s-eBbPBHHN83n-Jsy1a_bMchzLMIDV_yJgzITBw&oe=61C36458&_nc_sid=21929d", "config_width": 640, "config_height": 1138}, {"src": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e35/269680968_1552421765126936_3479985675304239098_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=108&_nc_ohc=d73g8cVjgPsAX_Brj4Y&tn=88XWGoZ_UZspQpVS&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT890EPfyOD7t75NWb6P0JXAPMqxvNhopGXFzayhmAsdRg&oe=61C30290&_nc_sid=21929d", "config_width": 750, "config_height": 1334}, {"src": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e35/269680968_1552421765126936_3479985675304239098_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=108&_nc_ohc=d73g8cVjgPsAX_Brj4Y&tn=88XWGoZ_UZspQpVS&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT890EPfyOD7t75NWb6P0JXAPMqxvNhopGXFzayhmAsdRg&oe=61C30290&_nc_sid=21929d", "config_width": 1080, "config_height": 1920}], "display_url": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e35/269680968_1552421765126936_3479985675304239098_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=108&_nc_ohc=d73g8cVjgPsAX_Brj4Y&tn=88XWGoZ_UZspQpVS&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT890EPfyOD7t75NWb6P0JXAPMqxvNhopGXFzayhmAsdRg&oe=61C30290&_nc_sid=21929d", "media_preview": "ABgqqxjLAe9apFULdfnFaVSWyIrRUuKKBFK25f6CrxFU7Uck+gq4M0hsTNFPI44opkmVDcCLORnNTi+T0P6VmtTKRpY2ReIfX8qKyRRQKx//2Q==", "gating_info": None, "fact_check_overall_rating": None, "fact_check_information": None, "sharing_friction_info": {"should_have_sharing_friction": False, "bloks_app_url": None}, "media_overlay_info": None, "sensitivity_friction_info": None, "taken_at_timestamp": 1640025904, "expiring_at_timestamp": 1640112304, "story_cta_url": None, "story_view_count": None, "is_video": False, "owner": {"id": "255391219", "profile_pic_url": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-19/s150x150/69239464_2715622995147419_7869939009076592640_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=111&_nc_ohc=7UQ_2qERozgAX8QpUgI&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_1I5PPkXw7aDOIUPTfi-3E9dUpMkciq7OsRWnUxEq8aw&oe=61C8407A&_nc_sid=21929d", "username": "hpfpv", "followed_by_viewer": False, "requested_by_viewer": False}, "tracking_token": "eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiYTRjZTk0MTNhYTJjNDM2MmEzMDRmZjVmYjI1MWM0ZDgyNzMzMDU4MDk3NzgwNTg0MzU3Iiwic2VydmVyX3Rva2VuIjoiMTY0MDAyNjA0Nzk0MHwyNzMzMDU4MDk3NzgwNTg0MzU3fDUwNzU0MjIyNzA3fDI1MjgyMzZlM2VhYWJkMjEwMDk0ZDk4MTVlZTc5ZWUxNDNkYWY5ZjVjOGVkNjgwMDExMzk5MzM4MzNmNzA5MTYifSwic2lnbmF0dXJlIjoiIn0=", "tappable_objects": [{"__typename": "GraphTappableMention", "x": 0.5, "y": 0.27811094452773605, "width": 0.32007999999999903, "height": 0.044977511244377, "rotation": 0.0, "custom_title": None, "attribution": None, "username": "229eaglemotion", "full_name": "229eaglemotion", "is_private": False}], "story_app_attribution": None, "edge_media_to_sponsor_user": {"edges": []}, "muting_info": None}, "instaloader": {"version": "4.8.2", "node_type": "StoryItem"}}, {"node": {"audience": "MediaAudience.DEFAULT", "__typename": "GraphStoryVideo", "id": "2733057752393590553", "dimensions": {"height": 1137, "width": 640}, "display_resources": [{"src": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e15/269611524_454937669564566_8115489837683735162_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=110&_nc_ohc=EgQ9OokrjEQAX_yZAGo&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT9iPg4_S4ssmQq2k_bmdkg39-0PpEewU4LHm0nJOtgouA&oe=61C2FE42&_nc_sid=21929d", "config_width": 640, "config_height": 1137}, {"src": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e15/269611524_454937669564566_8115489837683735162_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=110&_nc_ohc=EgQ9OokrjEQAX_yZAGo&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT9iPg4_S4ssmQq2k_bmdkg39-0PpEewU4LHm0nJOtgouA&oe=61C2FE42&_nc_sid=21929d", "config_width": 750, "config_height": 1332}, {"src": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e15/269611524_454937669564566_8115489837683735162_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=110&_nc_ohc=EgQ9OokrjEQAX_yZAGo&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT9iPg4_S4ssmQq2k_bmdkg39-0PpEewU4LHm0nJOtgouA&oe=61C2FE42&_nc_sid=21929d", "config_width": 1080, "config_height": 1918}], "display_url": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e15/269611524_454937669564566_8115489837683735162_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=110&_nc_ohc=EgQ9OokrjEQAX_yZAGo&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT9iPg4_S4ssmQq2k_bmdkg39-0PpEewU4LHm0nJOtgouA&oe=61C2FE42&_nc_sid=21929d", "media_preview": "ABgqpYrasAFTPcnmsjFXLW4ERwwytaowqJyWnc6LIAz2orPku0AyFOPpRSSJlKXRL7mYNOBxyKpC5Pp+tO+1+361Nzosy75jHjr+A/woqot4FOQCCPpRRcVitgUbaiHapqyNtxNtFOopDP/Z", "gating_info": None, "fact_check_overall_rating": None, "fact_check_information": None, "sharing_friction_info": {"should_have_sharing_friction": False, "bloks_app_url": None}, "media_overlay_info": None, "sensitivity_friction_info": None, "taken_at_timestamp": 1640025891, "expiring_at_timestamp": 1640112291, "story_cta_url": None, "story_view_count": None, "is_video": True, "owner": {"id": "255391219", "profile_pic_url": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-19/s150x150/69239464_2715622995147419_7869939009076592640_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=111&_nc_ohc=7UQ_2qERozgAX8QpUgI&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_1I5PPkXw7aDOIUPTfi-3E9dUpMkciq7OsRWnUxEq8aw&oe=61C8407A&_nc_sid=21929d", "username": "hpfpv", "followed_by_viewer": False, "requested_by_viewer": False}, "tracking_token": "eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiYTRjZTk0MTNhYTJjNDM2MmEzMDRmZjVmYjI1MWM0ZDgyNzMzMDU3NzUyMzkzNTkwNTUzIiwic2VydmVyX3Rva2VuIjoiMTY0MDAyNjA0Nzk0MHwyNzMzMDU3NzUyMzkzNTkwNTUzfDUwNzU0MjIyNzA3fGUyMzBiODk5M2M5NTdiZTMwYzRkZjA4MDU1MDY5YjBlZTUwODAzYWU2ODEzOTk3ZTZkNmEyN2E4YWE1MWM4ODQifSwic2lnbmF0dXJlIjoiIn0=", "has_audio": False, "overlay_image_resources": None, "video_duration": 1.6, "video_resources": [{"src": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t50.12441-16/268374747_123368980165091_8137214773520849214_n.mp4?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=111&_nc_ohc=qtd2XT2KgtIAX-jXL-B&tn=88XWGoZ_UZspQpVS&edm=AHlfZHwBAAAA&ccb=7-4&oe=61C30D18&oh=00_AT8fj6I349EThC0MYIGOxtGgsGZ5W5rBMEReoYSrIPdtHg&_nc_sid=21929d", "config_width": 480, "config_height": 852, "mime_type": "video/mp4; codecs=\"avc1.42E01E\"", "profile": "BASELINE"}], "tappable_objects": [{"__typename": "GraphTappableMention", "x": 0.5415373626543291, "y": 0.5790711591129181, "width": 0.16703703982832202, "height": 0.023471976809253003, "rotation": 0.0, "custom_title": None, "attribution": None, "username": "229eaglemotion", "full_name": "229eaglemotion", "is_private": False}], "story_app_attribution": None, "edge_media_to_sponsor_user": {"edges": []}, "muting_info": None}, "instaloader": {"version": "4.8.2", "node_type": "StoryItem"}}, {"node": {"audience": "MediaAudience.DEFAULT", "__typename": "GraphStoryImage", "id": "2733057967580775508", "dimensions": {"height": 1920, "width": 1080}, "display_resources": [{"src": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/sh0.08/e35/p640x640/269652790_1569238470141919_687933118075426926_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=6souQfzUdnwAX8MLMhU&tn=88XWGoZ_UZspQpVS&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT8Gm6ZTmQLX-y_Gu7NtmUA0z4MQAL4BeeEKzY35zo5lqg&oe=61C2E155&_nc_sid=21929d", "config_width": 640, "config_height": 1137}, {"src": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/sh0.08/e35/p750x750/269652790_1569238470141919_687933118075426926_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=6souQfzUdnwAX8MLMhU&tn=88XWGoZ_UZspQpVS&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_sv_nYF64OO97YIA9PIXE-Orpno4qW2Jio0VSqFSlzeQ&oe=61C35C91&_nc_sid=21929d", "config_width": 750, "config_height": 1333}, {"src": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e35/p1080x1080/269652790_1569238470141919_687933118075426926_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=6souQfzUdnwAX8MLMhU&tn=88XWGoZ_UZspQpVS&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT8XMkvFfEDGel2WpoYHPH9dyywip5_SGyCJt4q2KksU4w&oe=61C33F12&_nc_sid=21929d", "config_width": 1080, "config_height": 1920}], "display_url": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e35/p1080x1080/269652790_1569238470141919_687933118075426926_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=6souQfzUdnwAX8MLMhU&tn=88XWGoZ_UZspQpVS&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT8XMkvFfEDGel2WpoYHPH9dyywip5_SGyCJt4q2KksU4w&oe=61C33F12&_nc_sid=21929d", "media_preview": "ABgqvpgKKCw/yKQHgfSm7qQxSwoppJ9KKYgD4A+goLVEWAx9BSqQaQxxPvRSgAUUxEDn/P8Ak0K3b/P86Y9R55/GgC2Cf84/xoqFScUUwP/Z", "gating_info": None, "fact_check_overall_rating": None, "fact_check_information": None, "sharing_friction_info": {"should_have_sharing_friction": False, "bloks_app_url": None}, "media_overlay_info": None, "sensitivity_friction_info": None, "taken_at_timestamp": 1640025908, "expiring_at_timestamp": 1640112308, "story_cta_url": None, "story_view_count": None, "is_video": False, "owner": {"id": "2235780635", "profile_pic_url": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-19/s150x150/187686436_825975598339132_6757154020984796263_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=104&_nc_ohc=Ph8B4An5-m8AX_cAatT&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT9UanqLwMkc-nYjC86Wkhj8VLMfIKjYUnR2WGX5W3y69Q&oe=61C733C6&_nc_sid=21929d", "username": "syh_doriane", "followed_by_viewer": False, "requested_by_viewer": False}, "tracking_token": "eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiNDg0NWJmNTAyZDYzNDZlNDhkZWVjZWFmNzcxMmQ5NWEyNzMzMDU3OTY3NTgwNzc1NTA4Iiwic2VydmVyX3Rva2VuIjoiMTY0MDAyNjA2MjkxMXwyNzMzMDU3OTY3NTgwNzc1NTA4fDUwNzU0MjIyNzA3fGM4ZWQzNjQzOTc2NTk5Mzc0YzIyYzI5OGQzY2Y0ZjU0Y2NmNGMxM2ExNTdhYWE5YjkxZTliMTQ5OTQzOWFmZWQifSwic2lnbmF0dXJlIjoiIn0=", "tappable_objects": [{"__typename": "GraphTappableMention", "x": 0.7801454352576901, "y": 0.060900085532439, "width": 0.077427736325631, "height": 0.010474101352083001, "rotation": -0.025544109578405003, "custom_title": None, "attribution": None, "username": "229eaglemotion", "full_name": "229eaglemotion", "is_private": False}], "story_app_attribution": None, "edge_media_to_sponsor_user": {"edges": []}, "muting_info": None}, "instaloader": {"version": "4.8.2", "node_type": "StoryItem"}}, {"node": {"audience": "MediaAudience.DEFAULT", "__typename": "GraphStoryVideo", "id": "2733057492783018770", "dimensions": {"height": 1137, "width": 640}, "display_resources": [{"src": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e15/269729988_1019106748947737_1226875975110361541_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=105&_nc_ohc=adKgiElGz1sAX8LvzcO&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_qIT3AWtf3LrNxV9uwQTfQeDZgrXmneX3ZmXw9Uvpcjw&oe=61C308A3&_nc_sid=21929d", "config_width": 640, "config_height": 1137}, {"src": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e15/269729988_1019106748947737_1226875975110361541_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=105&_nc_ohc=adKgiElGz1sAX8LvzcO&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_qIT3AWtf3LrNxV9uwQTfQeDZgrXmneX3ZmXw9Uvpcjw&oe=61C308A3&_nc_sid=21929d", "config_width": 750, "config_height": 1332}, {"src": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e15/269729988_1019106748947737_1226875975110361541_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=105&_nc_ohc=adKgiElGz1sAX8LvzcO&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_qIT3AWtf3LrNxV9uwQTfQeDZgrXmneX3ZmXw9Uvpcjw&oe=61C308A3&_nc_sid=21929d", "config_width": 1080, "config_height": 1918}], "display_url": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e15/269729988_1019106748947737_1226875975110361541_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=105&_nc_ohc=adKgiElGz1sAX8LvzcO&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_qIT3AWtf3LrNxV9uwQTfQeDZgrXmneX3ZmXw9Uvpcjw&oe=61C308A3&_nc_sid=21929d", "media_preview": "ABgqvtIqnbyT1wAT/Km+YPRv++TTCcSn/dH86lL+n8qQDPNGQCGG7gZGKKjkbLJnn5vT2NFAFa9JEgI44qEbj3P5mrcoPmbsZG3H45qLypSdyqcE5xx+nNMhp9BiqQyt7j+dFXPIcrnHORxxRTEroe6k8g4z7A/zpm1zwW4+g/wp0Z4p1Sagqkd/0H+FFOPQ0UAf/9k=", "gating_info": None, "fact_check_overall_rating": None, "fact_check_information": None, "sharing_friction_info": {"should_have_sharing_friction": False, "bloks_app_url": None}, "media_overlay_info": None, "sensitivity_friction_info": None, "taken_at_timestamp": 1640025862, "expiring_at_timestamp": 1640112262, "story_cta_url": None, "story_view_count": None, "is_video": True, "owner": {"id": "2235780635", "profile_pic_url": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-19/s150x150/187686436_825975598339132_6757154020984796263_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=104&_nc_ohc=Ph8B4An5-m8AX_cAatT&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT9UanqLwMkc-nYjC86Wkhj8VLMfIKjYUnR2WGX5W3y69Q&oe=61C733C6&_nc_sid=21929d", "username": "syh_doriane", "followed_by_viewer": False, "requested_by_viewer": False}, "tracking_token": "eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiNDg0NWJmNTAyZDYzNDZlNDhkZWVjZWFmNzcxMmQ5NWEyNzMzMDU3NDkyNzgzMDE4NzcwIiwic2VydmVyX3Rva2VuIjoiMTY0MDAyNjA2MjkxMXwyNzMzMDU3NDkyNzgzMDE4NzcwfDUwNzU0MjIyNzA3fGJjYmVkMjI0ZWVhMDZjMDBiMWRjODA3OTE0ODk3YmNjYTVhOGE5MmU5MmM4ZDc0ZWQxYjY1ZTVlMzdkNDljNmQifSwic2lnbmF0dXJlIjoiIn0=", "has_audio": True, "overlay_image_resources": None, "video_duration": 3.066, "video_resources": [{"src": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t50.12441-16/269674275_1051599902298481_5926364055401693769_n.mp4?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=101&_nc_ohc=WIQ3U-vXNa8AX9cleGV&tn=88XWGoZ_UZspQpVS&edm=AHlfZHwBAAAA&ccb=7-4&oe=61C2CAF8&oh=00_AT-GAGQnjFrRjMM9AYTWy4MPa-nDd1Xaxp23PJNiK2Fuvw&_nc_sid=21929d", "config_width": 480, "config_height": 852, "mime_type": "video/mp4; codecs=\"avc1.42E01E, mp4a.40.2\"", "profile": "BASELINE"}], "tappable_objects": [{"__typename": "GraphTappableMention", "x": 0.535231953370027, "y": 0.144771888686022, "width": 0.026907162443543003, "height": 0.0036398887518210004, "rotation": -0.038332467406075, "custom_title": None, "attribution": None, "username": "229eaglemotion", "full_name": "229eaglemotion", "is_private": False}], "story_app_attribution": None, "edge_media_to_sponsor_user": {"edges": []}, "muting_info": None}, "instaloader": {"version": "4.8.2", "node_type": "StoryItem"}}]
   # stories = [
   #  {
   #     "node":{
   #        "audience":"MediaAudience.DEFAULT",
   #        "__typename":"GraphStoryVideo",
   #        "id":"2731478126261253082",
   #        "dimensions":{
   #           "height":1137,
   #           "width":640
   #        },
   #        "display_resources":[
   #           {
   #              "src":"https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e15/268325729_750579929667364_4176218990049020135_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=104&_nc_ohc=iS0YG2gsS-AAX_BczQ1&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-206xMPyG3Fy1VF2I-9z7JwfZgN9gdqDV0AU-6Kx506A&oe=61C0872D&_nc_sid=21929d",
   #              "config_width":640,
   #              "config_height":1137
   #           },
   #           {
   #              "src":"https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e15/268325729_750579929667364_4176218990049020135_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=104&_nc_ohc=iS0YG2gsS-AAX_BczQ1&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-206xMPyG3Fy1VF2I-9z7JwfZgN9gdqDV0AU-6Kx506A&oe=61C0872D&_nc_sid=21929d",
   #              "config_width":750,
   #              "config_height":1332
   #           },
   #           {
   #              "src":"https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e15/268325729_750579929667364_4176218990049020135_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=104&_nc_ohc=iS0YG2gsS-AAX_BczQ1&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-206xMPyG3Fy1VF2I-9z7JwfZgN9gdqDV0AU-6Kx506A&oe=61C0872D&_nc_sid=21929d",
   #              "config_width":1080,
   #              "config_height":1918
   #           }
   #        ],
   #        "display_url":"https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e15/268325729_750579929667364_4176218990049020135_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=104&_nc_ohc=iS0YG2gsS-AAX_BczQ1&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-206xMPyG3Fy1VF2I-9z7JwfZgN9gdqDV0AU-6Kx506A&oe=61C0872D&_nc_sid=21929d",
   #        "media_preview":"ABgqtrU6tiqwOamGKxTOhlrzKKr5oq+YixUDYqUPVYen8qeCfpWRoWc96KjU0UxFXNKDTFp1AiVTRS0Uij//2Q==",
   #        "gating_info":None,
   #        "fact_check_overall_rating":None,
   #        "fact_check_information":None,
   #        "sharing_friction_info":{
   #           "should_have_sharing_friction":False,
   #           "bloks_app_url":None
   #        },
   #        "media_overlay_info":None,
   #        "sensitivity_friction_info":None,
   #        "taken_at_timestamp":1639837585,
   #        "expiring_at_timestamp":1639923985,
   #        "story_cta_url":None,
   #        "story_view_count":None,
   #        "is_video":True,
   #        "owner":{
   #           "id":"255391219",
   #           "profile_pic_url":"https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-19/s150x150/69239464_2715622995147419_7869939009076592640_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=111&_nc_ohc=a9xERC0RLVoAX81oZty&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT9BSIP6fybyX7Ot0IPBONtlflatO5mIFMah2JsjwDxuPg&oe=61C44BFA&_nc_sid=21929d",
   #           "username":"229eaglemotion",
   #           "followed_by_viewer":False,
   #           "requested_by_viewer":False
   #        },
   #        "tracking_token":"eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiMDZmYTI4YTRlZDYzNDBkNTg0MWU0ZjBhMDVkZWVlNmUyNzMxNDc4MTI2MjYxMjUzMDgyIiwic2VydmVyX3Rva2VuIjoiMTYzOTgzNzYxNDg0NHwyNzMxNDc4MTI2MjYxMjUzMDgyfDUwNzU0MjIyNzA3fGE4MWJkYmM5NTJmYTY5ZDBmMDkwYWJmYzkzYWU3MDJhZjRiNjNhNjNmOGE0MDFhYjJiMDJhNGVhMjdkMzNiY2YifSwic2lnbmF0dXJlIjoiIn0=",
   #        "has_audio":True,
   #        "overlay_image_resources":None,
   #        "video_duration":2.09,
   #        "video_resources":[
   #           {
   #              "src":"https://instagram.fcoo1-2.fna.fbcdn.net/v/t50.12441-16/267669894_1088701278572441_1590994383961152622_n.mp4?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=105&_nc_ohc=TlwyXbiOa6kAX8Nj5us&edm=AHlfZHwBAAAA&ccb=7-4&oe=61C03E21&oh=00_AT-HDS2adHWgNNKqOgGQ0rEMIUG-M_5adGXSXkRkAyYGXQ&_nc_sid=21929d",
   #              "config_width":480,
   #              "config_height":852,
   #              "mime_type":"video/mp4; codecs=\"avc1.42E01E, mp4a.40.2\"",
   #              "profile":"BASELINE"
   #           }
   #        ],
   #        "tappable_objects":[
   #           {
   #              "__typename":"GraphTappableMention",
   #              "x":0.5,
   #              "y":0.27811094452773605,
   #              "width":0.32007999999999903,
   #              "height":0.044977511244377,
   #              "rotation":0.0,
   #              "custom_title":None,
   #              "attribution":None,
   #              "username":"229eaglemotion",
   #              "full_name":"229eaglemotion",
   #              "is_private":False
   #           }
   #        ],
   #        "story_app_attribution":None,
   #        "edge_media_to_sponsor_user":{
   #           "edges":[
                
   #           ]
   #        },
   #        "muting_info":None
   #     },
   #     "instaloader":{
   #        "version":"4.8.2",
   #        "node_type":"StoryItem"
   #     }
   #  }, {"node": {"audience": "MediaAudience.DEFAULT", "__typename": "GraphStoryImage", "id": "2730293655191842125", "dimensions": {"height": 1334, "width": 750}, "display_resources": [{"src": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/sh0.08/e35/p640x640/268445457_1367745210331147_8589600088301699084_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=Qqq-1z9oObUAX89hiy3&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-C7JrYZlTWjG2FMHg8x37sE6b_-TW6AQ7YrRpYxAWKdg&oe=61BE5903&_nc_sid=21929d", "config_width": 640, "config_height": 1138}, {"src": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e35/268445457_1367745210331147_8589600088301699084_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=Qqq-1z9oObUAX89hiy3&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_y_YXEgUGimKvcGolnonas6ysyd5sIrTaC-CBa7CmXIw&oe=61BDCF1B&_nc_sid=21929d", "config_width": 750, "config_height": 1334}, {"src": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e35/268445457_1367745210331147_8589600088301699084_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=Qqq-1z9oObUAX89hiy3&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_y_YXEgUGimKvcGolnonas6ysyd5sIrTaC-CBa7CmXIw&oe=61BDCF1B&_nc_sid=21929d", "config_width": 1080, "config_height": 1920}], "display_url": "https://instagram.fcoo1-1.fna.fbcdn.net/v/t51.2885-15/e35/268445457_1367745210331147_8589600088301699084_n.jpg?_nc_ht=instagram.fcoo1-1.fna.fbcdn.net&_nc_cat=107&_nc_ohc=Qqq-1z9oObUAX89hiy3&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT_y_YXEgUGimKvcGolnonas6ysyd5sIrTaC-CBa7CmXIw&oe=61BDCF1B&_nc_sid=21929d", "media_preview": "ABgq5qiiigAooooAKKKKACiiigAooooAKKKKAP/Z", "gating_info": None, "fact_check_overall_rating": None, "fact_check_information": None, "sharing_friction_info": {"should_have_sharing_friction": False, "bloks_app_url": None}, "media_overlay_info": None, "sensitivity_friction_info": None, "taken_at_timestamp": 1639696382, "expiring_at_timestamp": 1639782782, "story_cta_url": None, "story_view_count": None, "is_video": False, "owner": {"id": "255391219", "profile_pic_url": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-19/s150x150/69239464_2715622995147419_7869939009076592640_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=111&_nc_ohc=a9xERC0RLVoAX81oZty&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT86OB_d0-AzZQ8hEYoPkAVfF12zbZdgxk7HCSD2OLikQA&oe=61C251BA&_nc_sid=21929d", "username": "hpfpv", "followed_by_viewer": False, "requested_by_viewer": False}, "tracking_token": "eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiZmQ3NGI2ZTFlZTM1NDE2M2E2YTIzNzM5N2IzOTJmM2YyNzMwMjkzNjU1MTkxODQyMTI1Iiwic2VydmVyX3Rva2VuIjoiMTYzOTY5OTMwMjU3OHwyNzMwMjkzNjU1MTkxODQyMTI1fDUwNzU0MjIyNzA3fDY1MTRkNjUyZGRiZDNhZmNiMWVlZTdhMzIwZmIyYTg1YzNmOTNhMGM4ZjYzMTlhYzQ3Y2IwZTk2OGY5MmU1YTUifSwic2lnbmF0dXJlIjoiIn0=", "tappable_objects": [{"__typename": "GraphTappableMention", "x": 0.5, "y": 0.27811094452773605, "width": 0.32007999999999903, "height": 0.044977511244377, "rotation": 0.0, "custom_title": None, "attribution": None, "username": "229eaglemotion", "full_name": "229eaglemotion", "is_private": False}], "story_app_attribution": None, "edge_media_to_sponsor_user": {"edges": []}, "muting_info": None}, "instaloader": {"version": "4.8.2", "node_type": "StoryItem"}}, {"node": {"audience": "MediaAudience.DEFAULT", "__typename": "GraphStoryImage", "id": "2729916333045328299", "dimensions": {"height": 1334, "width": 750}, "display_resources": [{"src": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/sh0.08/e35/p640x640/268430240_648286416303865_1516137624972219047_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=101&_nc_ohc=pTOrC1zKXpsAX-dMaN0&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT-IVvTdxXeE3zGN8XjiI8Irk74aRFrFdyyEliOxyO5g_Q&oe=61BE0FFA&_nc_sid=21929d", "config_width": 640, "config_height": 1138}, {"src": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e35/268430240_648286416303865_1516137624972219047_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=101&_nc_ohc=pTOrC1zKXpsAX-dMaN0&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT8ftXSM2RiCuyRVgLv0OX1JWrFI3jqcLpONx8svLm27kA&oe=61BE5314&_nc_sid=21929d", "config_width": 750, "config_height": 1334}, {"src": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e35/268430240_648286416303865_1516137624972219047_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=101&_nc_ohc=pTOrC1zKXpsAX-dMaN0&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT8ftXSM2RiCuyRVgLv0OX1JWrFI3jqcLpONx8svLm27kA&oe=61BE5314&_nc_sid=21929d", "config_width": 1080, "config_height": 1920}], "display_url": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-15/e35/268430240_648286416303865_1516137624972219047_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=101&_nc_ohc=pTOrC1zKXpsAX-dMaN0&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT8ftXSM2RiCuyRVgLv0OX1JWrFI3jqcLpONx8svLm27kA&oe=61BE5314&_nc_sid=21929d", "media_preview": "ABgq1aKKKACiiigAooooAKKKKACiiigAooooA//Z", "gating_info": None, "fact_check_overall_rating": None, "fact_check_information": None, "sharing_friction_info": {"should_have_sharing_friction": False, "bloks_app_url": None}, "media_overlay_info": None, "sensitivity_friction_info": None, "taken_at_timestamp": 1639651405, "expiring_at_timestamp": 1639737805, "story_cta_url": None, "story_view_count": None, "is_video": False, "owner": {"id": "255391219", "profile_pic_url": "https://instagram.fcoo1-2.fna.fbcdn.net/v/t51.2885-19/s150x150/69239464_2715622995147419_7869939009076592640_n.jpg?_nc_ht=instagram.fcoo1-2.fna.fbcdn.net&_nc_cat=111&_nc_ohc=a9xERC0RLVoAX81oZty&edm=AHlfZHwBAAAA&ccb=7-4&oh=00_AT86OB_d0-AzZQ8hEYoPkAVfF12zbZdgxk7HCSD2OLikQA&oe=61C251BA&_nc_sid=21929d", "username": "hpfpv", "followed_by_viewer": False, "requested_by_viewer": False}, "tracking_token": "eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiZmQ3NGI2ZTFlZTM1NDE2M2E2YTIzNzM5N2IzOTJmM2YyNzI5OTE2MzMzMDQ1MzI4Mjk5Iiwic2VydmVyX3Rva2VuIjoiMTYzOTY5OTMwMjU3N3wyNzI5OTE2MzMzMDQ1MzI4Mjk5fDUwNzU0MjIyNzA3fDhhZDQ2NzUwMzFlYTk5MDdjYmNlYTEyZWY5MDY1NWIxYjk3NmU0OTA1OTkxNzJmZTE5ZGEyYmQxOTM1ODUyNjkifSwic2lnbmF0dXJlIjoiIn0=", "tappable_objects": [{"__typename": "GraphTappableMention", "x": 0.5, "y": 0.42503748125937, "width": 0.32007999999999903, "height": 0.044977511244377, "rotation": 0.0, "custom_title": None, "attribution": None, "username": "229eaglemotion", "full_name": "229eaglemotion", "is_private": False}], "story_app_attribution": None, "edge_media_to_sponsor_user": {"edges": []}, "muting_info": None}, "instaloader": {"version": "4.8.2", "node_type": "StoryItem"}}]
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
      # response_json = stories_response_json(response)
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