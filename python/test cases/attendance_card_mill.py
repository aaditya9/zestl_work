import logon as LL
import common as CM
import auth as AA
import csv

SERVER = "https://twig.me/" #Production
version = "v11/"
BASE_URL = SERVER + version
zviceID = "9J5EDAR3Y2PZA"   #Millennium
# zviceID = "8SFKZCV5PFAXV"   #Minal

email = "admin@zestl.com"
pwd = AA.pwd
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
hasHeader = "Y"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

#*******************  This code is for creating new card **************
# url = "https://twig.me/v9/fastscan/attendance/8SFKZCV5PFAXV"
# method = "POST"
# body = {}
# body['Title'] = "check out"
# body['Description'] = "check out"
# body['ScanType'] = "FAST"
# # body['MembershipPlanID'] = None
# body['CheckInOut'] = "OUT"
# body['PassCode'] = "1111"
# body['remove'] = "false"
#
# jaction = CM.hit_url_method(body, headers1, method, url)
# print jaction
#*******************************************************************************

#*********************** This code is for editing new card ************

with open(inputFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    counter = 0
    for row in data:
        counter += 1
        print counter
        # url = BASE_URL + "BBH2SQEKPUGLW/fastscan/attendance/19142"
        url = BASE_URL + "BBH2SQEKPUGLW/fastscan/attendance/" + str(row[1])
        method = "PUT"
        body = {}
        body['Title'] = row[0].strip()
        # body['Title'] = "BR 12: OUT12"
        # body['Description'] = ""
        body['ScanType'] = "FAST"
        # body['MembershipPlanID'] = None
        body['CheckInOut'] = "OUT"
        body['PassCode'] = "1111"
        body['remove'] = "false"
        body['MatchFSCardIDs'] = [row[3].strip(),row[4].strip()]
        # body['MatchFSCardIDs'] = [19140,23380]
        # body['MatchFSCardIDs'] = [320,324]
        jaction = CM.hit_url_method(body, headers1, method, url)
        print jaction

#************************************************************************