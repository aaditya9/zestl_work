import logon as LL
import common as CM
import json
import csv

SERVER = "https://twig.me/"
version = "v8/"
BASE_URL = SERVER + version

hasHeader = "Y"
# zviceID = "EFK3P7M69HQ36"    #### test user id
outfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/mill_12th_UCG.csv"
email = "admin@zestl.com"
pwd = "Zspladmin99"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

# for a in jsondata['data']['elements']:
csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/more_view.csv"
with open (csvfile, 'r') as infile:
    data = csv.reader(infile, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    counter = 0
    for row in data:
        counter += 1
        print counter
        zviceID = CM.force_decode(row[0].strip())
        print "Working for this Zvice ID :- " + zviceID
        jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
        url = "https://twig.me/v8/all_actions/user/"+ zviceID
        method = "GET"
        body = {}
        ja = CM.hit_url_method(body, headers1, method, url)
        print ja

        url = "https://twig.me/v8/settings_action/user/" + zviceID
        method = "POST"
        body = {"cardType":"ORG_USER_CARD"}
        ja = CM.hit_url_method(body, headers1, method, url)
        print ja

        url = "https://twig.me/v8/user/communication/" + zviceID + "/groups"
        method = "GET"
        body ={}
        ja = CM.hit_url_method(body, headers1, method, url)
        print ja
        with open(outfile, 'a') as wf:
            wf.write("\n")
            wf.write(zviceID + ",")
            for a in json.loads(ja)['data']['elements']:
                if "mastercard" in a['cardtype']:
                    fa = []
                    title = a['title']
                    subtitle = a['content']
                    subtitle = subtitle.replace("," , ":")
                    fa.append(subtitle)
                    for item in fa:
                        wf.write(item + ',')
                    print title