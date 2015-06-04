from anydo.api import AnyDoAPI
import json

class any_do:
    def __init__(self):
        ANYDO_CREDENTIALS_PATH = 'data/anydo_credentials.json'
        with open(ANYDO_CREDENTIALS_PATH) as f:
            anydo_credentials = json.loads(f.read())
            
        user_ = anydo_credentials['user']
        pass_ = anydo_credentials['pass']

        anydo_api = AnyDoAPI(username=user_,password=pass_)

        tasks = anydo_api.get_all_tasks()
        self.task_names = [task['title'] for task in tasks]
        self.task_count = len(tasks)
