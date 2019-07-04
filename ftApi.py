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


    def Accreditations(self, accreditation_id=None):
        extension = "/v2/accreditations/{}".format(accreditation_id) if accreditation_id is not None else "/v2/accreditations"
        return HttpMethod(extension, self.session)
        
    def Achievements(self, achievement_id=None):
        extension = "/v2/achievements/{}".format(achievement_id) if achievement_id is not None else "/v2/achievements"
        return HttpMethod(extension, self.session)
        
    def Achievements_users(self, id=None):
        extension = "/v2/achievements_users/{}".format(id) if id is not None else "/v2/achievements_users"
        return HttpMethod(extension, self.session)
        
    def Announcements(self, id=None):
        extension = "/v2/announcements/{}".format(id) if id is not None else "/v2/announcements"
        return HttpMethod(extension, self.session)
        
    def Apps(self, id=None):
        extension = "/v2/apps/{}".format(id) if id is not None else "/v2/apps"
        return HttpMethod(extension, self.session)
        
    def Attachments(self, id=None):
        extension = "/v2/attachments/{}".format(id) if id is not None else "/v2/attachments"
        return HttpMethod(extension, self.session)
        
    def Balances(self, id=None):
        extension = "/v2/balances/{}".format(id) if id is not None else "/v2/balances"
        return HttpMethod(extension, self.session)
        
    def Bloc_deadlines(self, id=None):
        extension = "/v2/bloc_deadlines/{}".format(id) if id is not None else "/v2/bloc_deadlines"
        return HttpMethod(extension, self.session)
        
    def Blocs(self, bloc_id=None):
        extension = "/v2/blocs/{}".format(bloc_id) if bloc_id is not None else "/v2/blocs"
        return HttpMethod(extension, self.session)
        
    def Campus(self, campus_id=None):
        extension = "/v2/campus/{}".format(campus_id) if campus_id is not None else "/v2/campus"
        return HttpMethod(extension, self.session)
        
    def Campus_users(self, id=None):
        extension = "/v2/campus_users/{}".format(id) if id is not None else "/v2/campus_users"
        return HttpMethod(extension, self.session)
        
    def Certificates(self, certificate_id=None):
        extension = "/v2/certificates/{}".format(certificate_id) if certificate_id is not None else "/v2/certificates"
        return HttpMethod(extension, self.session)
        
    def Certificates_users(self, id=None):
        extension = "/v2/certificates_users/{}".format(id) if id is not None else "/v2/certificates_users"
        return HttpMethod(extension, self.session)
        
    def Closes(self, close_id=None):
        extension = "/v2/closes/{}".format(close_id) if close_id is not None else "/v2/closes"
        return HttpMethod(extension, self.session)
        
    def Coalitions(self, coalition_id=None):
        extension = "/v2/coalitions/{}".format(coalition_id) if coalition_id is not None else "/v2/coalitions"
        return HttpMethod(extension, self.session)
        
    def Coalitions_users(self, coalitions_user_id=None):
        extension = "/v2/coalitions_users/{}".format(coalitions_user_id) if coalitions_user_id is not None else "/v2/coalitions_users"
        return HttpMethod(extension, self.session)
        
    def Community_services(self, id=None):
        extension = "/v2/community_services/{}".format(id) if id is not None else "/v2/community_services"
        return HttpMethod(extension, self.session)
        
    def Cursus(self, cursus_id=None):
        extension = "/v2/cursus/{}".format(cursus_id) if cursus_id is not None else "/v2/cursus"
        return HttpMethod(extension, self.session)
        
    def Cursus_topics(self, id=None):
        extension = "/v2/cursus_topics/{}".format(id) if id is not None else "/v2/cursus_topics"
        return HttpMethod(extension, self.session)
        
    def Cursus_users(self, id=None):
        extension = "/v2/cursus_users/{}".format(id) if id is not None else "/v2/cursus_users"
        return HttpMethod(extension, self.session)
        
    def Dashes(self, dash_id=None):
        extension = "/v2/dashes/{}".format(dash_id) if dash_id is not None else "/v2/dashes"
        return HttpMethod(extension, self.session)
        
    def Dashes_users(self, id=None):
        extension = "/v2/dashes_users/{}".format(id) if id is not None else "/v2/dashes_users"
        return HttpMethod(extension, self.session)
        
    def Endpoints(self, id=None):
        extension = "/v2/endpoints/{}".format(id) if id is not None else "/v2/endpoints"
        return HttpMethod(extension, self.session)
        
    def Evaluations(self, id=None):
        extension = "/v2/evaluations/{}".format(id) if id is not None else "/v2/evaluations"
        return HttpMethod(extension, self.session)
        
    def Events(self, event_id=None):
        extension = "/v2/events/{}".format(event_id) if event_id is not None else "/v2/events"
        return HttpMethod(extension, self.session)
        
    def Events_users(self, id=None):
        extension = "/v2/events_users/{}".format(id) if id is not None else "/v2/events_users"
        return HttpMethod(extension, self.session)
        
    def Exams(self, exam_id=None):
        extension = "/v2/exams/{}".format(exam_id) if exam_id is not None else "/v2/exams"
        return HttpMethod(extension, self.session)
        
    def Experiences(self, id=None):
        extension = "/v2/experiences/{}".format(id) if id is not None else "/v2/experiences"
        return HttpMethod(extension, self.session)
        
    def Expertises(self, expertise_id=None):
        extension = "/v2/expertises/{}".format(expertise_id) if expertise_id is not None else "/v2/expertises"
        return HttpMethod(extension, self.session)
        
    def Expertises_users(self, id=None):
        extension = "/v2/expertises_users/{}".format(id) if id is not None else "/v2/expertises_users"
        return HttpMethod(extension, self.session)
        
    def Feedbacks(self, id=None):
        extension = "/v2/feedbacks/{}".format(id) if id is not None else "/v2/feedbacks"
        return HttpMethod(extension, self.session)
        
    def Flash_users(self, id=None):
        extension = "/v2/flash_users/{}".format(id) if id is not None else "/v2/flash_users"
        return HttpMethod(extension, self.session)
        
    def Flashes(self, flash_id=None):
        extension = "/v2/flashes/{}".format(flash_id) if flash_id is not None else "/v2/flashes"
        return HttpMethod(extension, self.session)
        
    def Groups(self, group_id=None):
        extension = "/v2/groups/{}".format(group_id) if group_id is not None else "/v2/groups"
        return HttpMethod(extension, self.session)
        
    def Groups_users(self, id=None):
        extension = "/v2/groups_users/{}".format(id) if id is not None else "/v2/groups_users"
        return HttpMethod(extension, self.session)
        
    def Internships(self, id=None):
        extension = "/v2/internships/{}".format(id) if id is not None else "/v2/internships"
        return HttpMethod(extension, self.session)
        
    def Languages(self, id=None):
        extension = "/v2/languages/{}".format(id) if id is not None else "/v2/languages"
        return HttpMethod(extension, self.session)
        
    def Languages_users(self, id=None):
        extension = "/v2/languages_users/{}".format(id) if id is not None else "/v2/languages_users"
        return HttpMethod(extension, self.session)
        
    def Locations(self, id=None):
        extension = "/v2/locations/{}".format(id) if id is not None else "/v2/locations"
        return HttpMethod(extension, self.session)
        
    def Mailings(self, id=None):
        extension = "/v2/mailings/{}".format(id) if id is not None else "/v2/mailings"
        return HttpMethod(extension, self.session)
        
    def MeMessages(self, message_id=None):
        extension = "/v2/me/messages/{}".format(message_id) if message_id is not None else "/v2/me/messages"
        return HttpMethod(extension, self.session)
        
    def MeTopics(self, topic_id=None):
        extension = "/v2/me/topics/{}".format(topic_id) if topic_id is not None else "/v2/me/topics"
        return HttpMethod(extension, self.session)
        
    def Messages(self, id=None):
        extension = "/v2/messages/{}".format(id) if id is not None else "/v2/messages"
        return HttpMethod(extension, self.session)
        
    def Notes(self, id=None):
        extension = "/v2/notes/{}".format(id) if id is not None else "/v2/notes"
        return HttpMethod(extension, self.session)
        
    def Notions(self, id=None):
        extension = "/v2/notions/{}".format(id) if id is not None else "/v2/notions"
        return HttpMethod(extension, self.session)
        
    def Params_project_sessions_rules(self, id=None):
        extension = "/v2/params_project_sessions_rules/{}".format(id) if id is not None else "/v2/params_project_sessions_rules"
        return HttpMethod(extension, self.session)
        
    def Partnerships(self, id=None):
        extension = "/v2/partnerships/{}".format(id) if id is not None else "/v2/partnerships"
        return HttpMethod(extension, self.session)
        
    def Partnerships_users(self, id=None):
        extension = "/v2/partnerships_users/{}".format(id) if id is not None else "/v2/partnerships_users"
        return HttpMethod(extension, self.session)
        
    def Patronages(self, id=None):
        extension = "/v2/patronages/{}".format(id) if id is not None else "/v2/patronages"
        return HttpMethod(extension, self.session)
        
    def Patronages_reports(self, id=None):
        extension = "/v2/patronages_reports/{}".format(id) if id is not None else "/v2/patronages_reports"
        return HttpMethod(extension, self.session)
        
    def Pools(self, id=None):
        extension = "/v2/pools/{}".format(id) if id is not None else "/v2/pools"
        return HttpMethod(extension, self.session)
        
    def Products(self, id=None):
        extension = "/v2/products/{}".format(id) if id is not None else "/v2/products"
        return HttpMethod(extension, self.session)
        
    def Project_data(self, id=None):
        extension = "/v2/project_data/{}".format(id) if id is not None else "/v2/project_data"
        return HttpMethod(extension, self.session)
        
    def Project_sessions(self, id=None):
        extension = "/v2/project_sessions/{}".format(id) if id is not None else "/v2/project_sessions"
        return HttpMethod(extension, self.session)
        
    def Project_sessions_rules(self, id=None):
        extension = "/v2/project_sessions_rules/{}".format(id) if id is not None else "/v2/project_sessions_rules"
        return HttpMethod(extension, self.session)
        
    def Projects(self, id=None):
        extension = "/v2/projects/{}".format(id) if id is not None else "/v2/projects"
        return HttpMethod(extension, self.session)
        
    def Projects_users(self, id=None):
        extension = "/v2/projects_users/{}".format(id) if id is not None else "/v2/projects_users"
        return HttpMethod(extension, self.session)
        
    def Quests(self, id=None):
        extension = "/v2/quests/{}".format(id) if id is not None else "/v2/quests"
        return HttpMethod(extension, self.session)
        
    def Quests_users(self, id=None):
        extension = "/v2/quests_users/{}".format(id) if id is not None else "/v2/quests_users"
        return HttpMethod(extension, self.session)
        
    def Roles(self, id=None):
        extension = "/v2/roles/{}".format(id) if id is not None else "/v2/roles"
        return HttpMethod(extension, self.session)
        
    def Roles_entities(self, id=None):
        extension = "/v2/roles_entities/{}".format(id) if id is not None else "/v2/roles_entities"
        return HttpMethod(extension, self.session)
        
    def Rules(self, id=None):
        extension = "/v2/rules/{}".format(id) if id is not None else "/v2/rules"
        return HttpMethod(extension, self.session)
        
    def Scale_teams(self, id=None):
        extension = "/v2/scale_teams/{}".format(id) if id is not None else "/v2/scale_teams"
        return HttpMethod(extension, self.session)
        
    def Scales(self, id=None):
        extension = "/v2/scales/{}".format(id) if id is not None else "/v2/scales"
        return HttpMethod(extension, self.session)
        
    def Scores(self, id=None):
        extension = "/v2/scores/{}".format(id) if id is not None else "/v2/scores"
        return HttpMethod(extension, self.session)
        
    def Skills(self, id=None):
        extension = "/v2/skills/{}".format(id) if id is not None else "/v2/skills"
        return HttpMethod(extension, self.session)
        
    def Slots(self, id=None):
        extension = "/v2/slots/{}".format(id) if id is not None else "/v2/slots"
        return HttpMethod(extension, self.session)
        
    def Subnotions(self, id=None):
        extension = "/v2/subnotions/{}".format(id) if id is not None else "/v2/subnotions"
        return HttpMethod(extension, self.session)
        
    def Tags(self, id=None):
        extension = "/v2/tags/{}".format(id) if id is not None else "/v2/tags"
        return HttpMethod(extension, self.session)
        
    def Teams(self, id=None):
        extension = "/v2/teams/{}".format(id) if id is not None else "/v2/teams"
        return HttpMethod(extension, self.session)
        
    def Teams_uploads(self, id=None):
        extension = "/v2/teams_uploads/{}".format(id) if id is not None else "/v2/teams_uploads"
        return HttpMethod(extension, self.session)
        
    def Teams_users(self, id=None):
        extension = "/v2/teams_users/{}".format(id) if id is not None else "/v2/teams_users"
        return HttpMethod(extension, self.session)
        
    def Titles(self, id=None):
        extension = "/v2/titles/{}".format(id) if id is not None else "/v2/titles"
        return HttpMethod(extension, self.session)
        
    def Titles_users(self, id=None):
        extension = "/v2/titles_users/{}".format(id) if id is not None else "/v2/titles_users"
        return HttpMethod(extension, self.session)
        
    def Topics(self, id=None):
        extension = "/v2/topics/{}".format(id) if id is not None else "/v2/topics"
        return HttpMethod(extension, self.session)
        
    def Transactions(self, id=None):
        extension = "/v2/transactions/{}".format(id) if id is not None else "/v2/transactions"
        return HttpMethod(extension, self.session)
        
    def Translations(self, id=None):
        extension = "/v2/translations/{}".format(id) if id is not None else "/v2/translations"
        return HttpMethod(extension, self.session)
        
    def User_candidatures(self, id=None):
        extension = "/v2/user_candidatures/{}".format(id) if id is not None else "/v2/user_candidatures"
        return HttpMethod(extension, self.session)
        
    def Users(self, id=None):
        extension = "/v2/users/{}".format(id) if id is not None else "/v2/users"
        return HttpMethod(extension, self.session)
        
    def Votes(self, id=None):
        extension = "/v2/votes/{}".format(id) if id is not None else "/v2/votes"
        return HttpMethod(extension, self.session)
        
    def Waitlists(self, id=None):
        extension = "/v2/waitlists/{}".format(id) if id is not None else "/v2/waitlists"
        return HttpMethod(extension, self.session)
        
    def Accreditations(self, id):
        extension = "/v2/accreditations/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def AchievementsUsers(self, achievement_id):
        extension = "/v2/achievements/{}/users".format(achievement_id)
        return HttpMethod(extension, self.session)
        
    def Achievements(self, id):
        extension = "/v2/achievements/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def BlocsCoalitions(self, bloc_id):
        extension = "/v2/blocs/{}/coalitions".format(bloc_id)
        return HttpMethod(extension, self.session)
        
    def BlocsScores(self, bloc_id):
        extension = "/v2/blocs/{}/scores".format(bloc_id)
        return HttpMethod(extension, self.session)
        
    def BlocsScores(self, bloc_id, id):
        extension = "/v2/blocs/{}/scores/{}".format(bloc_id, id)
        return HttpMethod(extension, self.session)
        
    def Blocs(self, id):
        extension = "/v2/blocs/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def CampusCursusEvents(self, campus_id, cursus_id):
        extension = "/v2/campus/{}/cursus/{}/events".format(campus_id, cursus_id)
        return HttpMethod(extension, self.session)
        
    def CampusCursusExams(self, campus_id, cursus_id):
        extension = "/v2/campus/{}/cursus/{}/exams".format(campus_id, cursus_id)
        return HttpMethod(extension, self.session)
        
    def CampusEvents(self, campus_id):
        extension = "/v2/campus/{}/events".format(campus_id)
        return HttpMethod(extension, self.session)
        
    def CampusExams(self, campus_id):
        extension = "/v2/campus/{}/exams".format(campus_id)
        return HttpMethod(extension, self.session)
        
    def CampusLocations(self, campus_id):
        extension = "/v2/campus/{}/locations".format(campus_id)
        return HttpMethod(extension, self.session)
        
    def CampusLocationsEnd_all(self, campus_id):
        extension = "/v2/campus/{}/locations/end_all".format(campus_id)
        return HttpMethod(extension, self.session)
        
    def CampusNotes(self, campus_id):
        extension = "/v2/campus/{}/notes".format(campus_id)
        return HttpMethod(extension, self.session)
        
    def CampusProducts(self, campus_id):
        extension = "/v2/campus/{}/products".format(campus_id)
        return HttpMethod(extension, self.session)
        
    def CampusProducts(self, campus_id, id):
        extension = "/v2/campus/{}/products/{}".format(campus_id, id)
        return HttpMethod(extension, self.session)
        
    def CampusQuests(self, campus_id):
        extension = "/v2/campus/{}/quests".format(campus_id)
        return HttpMethod(extension, self.session)
        
    def CampusUsers(self, campus_id):
        extension = "/v2/campus/{}/users".format(campus_id)
        return HttpMethod(extension, self.session)
        
    def Campus(self, id):
        extension = "/v2/campus/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def Certificates(self, id):
        extension = "/v2/certificates/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def Closes(self, id):
        extension = "/v2/closes/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def ClosesUnclose(self, id):
        extension = "/v2/closes/{}/unclose".format(id)
        return HttpMethod(extension, self.session)
        
    def CoalitionsScores(self, coalition_id):
        extension = "/v2/coalitions/{}/scores".format(coalition_id)
        return HttpMethod(extension, self.session)
        
    def CoalitionsScores(self, coalition_id, id):
        extension = "/v2/coalitions/{}/scores/{}".format(coalition_id, id)
        return HttpMethod(extension, self.session)
        
    def CoalitionsUsers(self, coalition_id):
        extension = "/v2/coalitions/{}/users".format(coalition_id)
        return HttpMethod(extension, self.session)
        
    def Coalitions(self, id):
        extension = "/v2/coalitions/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def Coalitions_usersScores(self, coalitions_user_id, id):
        extension = "/v2/coalitions_users/{}/scores/{}".format(coalitions_user_id, id)
        return HttpMethod(extension, self.session)
        
    def Coalitions_users(self, id):
        extension = "/v2/coalitions_users/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def Community_servicesInvalidate(self, id):
        extension = "/v2/community_services/{}/invalidate".format(id)
        return HttpMethod(extension, self.session)
        
    def Community_servicesValidate(self, id):
        extension = "/v2/community_services/{}/validate".format(id)
        return HttpMethod(extension, self.session)
        
    def CursusAnnouncements(self, cursus_id):
        extension = "/v2/cursus/{}/announcements".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusCursus_topics(self, cursus_id):
        extension = "/v2/cursus/{}/cursus_topics".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusCursus_users(self, cursus_id):
        extension = "/v2/cursus/{}/cursus_users".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusEvents(self, cursus_id):
        extension = "/v2/cursus/{}/events".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusExams(self, cursus_id):
        extension = "/v2/cursus/{}/exams".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusLevels(self, cursus_id):
        extension = "/v2/cursus/{}/levels".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusNotions(self, cursus_id):
        extension = "/v2/cursus/{}/notions".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusProjects(self, cursus_id):
        extension = "/v2/cursus/{}/projects".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusQuests(self, cursus_id):
        extension = "/v2/cursus/{}/quests".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusSkills(self, cursus_id):
        extension = "/v2/cursus/{}/skills".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusTags(self, cursus_id):
        extension = "/v2/cursus/{}/tags".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusTeams(self, cursus_id):
        extension = "/v2/cursus/{}/teams".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusTopics(self, cursus_id):
        extension = "/v2/cursus/{}/topics".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def CursusUsers(self, cursus_id):
        extension = "/v2/cursus/{}/users".format(cursus_id)
        return HttpMethod(extension, self.session)
        
    def Cursus(self, id):
        extension = "/v2/cursus/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def DashesUsers(self, dash_id):
        extension = "/v2/dashes/{}/users".format(dash_id)
        return HttpMethod(extension, self.session)
        
    def Dashes(self, id):
        extension = "/v2/dashes/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def EventsFeedbacks(self, event_id):
        extension = "/v2/events/{}/feedbacks".format(event_id)
        return HttpMethod(extension, self.session)
        
    def EventsFeedbacks(self, event_id, id):
        extension = "/v2/events/{}/feedbacks/{}".format(event_id, id)
        return HttpMethod(extension, self.session)
        
    def EventsUsers(self, event_id):
        extension = "/v2/events/{}/users".format(event_id)
        return HttpMethod(extension, self.session)
        
    def EventsWaitlist(self, event_id):
        extension = "/v2/events/{}/waitlist".format(event_id)
        return HttpMethod(extension, self.session)
        
    def Events(self, id):
        extension = "/v2/events/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def ExamsExams_users(self, exam_id, id):
        extension = "/v2/exams/{}/exams_users/{}".format(exam_id, id)
        return HttpMethod(extension, self.session)
        
    def ExamsWaitlist(self, exam_id):
        extension = "/v2/exams/{}/waitlist".format(exam_id)
        return HttpMethod(extension, self.session)
        
    def Exams(self, id):
        extension = "/v2/exams/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def ExpertisesUsers(self, expertise_id):
        extension = "/v2/expertises/{}/users".format(expertise_id)
        return HttpMethod(extension, self.session)
        
    def Expertises(self, id):
        extension = "/v2/expertises/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def FlashesFlash_users(self, flash_id, id):
        extension = "/v2/flashes/{}/flash_users/{}".format(flash_id, id)
        return HttpMethod(extension, self.session)
        
    def Flashes(self, id):
        extension = "/v2/flashes/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def GroupsUsers(self, group_id):
        extension = "/v2/groups/{}/users".format(group_id)
        return HttpMethod(extension, self.session)
        
    def Groups(self, id):
        extension = "/v2/groups/{}".format(id)
        return HttpMethod(extension, self.session)
        
    def IssuesTags(self, issue_id):
        extension = "/v2/issues/{}/tags".format(issue_id)
        return HttpMethod(extension, self.session)
        
    def Levels(self):
        extension = "/v2/levels"
        return HttpMethod(extension, self.session)
        
    def Me(self):
        extension = "/v2/me"
        return HttpMethod(extension, self.session)
        
    def MeMessagesVotesDownvotes(self, message_id):
        extension = "/v2/me/messages/{}/votes/downvotes".format(message_id)
        return HttpMethod(extension, self.session)
        
    def MeMessagesVotesProblems(self, message_id):
        extension = "/v2/me/messages/{}/votes/problems".format(message_id)
        return HttpMethod(extension, self.session)
        
    def MeMessagesVotesTrollvotes(self, message_id):
        extension = "/v2/me/messages/{}/votes/trollvotes".format(message_id)
        return HttpMethod(extension, self.session)
        
    def MeMessagesVotesUpvotes(self, message_id):
        extension = "/v2/me/messages/{}/votes/upvotes".format(message_id)
        return HttpMethod(extension, self.session)
        
    def MeProjects(self):
        extension = "/v2/me/projects"
        return HttpMethod(extension, self.session)
        
    def MeScale_teams(self):
        extension = "/v2/me/scale_teams"
        return HttpMethod(extension, self.session)
        
    def MeScale_teamsAs_corrected(self):
        extension = "/v2/me/scale_teams/as_corrected"
        return HttpMethod(extension, self.session)
        
    def MeScale_teamsAs_corrector(self):
        extension = "/v2/me/scale_teams/as_corrector"
        return HttpMethod(extension, self.session)
        
    def MeSlots(self):
        extension = "/v2/me/slots"
        return HttpMethod(extension, self.session)
        
    def MeTeams(self):
        extension = "/v2/me/teams"
        return HttpMethod(extension, self.session)
        
    def MeTopicsVotesDownvotes(self, topic_id):
        extension = "/v2/me/topics/{}/votes/downvotes".format(topic_id)
        return HttpMethod(extension, self.session)
        
    def MeTopicsVotesProblems(self, topic_id):
        extension = "/v2/me/topics/{}/votes/problems".format(topic_id)
        return HttpMethod(extension, self.session)
        
    def MeTopicsVotesTrollvotes(self, topic_id):
        extension = "/v2/me/topics/{}/votes/trollvotes".format(topic_id)
        return HttpMethod(extension, self.session)
        
    def MeTopicsVotesUpvotes(self, topic_id):
        extension = "/v2/me/topics/{}/votes/upvotes".format(topic_id)
        return HttpMethod(extension, self.session)
        
    def MeVotes(self):
        extension = "/v2/me/votes"
        return HttpMethod(extension, self.session)
        
    def MeVotesDownvotes(self):
        extension = "/v2/me/votes/downvotes"
        return HttpMethod(extension, self.session)
        
    def MeVotesProblems(self):
        extension = "/v2/me/votes/problems"
        return HttpMethod(extension, self.session)
        
    def MeVotesTrollvotes(self):
        extension = "/v2/me/votes/trollvotes"
        return HttpMethod(extension, self.session)
        
    def MeVotesUpvotes(self):
        extension = "/v2/me/votes/upvotes"
        return HttpMethod(extension, self.session)
        
    def MessagesMessages(self, message_id):
        extension = "/v2/messages/{}/messages".format(message_id)
        return HttpMethod(extension, self.session)
        
    def MessagesVotes(self, message_id):
        extension = "/v2/messages/{}/votes".format(message_id)
        return HttpMethod(extension, self.session)
        
    def MessagesVotesDownvotes(self, message_id):
        extension = "/v2/messages/{}/votes/downvotes".format(message_id)
        return HttpMethod(extension, self.session)
        
    def MessagesVotesProblems(self, message_id):
        extension = "/v2/messages/{}/votes/problems".format(message_id)
        return HttpMethod(extension, self.session)
        
    def MessagesVotesTrollvotes(self, message_id):
        extension = "/v2/messages/{}/votes/trollvotes".format(message_id)
        return HttpMethod(extension, self.session)
        
    def MessagesVotesUpvotes(self, message_id):
        extension = "/v2/messages/{}/votes/upvotes".format(message_id)
        return HttpMethod(extension, self.session)
        
    def NotionsSubnotions(self, notion_id):
        extension = "/v2/notions/{}/subnotions".format(notion_id)
        return HttpMethod(extension, self.session)
        
    def NotionsTags(self, notion_id):
        extension = "/v2/notions/{}/tags".format(notion_id)
        return HttpMethod(extension, self.session)
        
    def PartnershipsPartnerships_users(self, partnership_id):
        extension = "/v2/partnerships/{}/partnerships_users".format(partnership_id)
        return HttpMethod(extension, self.session)
        
    def PartnershipsUsers(self, partnership_id):
        extension = "/v2/partnerships/{}/users".format(partnership_id)
        return HttpMethod(extension, self.session)
        
    def Partnerships_usersExperiences(self, partnerships_user_id):
        extension = "/v2/partnerships_users/{}/experiences".format(partnerships_user_id)
        return HttpMethod(extension, self.session)
        
    def PatronagesPatronages_reports(self, patronage_id):
        extension = "/v2/patronages/{}/patronages_reports".format(patronage_id)
        return HttpMethod(extension, self.session)
        
    def PoolsBalances(self, pool_id):
        extension = "/v2/pools/{}/balances".format(pool_id)
        return HttpMethod(extension, self.session)
        
    def PoolsBalances(self, pool_id, id):
        extension = "/v2/pools/{}/balances/{}".format(pool_id, id)
        return HttpMethod(extension, self.session)
        
    def Project_sessionsEvaluations(self, project_session_id):
        extension = "/v2/project_sessions/{}/evaluations".format(project_session_id)
        return HttpMethod(extension, self.session)
        
    def Project_sessionsProject_data(self, project_session_id):
        extension = "/v2/project_sessions/{}/project_data".format(project_session_id)
        return HttpMethod(extension, self.session)
        
    def Project_sessionsProject_sessions_rules(self, project_session_id):
        extension = "/v2/project_sessions/{}/project_sessions_rules".format(project_session_id)
        return HttpMethod(extension, self.session)
        
    def Project_sessionsRules(self, project_session_id):
        extension = "/v2/project_sessions/{}/rules".format(project_session_id)
        return HttpMethod(extension, self.session)
        
    def Project_sessionsScales(self, project_session_id):
        extension = "/v2/project_sessions/{}/scales".format(project_session_id)
        return HttpMethod(extension, self.session)
        
    def Project_sessionsTeams(self, project_session_id):
        extension = "/v2/project_sessions/{}/teams".format(project_session_id)
        return HttpMethod(extension, self.session)
        
    def Project_sessions_rulesParams_project_sessions_rules(self, project_sessions_rule_id):
        extension = "/v2/project_sessions_rules/{}/params_project_sessions_rules".format(project_sessions_rule_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsRetry(self, id):
        extension = "/v2/projects/{}/retry".format(id)
        return HttpMethod(extension, self.session)
        
    def ProjectsAttachments(self, project_id):
        extension = "/v2/projects/{}/attachments".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsEvaluations(self, project_id):
        extension = "/v2/projects/{}/evaluations".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsExams(self, project_id):
        extension = "/v2/projects/{}/exams".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsProject_sessions(self, project_id):
        extension = "/v2/projects/{}/project_sessions".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsProjects(self, project_id):
        extension = "/v2/projects/{}/projects".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsProjects_users(self, project_id):
        extension = "/v2/projects/{}/projects_users".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsRegister(self, project_id):
        extension = "/v2/projects/{}/register".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsScale_teams(self, project_id):
        extension = "/v2/projects/{}/scale_teams".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsScales(self, project_id):
        extension = "/v2/projects/{}/scales".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsSkills(self, project_id):
        extension = "/v2/projects/{}/skills".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsSlots(self, project_id):
        extension = "/v2/projects/{}/slots".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsTags(self, project_id):
        extension = "/v2/projects/{}/tags".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsTeams(self, project_id):
        extension = "/v2/projects/{}/teams".format(project_id)
        return HttpMethod(extension, self.session)
        
    def ProjectsUsers(self, project_id):
        extension = "/v2/projects/{}/users".format(project_id)
        return HttpMethod(extension, self.session)
        
    def Projects_usersRetry(self, id):
        extension = "/v2/projects_users/{}/retry".format(id)
        return HttpMethod(extension, self.session)
        
    def Projects_usersExperiences(self, projects_user_id):
        extension = "/v2/projects_users/{}/experiences".format(projects_user_id)
        return HttpMethod(extension, self.session)
        
    def QuestsQuests_users(self, quest_id):
        extension = "/v2/quests/{}/quests_users".format(quest_id)
        return HttpMethod(extension, self.session)
        
    def QuestsUsers(self, quest_id):
        extension = "/v2/quests/{}/users".format(quest_id)
        return HttpMethod(extension, self.session)
        
    def ReportsPatronages_reports(self, report_id):
        extension = "/v2/reports/{}/patronages_reports".format(report_id)
        return HttpMethod(extension, self.session)
        
    def RolesRoles_entities(self, role_id):
        extension = "/v2/roles/{}/roles_entities".format(role_id)
        return HttpMethod(extension, self.session)
        
    def Scale_teamsFeedbacks(self, scale_team_id):
        extension = "/v2/scale_teams/{}/feedbacks".format(scale_team_id)
        return HttpMethod(extension, self.session)
        
    def Scale_teamsFeedbacks(self, scale_team_id, id):
        extension = "/v2/scale_teams/{}/feedbacks/{}".format(scale_team_id, id)
        return HttpMethod(extension, self.session)
        
    def Scale_teamsMultiple_create(self):
        extension = "/v2/scale_teams/multiple_create"
        return HttpMethod(extension, self.session)
        
    def SkillsExperiences(self, skill_id):
        extension = "/v2/skills/{}/experiences".format(skill_id)
        return HttpMethod(extension, self.session)
        
    def TagsNotions(self, tag_id):
        extension = "/v2/tags/{}/notions".format(tag_id)
        return HttpMethod(extension, self.session)
        
    def TagsTopics(self, tag_id):
        extension = "/v2/tags/{}/topics".format(tag_id)
        return HttpMethod(extension, self.session)
        
    def TeamsTeams_uploads(self, team_id):
        extension = "/v2/teams/{}/teams_uploads".format(team_id)
        return HttpMethod(extension, self.session)
        
    def TeamsTeams_users(self, team_id):
        extension = "/v2/teams/{}/teams_users".format(team_id)
        return HttpMethod(extension, self.session)
        
    def TeamsUsers(self, team_id):
        extension = "/v2/teams/{}/users".format(team_id)
        return HttpMethod(extension, self.session)
        
    def Teams_uploadsMultiple_create(self):
        extension = "/v2/teams_uploads/multiple_create"
        return HttpMethod(extension, self.session)
        
    def TitlesAchievements(self, title_id):
        extension = "/v2/titles/{}/achievements".format(title_id)
        return HttpMethod(extension, self.session)
        
    def TitlesTitles_users(self, title_id):
        extension = "/v2/titles/{}/titles_users".format(title_id)
        return HttpMethod(extension, self.session)
        
    def TitlesUsers(self, title_id):
        extension = "/v2/titles/{}/users".format(title_id)
        return HttpMethod(extension, self.session)
        
    def TopicsCursus_topics(self, topic_id):
        extension = "/v2/topics/{}/cursus_topics".format(topic_id)
        return HttpMethod(extension, self.session)
        
    def TopicsMessages(self, topic_id):
        extension = "/v2/topics/{}/messages".format(topic_id)
        return HttpMethod(extension, self.session)
        
    def TopicsMessagesMessages(self, topic_id, message_id):
        extension = "/v2/topics/{}/messages/{}/messages".format(topic_id, message_id)
        return HttpMethod(extension, self.session)
        
    def TopicsTags(self, topic_id):
        extension = "/v2/topics/{}/tags".format(topic_id)
        return HttpMethod(extension, self.session)
        
    def TopicsVotes(self, topic_id):
        extension = "/v2/topics/{}/votes".format(topic_id)
        return HttpMethod(extension, self.session)
        
    def TopicsVotesDownvotes(self, topic_id):
        extension = "/v2/topics/{}/votes/downvotes".format(topic_id)
        return HttpMethod(extension, self.session)
        
    def TopicsVotesProblems(self, topic_id):
        extension = "/v2/topics/{}/votes/problems".format(topic_id)
        return HttpMethod(extension, self.session)
        
    def TopicsVotesTrollvotes(self, topic_id):
        extension = "/v2/topics/{}/votes/trollvotes".format(topic_id)
        return HttpMethod(extension, self.session)
        
    def TopicsVotesUpvotes(self, topic_id):
        extension = "/v2/topics/{}/votes/upvotes".format(topic_id)
        return HttpMethod(extension, self.session)
        
    def TopicsUnread(self):
        extension = "/v2/topics/unread"
        return HttpMethod(extension, self.session)
        
    def TranslationsUpload(self):
        extension = "/v2/translations/upload"
        return HttpMethod(extension, self.session)
        
    def UsersCorrection_pointsAdd(self, id):
        extension = "/v2/users/{}/correction_points/add".format(id)
        return HttpMethod(extension, self.session)
        
    def UsersCorrection_pointsRemove(self, id):
        extension = "/v2/users/{}/correction_points/remove".format(id)
        return HttpMethod(extension, self.session)
        
    def UsersExam(self, id):
        extension = "/v2/users/{}/exam".format(id)
        return HttpMethod(extension, self.session)
        
    def UsersApps(self, user_id):
        extension = "/v2/users/{}/apps".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersCampus_users(self, user_id):
        extension = "/v2/users/{}/campus_users".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersCertificates_users(self, user_id):
        extension = "/v2/users/{}/certificates_users".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersCloses(self, user_id):
        extension = "/v2/users/{}/closes".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersCoalitions(self, user_id):
        extension = "/v2/users/{}/coalitions".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersCoalitions_users(self, user_id):
        extension = "/v2/users/{}/coalitions_users".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersCursus_users(self, user_id):
        extension = "/v2/users/{}/cursus_users".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersEvents(self, user_id):
        extension = "/v2/users/{}/events".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersEvents_users(self, user_id):
        extension = "/v2/users/{}/events_users".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersExams(self, user_id):
        extension = "/v2/users/{}/exams".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersExperiences(self, user_id):
        extension = "/v2/users/{}/experiences".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersExpertises_users(self, user_id):
        extension = "/v2/users/{}/expertises_users".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersGroups(self, user_id):
        extension = "/v2/users/{}/groups".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersGroups_users(self, user_id):
        extension = "/v2/users/{}/groups_users".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersInternships(self, user_id):
        extension = "/v2/users/{}/internships".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersInternships(self, user_id, id):
        extension = "/v2/users/{}/internships/{}".format(user_id, id)
        return HttpMethod(extension, self.session)
        
    def UsersLanguages_users(self, user_id):
        extension = "/v2/users/{}/languages_users".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersLanguages_users(self, user_id, id):
        extension = "/v2/users/{}/languages_users/{}".format(user_id, id)
        return HttpMethod(extension, self.session)
        
    def UsersLocations(self, user_id):
        extension = "/v2/users/{}/locations".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersLocations(self, user_id, id):
        extension = "/v2/users/{}/locations/{}".format(user_id, id)
        return HttpMethod(extension, self.session)
        
    def UsersMailings(self, user_id):
        extension = "/v2/users/{}/mailings".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersMessages(self, user_id):
        extension = "/v2/users/{}/messages".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersNotes(self, user_id):
        extension = "/v2/users/{}/notes".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersPatronages(self, user_id):
        extension = "/v2/users/{}/patronages".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersPatronages_reports(self, user_id):
        extension = "/v2/users/{}/patronages_reports".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersProjectsTeams(self, user_id, project_id):
        extension = "/v2/users/{}/projects/{}/teams".format(user_id, project_id)
        return HttpMethod(extension, self.session)
        
    def UsersProjects_users(self, user_id):
        extension = "/v2/users/{}/projects_users".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersQuests(self, user_id):
        extension = "/v2/users/{}/quests".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersQuests_users(self, user_id):
        extension = "/v2/users/{}/quests_users".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersRoles(self, user_id):
        extension = "/v2/users/{}/roles".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersScale_teams(self, user_id):
        extension = "/v2/users/{}/scale_teams".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersScale_teamsAs_corrected(self, user_id):
        extension = "/v2/users/{}/scale_teams/as_corrected".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersScale_teamsAs_corrector(self, user_id):
        extension = "/v2/users/{}/scale_teams/as_corrector".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersScales(self, user_id):
        extension = "/v2/users/{}/scales".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersSlots(self, user_id):
        extension = "/v2/users/{}/slots".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersTags(self, user_id):
        extension = "/v2/users/{}/tags".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersTeams(self, user_id):
        extension = "/v2/users/{}/teams".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersTeams_users(self, user_id):
        extension = "/v2/users/{}/teams_users".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersTitles(self, user_id):
        extension = "/v2/users/{}/titles".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersTitles_users(self, user_id):
        extension = "/v2/users/{}/titles_users".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersTopics(self, user_id):
        extension = "/v2/users/{}/topics".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersTransactions(self, user_id):
        extension = "/v2/users/{}/transactions".format(user_id)
        return HttpMethod(extension, self.session)
        
    def UsersUser_candidature(self, user_id):
        extension = "/v2/users/{}/user_candidature".format(user_id)
        return HttpMethod(extension, self.session)
        
    def VotesDownvotes(self):
        extension = "/v2/votes/downvotes"
        return HttpMethod(extension, self.session)
        
    def VotesProblems(self):
        extension = "/v2/votes/problems"
        return HttpMethod(extension, self.session)
        
    def VotesTrollvotes(self):
        extension = "/v2/votes/trollvotes"
        return HttpMethod(extension, self.session)
        
    def VotesUpvotes(self):
        extension = "/v2/votes/upvotes"
        return HttpMethod(extension, self.session)


import pprint

if __name__ == "__main__":
    uid = os.environ["UID42"]
    secret = os.environ["SECRET42"]
    ftApi = FtApi(uid, secret)
    dump = ftApi.Users("ryaoi").get()
    pprint.pprint(dump)
