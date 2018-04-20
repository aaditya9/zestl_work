import logon as LL
import common as CM
import csv

SERVER = "http://35.154.20.82/"
version = "v8/"
BASE_URL = SERVER + version

zviceID = "3HRVUXXYAEA2Y"

email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

Label = 0
Name = 2
Type = 1
Visible = 3
Operator = 4
Leaf = 5

hasHeader = "Y"
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/Action_cust.csv"
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    title = "Lankesh Organisation"
    if title == a['title']:
        print "----"

        for sub in a['actions']:
            title = "Action Customization"
            arr = []
            if title == sub['title']:
                print "1----"

                with open(inputFile, 'r') as rf:
                    data = csv.reader(rf, delimiter=',')
                    if hasHeader == "Y":
                        row1 = data.next()
                    for row in data:

                        AcPref = {}
                        AcPref['label'] = row[Label]
                        AcPref['name'] = row[Name]
                        # AcPref['name'] = row
                        AcPref['type'] = row[Type]
                        AcPref['visible'] = str(row[Visible]).lower()
                        AcPref['operator'] = str(row[Operator]).lower()
                        AcPref['leaf'] = str(row[Leaf]).lower()
                        arr.append(AcPref)
                body = {}
                body['SetCardType'] = None
                body['CardID'] = None
                body['CardType'] = "ORG_BASE_CARD"
                body['ActionPref'] = arr
                url = sub['actionUrl']
                method = sub['method']
                print body
                jaction = CM.hit_url_method(body, headers1, method, url)
                print jaction