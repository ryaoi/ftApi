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

    def __init__(self, extension, session, **kwargs):
        self.url = "https://api.intra.42.fr{}".format(extension)
        self.filter = kwargs["filter"] if "filter" in kwargs else {}
        self.page = kwargs["pages"] if "pages" in kwargs else {'size':100, 'number':1}
        self.sort = kwargs["sort"] if "sort" in kwargs else ""
        self.range = kwargs["range"] if "range" in kwargs else {}
        self.session = session

    def ParseParams(self):

        filter_query = "&".join([f"filter[{key}]={value}" for key, value in self.filter.items()]) if self.filter else ""
        page_query = "&".join([f"page[{key}]={value}" for key, value in self.page.items()]) if self.page else ""
        range_query = "&".join([f"range[{key}]={value}" for key, value in self.range.items()]) if self.range else ""

        result = "&".join([query for query in [filter_query, page_query, range_query] if query != ""])

        if self.sort:
            if result:
                result += f"&sort={self.sort}"
            else:
                result = f"sort={self.sort}"

        return f"?{result}" if result else ""
 
    def Get(self):
        """
        return json
        """
        response = self.session.get(self.url + self.ParseParams())
        response.raise_for_status()
        if self.page and "number" in self.page: self.page['number'] += 1
        return json.loads(response.text)

    def Post(self, data):
        """
        return response Object
        """
        response = self.session.post(self.url, json=data)
        try:
            response.raise_for_status()
        except:
            raise Exception(f"[{response.status_code}] {response.content}")
        return response

    def Patch(self, data):
        """
        return response Object
        """
        response = self.session.patch(self.url, json=data)
        try:
            response.raise_for_status()
        except:
            raise Exception(f"[{response.status_code}] {response.content}")
        return response

    def Put(self, data):
        """
        return response Object
        """
        response = self.session.put(self.url, json=data)
        try:
            response.raise_for_status()
        except:
            raise Exception(f"[{response.status_code}] {response.content}")
        return response

    def Delete(self):
        """
        return response Object
        """
        response = self.session.delete(self.url)
        try:
            response.raise_for_status()
        except:
            raise Exception(f"[{response.status_code}] {response.content}")
        return response

class FtApi:

    def __init__(self, uid=None, secret=None, code=None, redirect=None, bearer=None, scope=None):
        self.uid = uid if uid is not None else os.environ['UID42'] if bearer is None else ""
        self.secret = secret if secret is not None else os.environ['SECRET42'] if bearer is None else ""
        self.code = code
        self.redirect = redirect
        self.bearer = bearer
        self.scope = scope if scope is not None else "public projects profile elearning tig forum"
        if self.bearer is None:
            try:
                self.bearer = self.GetBearer()
            except Exception as e:
                raise Exception(e)
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Bearer {}'.format(self.bearer)})

    def FastInit(self):
        self.__init__(os.environ['UID42'], os.environ['SECRET42'])

    def GetBearer(self):
        """
        Makes a call to get Bearer with your crendentials
        return: string
        """
        if self.code:
            payload = {'grant_type':'authorization_code', 'client_id': self.uid,
                    'client_secret': self.secret, 'code':self.code, 'redirect_uri':self.redirect}
        else:
            payload = {'grant_type':'client_credentials', 'client_id': self.uid, "scope": self.scope,
                    'client_secret': self.secret}
        try:
            response = requests.post("https://api.intra.42.fr/oauth/token", data=payload)
            if response.status_code != 200:
                raise Exception("wrong status_code:{}".format(response.status_code))
            parsed_response = json.loads(response.content.decode('utf-8'))
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

    def RawEndpoint(self, endpoint, **kwargs):
        """
        parameter : string
        return : HttpMethod

        Create a HttpMethod with passed parameter as the endpoint for "https://api.intra.42.fr/"

        example :"/v2/users?filter[pool_year]=2019&page[size]=100&page[number]=3"
        """
        return HttpMethod(endpoint, self.session, **kwargs)

    def ColorizeJsonOutput(self, jsonObject):
        jsonStr = json.dumps(jsonObject, indent=4, sort_keys=True)
        print(highlight(jsonStr, JsonLexer(), TerminalFormatter()))

    def Accreditations(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/accreditations.html"
        """
        extension = "/v2/accreditations/{}".format(id) if id is not None else "/v2/accreditations"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Achievements(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/achievements.html"
        """
        extension = "/v2/achievements/{}".format(id) if id is not None else "/v2/achievements"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Achievements_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/achievements_users.html"
        """
        extension = "/v2/achievements_users/{}".format(id) if id is not None else "/v2/achievements_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Announcements(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/announcements.html"
        """
        extension = "/v2/announcements/{}".format(id) if id is not None else "/v2/announcements"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Anti_grav_units(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/anti_grav_units.html"
        """
        extension = "/v2/anti_grav_units/{}".format(id) if id is not None else "/v2/anti_grav_units"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Anti_grav_units_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/anti_grav_units_users.html"
        """
        extension = "/v2/anti_grav_units_users/{}".format(id) if id is not None else "/v2/anti_grav_units_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Apps(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/apps.html"
        """
        extension = "/v2/apps/{}".format(id) if id is not None else "/v2/apps"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Attachments(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/attachments.html"
        """
        extension = "/v2/attachments/{}".format(id) if id is not None else "/v2/attachments"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Balances(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/balances.html"
        """
        extension = "/v2/balances/{}".format(id) if id is not None else "/v2/balances"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Bloc_deadlines(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/bloc_deadlines.html"
        """
        extension = "/v2/bloc_deadlines/{}".format(id) if id is not None else "/v2/bloc_deadlines"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Blocs(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/blocs.html"
        """
        extension = "/v2/blocs/{}".format(id) if id is not None else "/v2/blocs"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Campus(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/campus.html"
        """
        extension = "/v2/campus/{}".format(id) if id is not None else "/v2/campus"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Campus_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/campus_users.html"
        """
        extension = "/v2/campus_users/{}".format(id) if id is not None else "/v2/campus_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Certificates(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/certificates.html"
        """
        extension = "/v2/certificates/{}".format(id) if id is not None else "/v2/certificates"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Certificates_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/certificates_users.html"
        """
        extension = "/v2/certificates_users/{}".format(id) if id is not None else "/v2/certificates_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Closes(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/closes.html"
        """
        extension = "/v2/closes/{}".format(id) if id is not None else "/v2/closes"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Coalitions(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/coalitions.html"
        """
        extension = "/v2/coalitions/{}".format(id) if id is not None else "/v2/coalitions"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Coalitions_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/coalitions_users.html"
        """
        extension = "/v2/coalitions_users/{}".format(id) if id is not None else "/v2/coalitions_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Community_services(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/community_services.html"
        """
        extension = "/v2/community_services/{}".format(id) if id is not None else "/v2/community_services"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Companies(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/companies.html"
        """
        extension = "/v2/companies/{}".format(id) if id is not None else "/v2/companies"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Cursus(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/cursus.html"
        """
        extension = "/v2/cursus/{}".format(id) if id is not None else "/v2/cursus"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Cursus_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/cursus_users.html"
        """
        extension = "/v2/cursus_users/{}".format(id) if id is not None else "/v2/cursus_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Dashes(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/dashes.html"
        """
        extension = "/v2/dashes/{}".format(id) if id is not None else "/v2/dashes"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Dashes_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/dashes_users.html"
        """
        extension = "/v2/dashes_users/{}".format(id) if id is not None else "/v2/dashes_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Endpoints(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/endpoints.html"
        """
        extension = "/v2/endpoints/{}".format(id) if id is not None else "/v2/endpoints"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Evaluations(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/evaluations.html"
        """
        extension = "/v2/evaluations/{}".format(id) if id is not None else "/v2/evaluations"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Events(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/events.html"
        """
        extension = "/v2/events/{}".format(id) if id is not None else "/v2/events"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Events_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/events_users.html"
        """
        extension = "/v2/events_users/{}".format(id) if id is not None else "/v2/events_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Exams(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/exams.html"
        """
        extension = "/v2/exams/{}".format(id) if id is not None else "/v2/exams"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Experiences(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/experiences.html"
        """
        extension = "/v2/experiences/{}".format(id) if id is not None else "/v2/experiences"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Expertises(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/expertises.html"
        """
        extension = "/v2/expertises/{}".format(id) if id is not None else "/v2/expertises"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Expertises_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/expertises_users.html"
        """
        extension = "/v2/expertises_users/{}".format(id) if id is not None else "/v2/expertises_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Feedbacks(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/feedbacks.html"
        """
        extension = "/v2/feedbacks/{}".format(id) if id is not None else "/v2/feedbacks"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Flash_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/flash_users.html"
        """
        extension = "/v2/flash_users/{}".format(id) if id is not None else "/v2/flash_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Flashes(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/flashes.html"
        """
        extension = "/v2/flashes/{}".format(id) if id is not None else "/v2/flashes"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Groups(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/groups.html"
        """
        extension = "/v2/groups/{}".format(id) if id is not None else "/v2/groups"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Groups_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/groups_users.html"
        """
        extension = "/v2/groups_users/{}".format(id) if id is not None else "/v2/groups_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Internships(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/internships.html"
        """
        extension = "/v2/internships/{}".format(id) if id is not None else "/v2/internships"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Languages(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/languages.html"
        """
        extension = "/v2/languages/{}".format(id) if id is not None else "/v2/languages"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Languages_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/languages_users.html"
        """
        extension = "/v2/languages_users/{}".format(id) if id is not None else "/v2/languages_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Locations(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/locations.html"
        """
        extension = "/v2/locations/{}".format(id) if id is not None else "/v2/locations"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Mailings(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mailings.html"
        """
        extension = "/v2/mailings/{}".format(id) if id is not None else "/v2/mailings"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Notes(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/notes.html"
        """
        extension = "/v2/notes/{}".format(id) if id is not None else "/v2/notes"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Notions(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/notions.html"
        """
        extension = "/v2/notions/{}".format(id) if id is not None else "/v2/notions"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Offers(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/offers.html"
        """
        extension = "/v2/offers/{}".format(id) if id is not None else "/v2/offers"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Offers_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/offers_users.html"
        """
        extension = "/v2/offers_users/{}".format(id) if id is not None else "/v2/offers_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Params_project_sessions_rules(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/params_project_sessions_rules.html"
        """
        extension = "/v2/params_project_sessions_rules/{}".format(id) if id is not None else "/v2/params_project_sessions_rules"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Partnerships(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/partnerships.html"
        """
        extension = "/v2/partnerships/{}".format(id) if id is not None else "/v2/partnerships"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Partnerships_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/partnerships_users.html"
        """
        extension = "/v2/partnerships_users/{}".format(id) if id is not None else "/v2/partnerships_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Patronages(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/patronages.html"
        """
        extension = "/v2/patronages/{}".format(id) if id is not None else "/v2/patronages"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Patronages_reports(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/patronages_reports.html"
        """
        extension = "/v2/patronages_reports/{}".format(id) if id is not None else "/v2/patronages_reports"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Pools(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/pools.html"
        """
        extension = "/v2/pools/{}".format(id) if id is not None else "/v2/pools"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Products(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/products.html"
        """
        extension = "/v2/products/{}".format(id) if id is not None else "/v2/products"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_data(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/project_data.html"
        """
        extension = "/v2/project_data/{}".format(id) if id is not None else "/v2/project_data"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessions(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/project_sessions.html"
        """
        extension = "/v2/project_sessions/{}".format(id) if id is not None else "/v2/project_sessions"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessions_rules(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/project_sessions_rules.html"
        """
        extension = "/v2/project_sessions_rules/{}".format(id) if id is not None else "/v2/project_sessions_rules"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessions_skills(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/project_sessions_skills.html"
        """
        extension = "/v2/project_sessions_skills/{}".format(id) if id is not None else "/v2/project_sessions_skills"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Projects(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/projects.html"
        """
        extension = "/v2/projects/{}".format(id) if id is not None else "/v2/projects"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Projects_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/projects_users.html"
        """
        extension = "/v2/projects_users/{}".format(id) if id is not None else "/v2/projects_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Quests(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/quests.html"
        """
        extension = "/v2/quests/{}".format(id) if id is not None else "/v2/quests"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Quests_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/quests_users.html"
        """
        extension = "/v2/quests_users/{}".format(id) if id is not None else "/v2/quests_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Roles(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/roles.html"
        """
        extension = "/v2/roles/{}".format(id) if id is not None else "/v2/roles"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Roles_entities(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/roles_entities.html"
        """
        extension = "/v2/roles_entities/{}".format(id) if id is not None else "/v2/roles_entities"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Rules(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/rules.html"
        """
        extension = "/v2/rules/{}".format(id) if id is not None else "/v2/rules"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Scale_teams(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/scale_teams.html"
        """
        extension = "/v2/scale_teams/{}".format(id) if id is not None else "/v2/scale_teams"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Scales(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/scales.html"
        """
        extension = "/v2/scales/{}".format(id) if id is not None else "/v2/scales"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Scores(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/scores.html"
        """
        extension = "/v2/scores/{}".format(id) if id is not None else "/v2/scores"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Skills(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/skills.html"
        """
        extension = "/v2/skills/{}".format(id) if id is not None else "/v2/skills"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Slots(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/slots.html"
        """
        extension = "/v2/slots/{}".format(id) if id is not None else "/v2/slots"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Subnotions(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/subnotions.html"
        """
        extension = "/v2/subnotions/{}".format(id) if id is not None else "/v2/subnotions"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Tags(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/tags.html"
        """
        extension = "/v2/tags/{}".format(id) if id is not None else "/v2/tags"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Tags_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/tags_users.html"
        """
        extension = "/v2/tags_users/{}".format(id) if id is not None else "/v2/tags_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Teams(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/teams.html"
        """
        extension = "/v2/teams/{}".format(id) if id is not None else "/v2/teams"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Teams_uploads(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/teams_uploads.html"
        """
        extension = "/v2/teams_uploads/{}".format(id) if id is not None else "/v2/teams_uploads"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Teams_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/teams_users.html"
        """
        extension = "/v2/teams_users/{}".format(id) if id is not None else "/v2/teams_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Titles(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/titles.html"
        """
        extension = "/v2/titles/{}".format(id) if id is not None else "/v2/titles"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Titles_users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/titles_users.html"
        """
        extension = "/v2/titles_users/{}".format(id) if id is not None else "/v2/titles_users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Transactions(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/transactions.html"
        """
        extension = "/v2/transactions/{}".format(id) if id is not None else "/v2/transactions"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Translations(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/translations.html"
        """
        extension = "/v2/translations/{}".format(id) if id is not None else "/v2/translations"
        return HttpMethod(extension, self.session, **kwargs)
        
    def User_candidatures(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/user_candidatures.html"
        """
        extension = "/v2/user_candidatures/{}".format(id) if id is not None else "/v2/user_candidatures"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Users(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/users.html"
        """
        extension = "/v2/users/{}".format(id) if id is not None else "/v2/users"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Waitlists(self, id=None, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/waitlists.html"
        """
        extension = "/v2/waitlists/{}".format(id) if id is not None else "/v2/waitlists"
        return HttpMethod(extension, self.session, **kwargs)
        
    def AccreditationsUsers(self, accreditation_id, **kwargs):
        extension = "/v2/accreditations/{}/users".format(accreditation_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def AchievementsUsers(self, achievement_id, **kwargs):
        extension = "/v2/achievements/{}/users".format(achievement_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def AchievementsAchievements_users(self, achievement_id, **kwargs):
        extension = "/v2/achievements/{}/achievements_users".format(achievement_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def BlocsSquads(self, bloc_id, **kwargs):
        extension = "/v2/blocs/{}/squads".format(bloc_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def BlocsScores(self, bloc_id, **kwargs):
        extension = "/v2/blocs/{}/scores".format(bloc_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def BlocsScores(self, bloc_id, id, **kwargs):
        extension = "/v2/blocs/{}/scores/{}".format(bloc_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def BlocsCoalitions(self, bloc_id, **kwargs):
        extension = "/v2/blocs/{}/coalitions".format(bloc_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def BlocsSquads(self, bloc_id, id, **kwargs):
        extension = "/v2/blocs/{}/squads/{}".format(bloc_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def BlocsSquads_users(self, bloc_id, **kwargs):
        extension = "/v2/blocs/{}/squads_users".format(bloc_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def BlocsBloc_deadlines(self, bloc_id, **kwargs):
        extension = "/v2/blocs/{}/bloc_deadlines".format(bloc_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def BlocsSquads_users(self, bloc_id, id, **kwargs):
        extension = "/v2/blocs/{}/squads_users/{}".format(bloc_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusJournal(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/campusjournal.html"
        """
        extension = "/v2/campus/journal"
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusNotes(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/notes".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusUsers(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/users".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusExams(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/exams".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusStats(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/stats".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusQuests(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/quests".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusEvents(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/events".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusProducts(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/products".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusLocations(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/locations".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusBroadcasts(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/broadcasts".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusTags_users(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/tags_users".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusAchievements(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/achievements".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusProducts(self, campus_id, id, **kwargs):
        extension = "/v2/campus/{}/products/{}".format(campus_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusLocationsEnd_all(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/locations/end_all".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusAnti_grav_units_users(self, campus_id, **kwargs):
        extension = "/v2/campus/{}/anti_grav_units_users".format(campus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusCursusExams(self, campus_id, cursus_id, **kwargs):
        extension = "/v2/campus/{}/cursus/{}/exams".format(campus_id, cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusCursusEvents(self, campus_id, cursus_id, **kwargs):
        extension = "/v2/campus/{}/cursus/{}/events".format(campus_id, cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CampusProductsCommands(self, campus_id, product_id, **kwargs):
        extension = "/v2/campus/{}/products/{}/commands".format(campus_id, product_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CertificatesCertificates_users(self, certificate_id, **kwargs):
        extension = "/v2/certificates/{}/certificates_users".format(certificate_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ClosesClose(self, id, **kwargs):
        extension = "/v2/closes/{}/close".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ClosesUnclose(self, id, **kwargs):
        extension = "/v2/closes/{}/unclose".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ClosesCommunity_services(self, close_id, **kwargs):
        extension = "/v2/closes/{}/community_services".format(close_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CoalitionsUsers(self, coalition_id, **kwargs):
        extension = "/v2/coalitions/{}/users".format(coalition_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CoalitionsScores(self, coalition_id, **kwargs):
        extension = "/v2/coalitions/{}/scores".format(coalition_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CoalitionsScores(self, coalition_id, id, **kwargs):
        extension = "/v2/coalitions/{}/scores/{}".format(coalition_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CoalitionsCoalitions_users(self, coalition_id, **kwargs):
        extension = "/v2/coalitions/{}/coalitions_users".format(coalition_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Coalitions_usersScores(self, coalitions_user_id, **kwargs):
        extension = "/v2/coalitions_users/{}/scores".format(coalitions_user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Coalitions_usersScores(self, coalitions_user_id, id, **kwargs):
        extension = "/v2/coalitions_users/{}/scores/{}".format(coalitions_user_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Community_servicesValidate(self, id, **kwargs):
        extension = "/v2/community_services/{}/validate".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Community_servicesInvalidate(self, id, **kwargs):
        extension = "/v2/community_services/{}/invalidate".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CompaniesSubscribed_users(self, company_id, **kwargs):
        extension = "/v2/companies/{}/subscribed_users".format(company_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CompaniesInternships_users(self, company_id, **kwargs):
        extension = "/v2/companies/{}/internships_users".format(company_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusTags(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/tags".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusExams(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/exams".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusTeams(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/teams".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusUsers(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/users".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusQuests(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/quests".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusEvents(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/events".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusSkills(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/skills".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusLevels(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/levels".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusNotions(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/notions".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusProjects(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/projects".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusTags_users(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/tags_users".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusAchievements(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/achievements".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusCursus_users(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/cursus_users".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def CursusAnnouncements(self, cursus_id, **kwargs):
        extension = "/v2/cursus/{}/announcements".format(cursus_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def DashesUsers(self, dash_id, **kwargs):
        extension = "/v2/dashes/{}/users".format(dash_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def DashesDashes_users(self, dash_id, **kwargs):
        extension = "/v2/dashes/{}/dashes_users".format(dash_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def EventsUsers(self, event_id, **kwargs):
        extension = "/v2/events/{}/users".format(event_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def EventsWaitlist(self, event_id, **kwargs):
        extension = "/v2/events/{}/waitlist".format(event_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def EventsFeedbacks(self, event_id, **kwargs):
        extension = "/v2/events/{}/feedbacks".format(event_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def EventsEvents_users(self, event_id, **kwargs):
        extension = "/v2/events/{}/events_users".format(event_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def EventsFeedbacks(self, event_id, id, **kwargs):
        extension = "/v2/events/{}/feedbacks/{}".format(event_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ExamsWaitlist(self, exam_id, **kwargs):
        extension = "/v2/exams/{}/waitlist".format(exam_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ExamsExams_users(self, exam_id, **kwargs):
        extension = "/v2/exams/{}/exams_users".format(exam_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ExamsExams_users(self, exam_id, id, **kwargs):
        extension = "/v2/exams/{}/exams_users/{}".format(exam_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ExpertisesUsers(self, expertise_id, **kwargs):
        extension = "/v2/expertises/{}/users".format(expertise_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ExpertisesExpertises_users(self, expertise_id, **kwargs):
        extension = "/v2/expertises/{}/expertises_users".format(expertise_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Flags(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/flags.html"
        """
        extension = "/v2/flags"
        return HttpMethod(extension, self.session, **kwargs)
        
    def FlashesFlash_users(self, flash_id, **kwargs):
        extension = "/v2/flashes/{}/flash_users".format(flash_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def FlashesFlash_users(self, flash_id, id, **kwargs):
        extension = "/v2/flashes/{}/flash_users/{}".format(flash_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def GroupsUsers(self, group_id, **kwargs):
        extension = "/v2/groups/{}/users".format(group_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def GroupsGroups_users(self, group_id, **kwargs):
        extension = "/v2/groups/{}/groups_users".format(group_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def IssuesTags(self, issue_id, **kwargs):
        extension = "/v2/issues/{}/tags".format(issue_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Levels(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/levels.html"
        """
        extension = "/v2/levels"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Me(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/me.html"
        """
        extension = "/v2/me"
        return HttpMethod(extension, self.session, **kwargs)
        
    def MeSlots(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/meslots.html"
        """
        extension = "/v2/me/slots"
        return HttpMethod(extension, self.session, **kwargs)
        
    def MeTeams(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/meteams.html"
        """
        extension = "/v2/me/teams"
        return HttpMethod(extension, self.session, **kwargs)
        
    def MeProjects(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/meprojects.html"
        """
        extension = "/v2/me/projects"
        return HttpMethod(extension, self.session, **kwargs)
        
    def MeScale_teams(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mescale_teams.html"
        """
        extension = "/v2/me/scale_teams"
        return HttpMethod(extension, self.session, **kwargs)
        
    def MeScale_teamsAs_corrector(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mescale_teamsas_corrector.html"
        """
        extension = "/v2/me/scale_teams/as_corrector"
        return HttpMethod(extension, self.session, **kwargs)
        
    def MeScale_teamsAs_corrected(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/mescale_teamsas_corrected.html"
        """
        extension = "/v2/me/scale_teams/as_corrected"
        return HttpMethod(extension, self.session, **kwargs)
        
    def NotionsTags(self, notion_id, **kwargs):
        extension = "/v2/notions/{}/tags".format(notion_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def NotionsSubnotions(self, notion_id, **kwargs):
        extension = "/v2/notions/{}/subnotions".format(notion_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def OffersOffers_users(self, offer_id, **kwargs):
        extension = "/v2/offers/{}/offers_users".format(offer_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def PartnershipsUsers(self, partnership_id, **kwargs):
        extension = "/v2/partnerships/{}/users".format(partnership_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def PartnershipsPartnerships_users(self, partnership_id, **kwargs):
        extension = "/v2/partnerships/{}/partnerships_users".format(partnership_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Partnerships_usersExperiences(self, partnerships_user_id, **kwargs):
        extension = "/v2/partnerships_users/{}/experiences".format(partnerships_user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def PatronagesPatronages_reports(self, patronage_id, **kwargs):
        extension = "/v2/patronages/{}/patronages_reports".format(patronage_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def PoolsPointsAdd(self, id, **kwargs):
        extension = "/v2/pools/{}/points/add".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def PoolsPointsRemove(self, id, **kwargs):
        extension = "/v2/pools/{}/points/remove".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def PoolsBalances(self, pool_id, **kwargs):
        extension = "/v2/pools/{}/balances".format(pool_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def PoolsBalances(self, pool_id, id, **kwargs):
        extension = "/v2/pools/{}/balances/{}".format(pool_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProductsCommands(self, product_id, **kwargs):
        extension = "/v2/products/{}/commands".format(product_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessionsTeams(self, project_session_id, **kwargs):
        extension = "/v2/project_sessions/{}/teams".format(project_session_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessionsRules(self, project_session_id, **kwargs):
        extension = "/v2/project_sessions/{}/rules".format(project_session_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessionsScales(self, project_session_id, **kwargs):
        extension = "/v2/project_sessions/{}/scales".format(project_session_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessionsScale_teams(self, project_session_id, **kwargs):
        extension = "/v2/project_sessions/{}/scale_teams".format(project_session_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessionsAttachments(self, project_session_id, **kwargs):
        extension = "/v2/project_sessions/{}/attachments".format(project_session_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessionsProject_data(self, project_session_id, **kwargs):
        extension = "/v2/project_sessions/{}/project_data".format(project_session_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessionsScale_teams(self, project_session_id, id, **kwargs):
        extension = "/v2/project_sessions/{}/scale_teams/{}".format(project_session_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessionsAttachments(self, project_session_id, id, **kwargs):
        extension = "/v2/project_sessions/{}/attachments/{}".format(project_session_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessionsProject_sessions_rules(self, project_session_id, **kwargs):
        extension = "/v2/project_sessions/{}/project_sessions_rules".format(project_session_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessionsProject_sessions_skills(self, project_session_id, **kwargs):
        extension = "/v2/project_sessions/{}/project_sessions_skills".format(project_session_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessionsProject_sessions_skills(self, project_session_id, id, **kwargs):
        extension = "/v2/project_sessions/{}/project_sessions_skills/{}".format(project_session_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Project_sessions_rulesParams_project_sessions_rules(self, project_sessions_rule_id, **kwargs):
        extension = "/v2/project_sessions_rules/{}/params_project_sessions_rules".format(project_sessions_rule_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsRetry(self, id, **kwargs):
        extension = "/v2/projects/{}/retry".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsTags(self, project_id, **kwargs):
        extension = "/v2/projects/{}/tags".format(project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsUsers(self, project_id, **kwargs):
        extension = "/v2/projects/{}/users".format(project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsTeams(self, project_id, **kwargs):
        extension = "/v2/projects/{}/teams".format(project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsExams(self, project_id, **kwargs):
        extension = "/v2/projects/{}/exams".format(project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsSlots(self, project_id, **kwargs):
        extension = "/v2/projects/{}/slots".format(project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsScales(self, project_id, **kwargs):
        extension = "/v2/projects/{}/scales".format(project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsProjects(self, project_id, **kwargs):
        extension = "/v2/projects/{}/projects".format(project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsRegister(self, project_id, **kwargs):
        extension = "/v2/projects/{}/register".format(project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsScale_teams(self, project_id, **kwargs):
        extension = "/v2/projects/{}/scale_teams".format(project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsAttachments(self, project_id, **kwargs):
        extension = "/v2/projects/{}/attachments".format(project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsProjects_users(self, project_id, **kwargs):
        extension = "/v2/projects/{}/projects_users".format(project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ProjectsProject_sessions(self, project_id, **kwargs):
        extension = "/v2/projects/{}/project_sessions".format(project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Projects_usersRetry(self, id, **kwargs):
        extension = "/v2/projects_users/{}/retry".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Projects_usersCompile(self, id, **kwargs):
        extension = "/v2/projects_users/{}/compile".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Projects_usersExperiences(self, projects_user_id, **kwargs):
        extension = "/v2/projects_users/{}/experiences".format(projects_user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def QuestsUsers(self, quest_id, **kwargs):
        extension = "/v2/quests/{}/users".format(quest_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def QuestsQuests_users(self, quest_id, **kwargs):
        extension = "/v2/quests/{}/quests_users".format(quest_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def ReportsPatronages_reports(self, report_id, **kwargs):
        extension = "/v2/reports/{}/patronages_reports".format(report_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def RolesRoles_entities(self, role_id, **kwargs):
        extension = "/v2/roles/{}/roles_entities".format(role_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Scale_teamsMultiple_create(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/scale_teamsmultiple_create.html"
        """
        extension = "/v2/scale_teams/multiple_create"
        return HttpMethod(extension, self.session, **kwargs)
        
    def Scale_teamsFeedbacks(self, scale_team_id, **kwargs):
        extension = "/v2/scale_teams/{}/feedbacks".format(scale_team_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Scale_teamsFeedbacks(self, scale_team_id, id, **kwargs):
        extension = "/v2/scale_teams/{}/feedbacks/{}".format(scale_team_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def SkillsExperiences(self, skill_id, **kwargs):
        extension = "/v2/skills/{}/experiences".format(skill_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def SkillsProject_sessions_skills(self, skill_id, **kwargs):
        extension = "/v2/skills/{}/project_sessions_skills".format(skill_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Staff(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/staff.html"
        """
        extension = "/v2/staff"
        return HttpMethod(extension, self.session, **kwargs)
        
    def TagsNotions(self, tag_id, **kwargs):
        extension = "/v2/tags/{}/notions".format(tag_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def TagsTags_users(self, tag_id, **kwargs):
        extension = "/v2/tags/{}/tags_users".format(tag_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def TeamsUsers(self, team_id, **kwargs):
        extension = "/v2/teams/{}/users".format(team_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def TeamsTeams_users(self, team_id, **kwargs):
        extension = "/v2/teams/{}/teams_users".format(team_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def TeamsReset_team_uploads(self, id, **kwargs):
        extension = "/v2/teams/{}/reset_team_uploads".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def TeamsTeams_uploads(self, team_id, **kwargs):
        extension = "/v2/teams/{}/teams_uploads".format(team_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def Teams_uploadsMultiple_create(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/teams_uploadsmultiple_create.html"
        """
        extension = "/v2/teams_uploads/multiple_create"
        return HttpMethod(extension, self.session, **kwargs)
        
    def TitlesUsers(self, title_id, **kwargs):
        extension = "/v2/titles/{}/users".format(title_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def TitlesAchievements(self, title_id, **kwargs):
        extension = "/v2/titles/{}/achievements".format(title_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def TitlesTitles_users(self, title_id, **kwargs):
        extension = "/v2/titles/{}/titles_users".format(title_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def TranslationsUpload(self, **kwargs):
        """
        More details: "https://api.intra.42.fr/apidoc/2.0/translationsupload.html"
        """
        extension = "/v2/translations/upload"
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersExam(self, id, **kwargs):
        extension = "/v2/users/{}/exam".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersApps(self, user_id, **kwargs):
        extension = "/v2/users/{}/apps".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersTags(self, user_id, **kwargs):
        extension = "/v2/users/{}/tags".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersNotes(self, user_id, **kwargs):
        extension = "/v2/users/{}/notes".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersSlots(self, user_id, **kwargs):
        extension = "/v2/users/{}/slots".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersRoles(self, user_id, **kwargs):
        extension = "/v2/users/{}/roles".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersTeams(self, user_id, **kwargs):
        extension = "/v2/users/{}/teams".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersExams(self, user_id, **kwargs):
        extension = "/v2/users/{}/exams".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersTitles(self, user_id, **kwargs):
        extension = "/v2/users/{}/titles".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersCloses(self, user_id, **kwargs):
        extension = "/v2/users/{}/closes".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersScales(self, user_id, **kwargs):
        extension = "/v2/users/{}/scales".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersEvents(self, user_id, **kwargs):
        extension = "/v2/users/{}/events".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersGroups(self, user_id, **kwargs):
        extension = "/v2/users/{}/groups".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersQuests(self, user_id, **kwargs):
        extension = "/v2/users/{}/quests".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersUnfreeze(self, user_id, **kwargs):
        extension = "/v2/users/{}/unfreeze".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersMailings(self, user_id, **kwargs):
        extension = "/v2/users/{}/mailings".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersLocations(self, user_id, **kwargs):
        extension = "/v2/users/{}/locations".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersPatronages(self, user_id, **kwargs):
        extension = "/v2/users/{}/patronages".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersLocations_stats(self, id, **kwargs):
        extension = "/v2/users/{}/locations_stats".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersTags_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/tags_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersCoalitions(self, user_id, **kwargs):
        extension = "/v2/users/{}/coalitions".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersExperiences(self, user_id, **kwargs):
        extension = "/v2/users/{}/experiences".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersTeams_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/teams_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersScale_teams(self, user_id, **kwargs):
        extension = "/v2/users/{}/scale_teams".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersInternships(self, user_id, **kwargs):
        extension = "/v2/users/{}/internships".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersTitles_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/titles_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersGroups_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/groups_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersEvents_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/events_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersQuests_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/quests_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersCursus_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/cursus_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersTransactions(self, user_id, **kwargs):
        extension = "/v2/users/{}/transactions".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersCampus_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/campus_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersGitlab_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/gitlab_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersOffers_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/offers_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersFree_past_agu(self, user_id, **kwargs):
        extension = "/v2/users/{}/free_past_agu".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersLocations(self, user_id, id, **kwargs):
        extension = "/v2/users/{}/locations/{}".format(user_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersProjects_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/projects_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersInternships(self, user_id, id, **kwargs):
        extension = "/v2/users/{}/internships/{}".format(user_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersLanguages_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/languages_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersExpertises_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/expertises_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersCorrection_pointsAdd(self, id, **kwargs):
        extension = "/v2/users/{}/correction_points/add".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersUser_candidature(self, user_id, **kwargs):
        extension = "/v2/users/{}/user_candidature".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersCoalitions_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/coalitions_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersCertificates_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/certificates_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersPatronages_reports(self, user_id, **kwargs):
        extension = "/v2/users/{}/patronages_reports".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersCorrection_pointsRemove(self, id, **kwargs):
        extension = "/v2/users/{}/correction_points/remove".format(id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersLanguages_users(self, user_id, id, **kwargs):
        extension = "/v2/users/{}/languages_users/{}".format(user_id, id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersAnti_grav_units_users(self, user_id, **kwargs):
        extension = "/v2/users/{}/anti_grav_units_users".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersScale_teamsAs_corrector(self, user_id, **kwargs):
        extension = "/v2/users/{}/scale_teams/as_corrector".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersScale_teamsAs_corrected(self, user_id, **kwargs):
        extension = "/v2/users/{}/scale_teams/as_corrected".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersProjectsTeams(self, user_id, project_id, **kwargs):
        extension = "/v2/users/{}/projects/{}/teams".format(user_id, project_id)
        return HttpMethod(extension, self.session, **kwargs)
        
    def UsersCorrection_point_historics(self, user_id, **kwargs):
        extension = "/v2/users/{}/correction_point_historics".format(user_id)
        return HttpMethod(extension, self.session, **kwargs)
        