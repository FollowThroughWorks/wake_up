import datetime
import os

import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

CREDENTIALS_PATH = 'c:/mg/wake_up/credentials.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/calendar.readonly']
CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Wake Up!'

def get_credentials():
    # Get credentials saved on system
    credential_path = CREDENTIALS_PATH
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    # If there are no saved credentials, generate them
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow,store,flags)
        print('Storing credentials to {}'.format(credential_path))
    return credentials

def delete_credentials():
    os.remove(CREDENTIALS_PATH)
    return

if __name__ == '__main__':
    delete_credentials()
