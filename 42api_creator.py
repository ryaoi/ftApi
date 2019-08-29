
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
                print(method)
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
        secondMatches = re.findall("(\/v2[\/\w+]+)(\/:\w+)(\/\w+)*", endpoints[index + 1])
        print(firstMatches, secondMatches)
        if len(firstMatches) == len(secondMatches)  \
                and len(secondMatches[0]) == 3 and secondMatches[0][2] == '' \
                and firstMatches[0] == secondMatches[0][0]:
            variable = re.findall("(\/:\w+)", endpoints[index + 1])[0]
            url = endpoints[index]
            #params = ", {}=None".format(variable[2:])
            # params = ", *args, {}=None, **kwargs".format(variable[2:])
            params = ", {}=None, **kwargs".format(variable[2:])
            endpoints[index] = endpoints[index].replace(variable, "")
            url = url.replace(variable, "/{}")

            splitedValue = endpoints[index][4:].split("/")
            funcName = "".join((elem.capitalize() for elem in splitedValue))
            payload = """
    def {}(self{}):
        {}
        More details: "https://api.intra.42.fr/apidoc/2.0/{}.html"
        {}
        extension = "{}/{}".format({}) if {} is not None else "{}"
        return HttpMethod(extension, self.session, **kwargs)
        """

            # print(payload.format(funcName, params, url, "{}", variables[0][2:], variables[0][2:], url))
            f.write(payload.format(funcName, params, '"""', endpoints[index].replace("/v2/", ""), '"""', url, "{}", variable[2:], variable[2:], url))

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

        # "/v2/test/aaaa" -> ['test', 'aaaa']
        splitedValue = endpoint[4:].split("/")
        funcName = "".join((elem.capitalize() for elem in splitedValue))
        if params == "":
            payload = """
    def {}(self{}):
        {}
        More details: "https://api.intra.42.fr/apidoc/2.0/{}.html"
        {}
        extension = "{}"
        return HttpMethod(extension, self.session, **kwargs)
        """

            # f.write(payload.format(funcName, params, '"""', funcName.lower(), '"""', url))
            f.write(payload.format(funcName, ", **kwargs", '"""', funcName.lower(), '"""', url))

        else:
            payload = """
    def {}(self{}):
        extension = "{}".format({})
        return HttpMethod(extension, self.session, **kwargs)
        """
            # f.write(payload.format(funcName, params, url, params[2:]))
            f.write(payload.format(funcName, params + ",**kwargs", url, params[2:]))

def AppendMethods(docs, f):
    """
    Create methods to a .py file
    """
    endpoints = GetEndpoints(docs)
    #endpoints.sort()

    splittedEndpoints = []
    for endpoint in endpoints:
        print(endpoint, endpoint.find("/"))
        if endpoint.count("/") == 2:
            splittedEndpoints.append([endpoint, ''])
            continue
        indices = [x.start() for x in re.finditer("/", endpoint)]
        part1 = endpoint[0:indices[2]]
        part2 = endpoint[indices[2]+1:]
        splittedEndpoints.append([part1, part2])
    splittedEndpoints.sort(key=lambda item: (item[0], len(item[1])))
    endpoints = ["{}/{}".format(elem[0], elem[1]) if len(elem[1]) else elem[0] for elem in splittedEndpoints]

    remainEndpoints = CreateKwargHandler(endpoints, f)
    for elem in remainEndpoints:
        print(elem)
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
