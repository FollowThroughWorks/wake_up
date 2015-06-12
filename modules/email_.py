import oauth.google_oauth2 as google_oauth2 # oauth
from apiclient.discovery import build
from utilities import text_to_speech as tts # For text to speech

from httplib2 import Http

GOOGLE_CREDENTIALS = google_oauth2.get_credentials()

# Google keep
class gmail:
    def __init__(self):
        print("Connecting to gmail...")
        self.service = build('gmail', 'v1', http=GOOGLE_CREDENTIALS.authorize(Http()))

    def unread_emails(self):
        print("Retrieving gmail info...")
        emails = self.service.users().messages().list(
            userId='me',
            q='is:unread').execute()
        
        unread = len(emails['messages'])
        
        while 'nextPageToken' in emails:
            page_token = emails['nextPageToken']
            emails = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                pageToken=page_token).execute()
            unread += len(emails['messages'])

        return unread

    def unread_emails_message(self):
        message = "You have {} unread emails".format(self.unread_emails())
        print(message)
        tts(message)
