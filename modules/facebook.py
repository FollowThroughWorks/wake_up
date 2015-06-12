import oauth.facebook_oauth2  as facebook_oauth2 
import requests
import json
from utilities import text_to_speech as tts # For text to speech

token = facebook_oauth2.get_token()

class notifications:
    def __init__(self):
        print("Connecting to facebook")
        notifications_url = 'https://graph.facebook.com/me/notifications?access_token={}'.format(token)
        response = requests.get(notifications_url)
        self.response_json = json.loads(response.text)
        self.notifications = [item['title'] for item in self.response_json['data']]
        self.unread_count = len(self.response_json['data'])
        try:
            self.unseen_count = self.response_json['summary']['unseen_count']
        except KeyError:
            self.unseen_count = 0

    def notifications_message(self):
        message = "You have {} unseen notifications, and {} unread notifications".format(self.unseen_count,self.unread_count)
        print(message)
        tts(message)
