import json

from os import environ
from dotenv import load_dotenv


load_dotenv()

if __name__ == '__main__':
    with open(environ['GCP_SERVICE_ACCOUNT_FILE'], 'r') as f:
        info = json.load(f)
    print(info)