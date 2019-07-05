import requests
import json
import os
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

class HttpMethod:

    """
    HttpMethod will have methods to send
    GET, POST, PATCH, PUT, DELETE request to the initalized url
    """

    def __init__(self, extension, session):
        self.url = "https://api.intra.42.fr/{}".format(extension)
        self.session = session

    def get(self):
        try:
            response = self.session.get(self.url)
            return json.loads(response.text)
        except Exception as e:
            print("[-]", e)
            return None

    def post(self, data):
        try:
            response = self.session.post(self.url, data=data)
            return json.loads(response.text)
        except Exception as e:
            print("[-]", e)
            return None

    def patch(self, data):
        try:
            response = self.session.patch(self.url, data=data)
            return json.loads(response.text)
        except Exception as e:
            print("[-]", e)
            return None

    def put(self, data):
        try:
            response = self.session.put(self.url, data=data)
            return json.loads(response.text)
        except Exception as e:
            print("[-]", e)
            return None

    def delete(self):
        try:
            response = self.session.delete(self.url)
            return json.loads(response.text)
        except Exception as e:
            print("[-]", e)
            return None

class FtApi:

    def __init__(self, uid, secret):
        self.uid = uid
        self.secret = secret
        try:
            self.bearer = self.GetBearer()
        except Exception as e:
            raise Exception(e)
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Bearer {}'.format(self.bearer)})

    def GetBearer(self):
        """
        Makes a call to get Bearer with your crendentials
        return: string
        """
        payload = {'grant_type':'client_credentials', 'client_id': self.uid,
                'client_secret': self.secret}
        try:
            test = requests.post("https://api.intra.42.fr/oauth/token", data=payload)
            if test.status_code != 200:
                raise Exception("wrong status_code:{}".format(test.status_code))
            parsed_response = json.loads(test.content.decode('utf-8'))
        except Exception as e:
            raise Exception(e)
        
        return parsed_response['access_token']

    def ReloadBearer(self):
        """
        Use this method in case 'The access token expired'
        """
        self.bearer = self.GetBearer()
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Bearer {}'.format(self.bearer)})

    def RawEndpoint(self, endpoint):
        """
        parameter : string
        return : HttpMethod
        
        Create a HttpMethod with passed parameter as the endpoint for "https://api.intra.42.fr/"
        """
        return HttpMethod(endpoint, self.session)

    def ColorizeJsonOutput(self, jsonObject):
        jsonStr = json.dumps(jsonObject, indent=4, sort_keys=True)
        print(highlight(jsonStr, JsonLexer(), TerminalFormatter()))
