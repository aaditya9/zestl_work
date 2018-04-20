import json
import logon as LL
import common as CM
import csv
import password as PP
# import function_combine as CC


SERVER = "https://twig.me/"
version = "v13/"
BASE_URL = SERVER + version

email = "admin@zestl.com"
pwd = PP.pwd
# pwd = "zsplADMIN999"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"
hasHeaders = True
with open(inputFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeaders:
        row1 = data.next()
    for row in data:
        # zviceID = row[0]
        # startDate = row[1]
        # ExpireDate = row[2]
        # fees = ""
        # status = row[3]
        # notes = 5
        # member_type = 6
        print "working for zvice id  :******** " + str(row[0])
        body = {}
        body['Title'] = CM.force_decode(row[4])
        body['Fees'] = ""
        body['StartDate'] = CM.force_decode(row[1])
        body['Expiry'] = CM.force_decode(row[2])
        body['Status'] = CM.force_decode(row[3])
        body['Notes'] = ""
        method = "POST"
        url = BASE_URL + "membership/user/" + CM.force_decode(row[0])
        response = CM.hit_url_method(body, headers1, method, url)
        print response

        # jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
        #
        # for a in jsondata['data']['elements']:
        #     title = "Memberships"
        #     if title in a['title']:
        #         print "Found"
        #         url = a['cardsjsonurl']
        #         method = "GET"
        #         body = {}
        #         body['genericCardType'] = "UserMemPlanCard"
        #         ja = CM.hit_url_method(body, headers1, method, url)
        #         print "Found 1st level"
        #
        #         for ac in json.loads(ja)['data']['elements']:
        #             if "textcard" in ac['cardtype']:
        #             # if "Membership Plans for Minal Thorat" in ac['title']:
        #                 print "2nd level"
        #                 for subac in ac['actions']:
        #                     if "Add New Membership Plan" in subac['title']:
        #                         print "found"
        #                         # d1 = row[startDate]
        #                         # d2 = row[ExpireDate]
        #                         # day = CC.days_between(d1,d2)
        #                         # print day
        #                         # member_type = CC.section(day)
        #                         # print member_type
        #
        #                         body = {}
        #                         body['Title'] = row[member_type]
        #                         # print body['Title']
        #                         body['Fees'] = row[fees]
        #                         body['StartDate'] = row[startDate]
        #                         body['Expiry'] = row[ExpireDate]
        #                         body['Status'] = row[status]
        #                         body['Notes'] = row[notes]
        #                         method = "POST"
        #                         url = subac['actionUrl']
        #                         response = CM.hit_url_method(body, headers1, method, url)
        #                         print response