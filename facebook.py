import facebook_oauth2
import requests
import json

token = facebook_oauth2.get_token()

class notifications:
    def __init__(self):
        print("Connecting to facebook")
        notifications_url = 'https://graph.facebook.com/me/notifications?access_token={}'.format(token)
        response = requests.get(notifications_url)
        self.response_json = json.loads(response.text)
        self.notifications = [item['title'] for item in self.response_json['data']]
        self.amount_unread = len(self.response_json['data'])
