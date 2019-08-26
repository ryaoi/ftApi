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
        self.url = "https://api.intra.42.fr{}".format(extension)
        self.session = session

    def get(self):
        """
        return json
        """
        response = self.session.get(self.url)
        response.raise_for_status()
        return json.loads(response.text)

    def post(self, data):
        """
        return response Object
        """
        response = self.session.post(self.url, json=data)
        response.raise_for_status()
        return response

    def patch(self, data):
        """
        return response Object
        """
        response = self.session.patch(self.url, json=data)
        response.raise_for_status()
        return response

    def put(self, data):
        """
        return response Object
        """
        response = self.session.put(self.url, json=data)
        response.raise_for_status()
        return response

    def delete(self):
        """
        return response Object
        """
        response = self.session.delete(self.url)
        response.raise_for_status()
        return response

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

        example :"/v2/users?filter[pool_year]=2019&page[size]=100&page[number]=3"
        """
        return HttpMethod(endpoint, self.session)

    def ColorizeJsonOutput(self, jsonObject):
        jsonStr = json.dumps(jsonObject, indent=4, sort_keys=True)
        print(highlight(jsonStr, JsonLexer(), TerminalFormatter()))
