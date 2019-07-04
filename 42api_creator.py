
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

    return list(set(endpoints))

def CreateKwargHandler(endpoints, f):
    """
    Create methods which contains kwargs
    and return the remaining endpoints to handle
    """
    index = 0

    # endpoints = ["/v2/users", "/v2/users/:id"]
    remainEndpoints = []
    while index < len(endpoints) - 1:
        firstMatches = re.findall("(\/v2[\/\w+]+)", endpoints[index])
        secondMatches = re.findall("(\/v2[\/\w+]+)(\/:\w+)", endpoints[index + 1])

        if len(firstMatches) == 1 and len(secondMatches) and firstMatches[0] == secondMatches[0][0]:
            variable = re.findall("(\/:\w+)", endpoints[index + 1])[0]
            print(variable)
            url = endpoints[index]
            params = ""

            # params = ", " + ", ".join((elem[2:] + "=None" for elem in variables))
            params = ", {}=None".format(variable[2:])
            endpoints[index] = endpoints[index].replace(variable, "")
            url = url.replace(variable, "/{}")

            splitedValue = endpoints[index][4:].split("/")
            funcName = "".join((elem.capitalize() for elem in splitedValue))
            payload = """
    def {}(self{}):
        extension = "{}/{}".format({}) if {} is not None else "{}"
        return HttpMethod(extension, self.session)
        """

            # print(payload.format(funcName, params, url, "{}", variables[0][2:], variables[0][2:], url))
            f.write(payload.format(funcName, params, url, "{}", variable[2:], variable[2:], url))

            index += 2
        else:
            remainEndpoints.append(endpoints[index])
            index += 1

    return remainEndpoints


def CreateHandler(endpoints, f):
    for endpoint in endpoints:
        # if someone wants to handle graph for me
        # I appreciate
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
        if params == "":
            payload = """
    def {}(self{}):
        extension = "{}"
        return HttpMethod(extension, self.session)
        """

            # print(payload.format(funcName, params, url))
            f.write(payload.format(funcName, params, url))

        else:
            payload = """
    def {}(self{}):
        extension = "{}".format({})
        return HttpMethod(extension, self.session)
        """
            # print(payload.format(funcName, params, url, params[2:]))
            f.write(payload.format(funcName, params, url, params[2:]))

def AppendMethods(docs, f):
    """
    Create methods to a .py file
    """
    endpoints = GetEndpoints(docs)
    endpoints.sort()

    remainEndpoints = CreateKwargHandler(endpoints, f)
    CreateHandler(remainEndpoints, f)


if __name__ == "__main__":
    docs = GetJson("https://api.intra.42.fr/apidoc")
    if docs is None:
        exit(-1)
    try:
        f = open("FtApi.py", 'w')
    except Exception as e:
        print("[-]", e) 
        exit(-1)
    try:
        with open("template.py", 'r') as template:
            f.write("".join(template.readlines()))
    except Exception as e:
        print("[-]", e) 
        exit(-1)

    print("[+] Copied template !")
    AppendMethods(docs, f)
    print("[+] Created methods for 42Api !")
