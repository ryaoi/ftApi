from Usefull import SetupFtApi

if __name__ == "__main__":
    ftApi = SetupFtApi()
    teamId = input("What is the team id? ")
    if not teamId.isdigit():
        print("give me a number!")
        exit(-1)
    teamData = ftApi.Teams(teamId).get()
    if teamData is {}:
        print("[-] Wrong teamId!")
        exit(-1)

    for index, elem in enumerate(teamData['scale_teams'], start=1):
        print("[{}] marked: {} by : {}".format(index, elem['final_mark'], elem['corrector']['login'], elem['final_mark']))

    scaleIndex = input("Which one do you want to delete? ")
    if not scaleIndex.isdigit():
        print("give me a number!")
        exit(-1)
    scaleIndex = int(scaleIndex)
    if scaleIndex < 0 or scaleIndex > len(teamData['scale_teams']):
        print("not in range !")
        exit(-1)

    scaleTeamsId = teamData['scale_teams'][scaleIndex]['id']
    print(scaleTeamsId)

    response = ftApi.Scale_teams(scaleTeamsId).delete()
    print(response)
