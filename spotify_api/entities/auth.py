
import base64
import binascii
import datetime
import json
import os
import urllib.parse
import webbrowser

import requests

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from spotify_api.config import cfg_item

state = binascii.hexlify(os.urandom(20)).decode('utf-8')
code = None

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global code
        self.close_connection = True
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if not query['state'] or query['state'][0] != state:
            raise RuntimeError("state argument missing or invalid")
        code = query['code']

class Auth:
    __server = 'localhost'
    __port = 8081
    __redirect_uri = f'http://{__server}:{__port}'
    __base_url = 'https://accounts.spotify.com/'
    __auth_endpoint = 'authorize'
    __get_token_endpoint = 'api/token'
    __auth_file = 'f_token.json'
    __scope = ['user-top-read','user-read-email']

    def __init__(self):
        self.__data = None
        self.__client_id = cfg_item("client_id") 
        self.__client_secret = cfg_item("client_secret") 

    def get_token(self):
        if not os.path.isfile(Auth.__auth_file):
            self.__generate_token()
        else:
            self.__load_token_from_file()
            if not self.__data.get('token', ''):
                self.__generate_token()
            else:
                now = datetime.datetime.now()
                if now > datetime.datetime.fromisoformat(self.__data['expires']):
                    if self.__data['refresh_token']:
                        self.__refresh_token()
                    else:
                        self.__generate_token()

        return self.__data['token']

    def __generate_token(self):
        url = self.__create_oauth_link()
        webbrowser.open_new_tab(url)

        server = HTTPServer((Auth.__server, Auth.__port), RequestHandler)
        server.handle_request()

        self.__exchange_code_for_access_token(code)

    def __refresh_token(self):
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.__data['refresh_token']
        }

        auth_header = base64.b64encode(f'{self.__client_id}:{self.__client_secret}'.encode())

        headers = {"Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth_header.decode('ascii')}"}

        endpoint = Auth.__base_url + Auth.__get_token_endpoint

        response = requests.post(endpoint, data=data, headers=headers)

        if response:
            response_json = response.json()
            self.__save_token_to_file(response_json["access_token"], '', response_json['expires_in'])
            self.__load_token_from_file()
        else:
            raise Exception(f"Could Not Get Token... {response.status_code} = {response.content}")

    def __create_oauth_link(self):

        params = {
            "client_id": self.__client_id,
            "redirect_uri": Auth.__redirect_uri,
            "response_type": "code",
            "scope" : ' '.join(Auth.__scope),
            "state" : state
        }

        endpoint = Auth.__base_url + Auth.__auth_endpoint
        response = requests.get(endpoint, params=params)

        if response:
            url = response.url
            return url
        else:
            raise Exception(f"Could Not Get An Url... {response.status_code} = {response.content}")

    def __exchange_code_for_access_token(self, code=None):
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": Auth.__redirect_uri,
        }

        auth_header = base64.b64encode(f'{self.__client_id}:{self.__client_secret}'.encode())

        headers = {"Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth_header.decode('ascii')}"}

        endpoint = Auth.__base_url + Auth.__get_token_endpoint

        response = requests.post(endpoint, data=data, headers=headers)
        response_json = response.json()

        if response:
            self.__save_token_to_file(response_json["access_token"], response_json["refresh_token"], response_json['expires_in'])
            self.__load_token_from_file()
        else:
            raise Exception(f"Could Not Get Token... {response.status_code} = {response.content}")

    def __save_token_to_file(self, token, refresh_token, expires_in):
        expires = datetime.datetime.now() + datetime.timedelta(seconds = expires_in)
        with open(Auth.__auth_file, 'w') as file:
            json.dump({"token":token, "refresh_token":refresh_token, "expires": expires.isoformat()}, file)

    def __load_token_from_file(self):
        with open(Auth.__auth_file, 'r') as file:
            self.__data = json.load(file)

    '''def __load_secret(self):
        with open(Auth.__secret_file, 'r') as file:
            secret = json.load(file)

        return secret.get('client_id',''), secret.get('client_secret','')'''