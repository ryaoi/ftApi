
import requests
from sys import exit
import json
import re

def GetJson(url):
    """
    params: url
    return: json

    get the content from the url and return the json
    """
    try:
        response = requests.get(url)
    except Exception as e:
        print(e)
        return None
    try:
        docs = json.loads(response.text)
        return docs
    except TypeError as e:
        print(e)
        return None


def GetEndpoints(docs):
    apiResources = [elem for elem in docs['docs']['resources']]
    endpoints = []
    for resource in apiResources:
        for methods in docs['docs']['resources'][resource]['methods']:
            for method in methods['apis']:
                print(method['api_url'], method['http_method'])
                endpoints.append(method['api_url'])

    return set(endpoints)

def CreateApiHandler(docs):
    endpoints = GetEndpoints(docs)

    print(endpoints)
    for endpoint in endpoints:
        if "graph(/on/:field(/by/:interval))" in endpoint:
            continue

        variables = re.findall("(\/:\w+)", endpoint)

        url = endpoint
        params = ""
        if len(variables):
            params = ", " + ", ".join((elem[2:] for elem in variables))
            for value in variables:
                endpoint = endpoint.replace(value, "")
                url = url.replace(value, "/{}")

        splitedValue = endpoint[4:].split("/")
        funcName = "".join((elem.capitalize() for elem in splitedValue))
        payload = """
    def {}(self{}):
        extension = "{}".format({})
        return HttpMethod(extension, self.session)
        """

        print(payload.format(funcName, params, url, params[2:]))


if __name__ == "__main__":
    docs = GetJson("https://api.intra.42.fr/apidoc")
    if docs is None:
        exit(-1)
    CreateApiHandler(docs)
