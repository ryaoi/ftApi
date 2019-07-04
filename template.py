import requests
import json
import os

class HttpMethod:
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

    def RawEndpoint(self, endpoint):
        return HttpMethod(endpoint, self.session)

