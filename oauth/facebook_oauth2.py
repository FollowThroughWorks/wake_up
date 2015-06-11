import requests
import webbrowser
import threading
import time
from wsgiref.simple_server import make_server
import json
import os

# JSON file with app id and secret
APP_INFO_PATH = 'data/facebook_app_info.json'

with open(APP_INFO_PATH) as app_info_file:
    app_info = json.loads(app_info_file.read())
    app_id = app_info['app_id']
    app_secret = app_info['app_secret'] #'a8437acfac3a8a988200fdea903ee165'

site_url = r'http://localhost:8051/'
permissions = 'manage_notifications'

code_file = 'data/facebook_code.txt'
token_file = 'data/facebook_token.txt'

# Set up server to handle redirect request from facebook
def run_server(host,port,fcn):
    my_server = make_server(host,port,fcn)
    my_server.handle_request()

# Code that is run when "server" receives request; saves code from facebook's response
def get_code(environ,start_response):
    response_body = ['{}:{}'.format(key,value) for key,value in sorted(environ.items())]
    response_body = '\n'.join(response_body)
    
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain',),
                        ('Content-Length',str(len(response_body)))]
    start_response(status,response_headers)

    with open(code_file,'w') as f:
        f.write(environ['QUERY_STRING'])
        
    return [response_body.encode()]

def get_token():
    print("Getting facebook token...")
    # Check to see if token already exists; if not, continue on to retrieve and save it
    try:
        with open(token_file) as f:
            token = f.read()
            return token
    except FileNotFoundError:
        print("Token not found; retrieving now.")
        pass
    # ADD IN TOKEN CHECK, TO SEE IF EXPIRED

    # 1) Set up server thread to handle facebook response with code

    print("Starting server thread")
    server_args = ('',8051,get_code)
    server_thread = threading.Thread(target = run_server, args = server_args)
    server_thread.start()

    # 2) Go to url with APP ID, REDIRECT URL, and PERMISSIONS; facebook redirects to localhost with CODE

    print("Opening browser for permission")
    get_code_url = 'https://www.facebook.com/dialog/oauth?' \
                'client_id={}' \
                '&redirect_uri={}' \
                '&scope={}'.format(app_id,site_url,permissions)

    webbrowser.open_new(get_code_url)

    # 3) Once user grants permission, server receives request and writes code to  code_file
    # which is then read in as a variable
    print("Waiting for server to receive and handle request")
    time.sleep(5)
    with open(code_file) as f:
        code = f.read().split('=')[1]
    os.remove(code_file)

    # 4) Go to url with APP ID & SECRET, REDIRECT URL, and now-received CODE, to receive TOKEN; save token
    get_token_url = 'https://graph.facebook.com/v2.3/oauth/access_token?' \
                    'client_id={}' \
                    '&redirect_uri={}' \
                    '&client_secret={}' \
                    '&code={}'.format(app_id,site_url,app_secret,code)

    response = requests.get(get_token_url)
    token = json.loads(response.text)['access_token']
    with open(token_file,'w') as f:
        f.write(token)
    return token
