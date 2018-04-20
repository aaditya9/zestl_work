import logon as LL
import common as CM
import csv
import password as PD
# SERVER = "https://future.twig.me/" #future prod
SERVER = "http://35.154.64.119/"    # test server
# SERVER ="https://twig.me/" ### Production Server
version = "v13/"
BASE_URL = SERVER + version
# zviceID = "B969YSR37AT7G"
zviceID = "A3S7NY7KCKLRC"

email = "admin@zestl.com"
# pwd = PD.pwd
pwd = "TwigMeNow"
hasHeader = "Y"
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
with open(inputFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    counter = 0
    for row in data:
        counter += 1
        print counter
        tag = row[0].strip()
        body = {}
        body['ActiveStatus'] = 'NO' # put 'NO' for deactivate the user
        method = "POST"
        url = BASE_URL + "org/" + zviceID + "/user/" + tag + "/activestatus"
        # url = "https://twig.me/v8/org/B969YSR37AT7G/user/" + tag + "/activestatus"
        jasub = CM.hit_url_method(body, headers1, method, url)
        print jasub