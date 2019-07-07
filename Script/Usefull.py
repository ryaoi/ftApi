from FtApi import *

def SetupFtApi():
    if 'UID42' not in os.environ or 'SECRET42' not in os.environ:
        print("please set UID42 and SECRET42")
        exit(-1)
    uid = os.environ['UID42']
    secret = os.environ['SECRET42']
    ftApi = FtApi(uid, secret)
    return ftApi
