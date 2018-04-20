import logon as LL
import common as CM
import password as PP
import csv

SERVER = "https://twig.me/" #Production
version = "v8/"
BASE_URL = SERVER + version

zviceID = "9J5EDAR3Y2PZA"
email = "admin@zestl.com"
# pwd = "TwigMeNow"
pwd = PP.pwd
hasHeader = "Y"
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
# jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

with open(inputFile, 'r') as rf:

    data = csv.reader(rf, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    counter = 0
    for row in data:
        body = {}
        body['LTCardID'] = row[1]
        body['UserIDListOld'] = None
        body['UserIDList'] = row[0] # put users zvice id
        method = "POST"
        url = "https://twig.me/v8/lt/" + zviceID + "/users/add/" + row[1]
        jasub = CM.hit_url_method(body, headers1, method, url)
        print jasub