import os
import load_dotenv
import requests

from dotenv import load_dotenv

class Git_api():
    def __init__(self):
        load_dotenv()
        self.token: str = ""
        self.get_token()