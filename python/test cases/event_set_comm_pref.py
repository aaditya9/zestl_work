
import json
import csv
import urllib2
import hashlib\

import lib.login1 as LL
import common as CM

def getAllUserGroups(headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('GET', BASE_URL + 'usergroups/' + zbotID + "?filter={\"limit\":1000,\"offset\":0}", None, headers)
    return jsondata['reply']

def change_view_permissions_fullurl(body, headers, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL , json.dumps(body), headers)
    return jsondata['reply']

def set_card_permissions(allowedusers, cardID, zviceID, acttype, headers1):
    BASE_URL = "https://twig.me/v8/"
    usergroups = getAllUserGroups(headers1, zviceID, BASE_URL)
    grplist = json.loads(usergroups)['output']['usergroup']
    try:
        grpID = grplist[allowedusers]
        print grpID
        actionType = acttype
        RequestBody = {
                       "opType": "1",
                       "actionType": actionType,
                       "groupID": grpID,
                       "cardID": str(cardID),
                       "cardType": "GenericCard"
                       }
        url = BASE_URL + 'card/permissions/' + zviceID
        response = change_view_permissions_fullurl(RequestBody, headers1, url)
    except:
        response = "Could not change permision " + acttype + " : " + allowedusers
    return response


if __name__ == '__main__':
    # log in of course
    headers, headers1 = LL.req_headers()
    errorFile = "saptpadi_UCG.txt"

    inputfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"

    hasHeader = 'Y'

    zviceID = '8SFKZCV5PFAXV'
    cardname = "Cal_shripad"
    decurl = "http://twig.me/v1/push/dectest/" + zviceID
    response = urllib2.urlopen(decurl)
    html = response.read()
    decTag = json.loads(html)['decTagID']

    jsondata = CM.getBaseStructure(zviceID, headers1, LL.BASE_URL)

    for card in jsondata['data']['elements']:
        if cardname == card['title']:
            url =  card['actions'][0]['actionUrl']
            method = card['actions'][0]['method']
            body = {}
            jasub = CM.hit_url_method(body, headers1, method, url)
            for sub in json.loads(jasub)['data']['elements']:
                if sub['title'] == "Meeting with HoDs & New Teachers":
                    url = sub['cturl']
                    method = sub['ctmethod']
                    body = {}
                    jasub = CM.hit_url_method(body, headers1, method, url)
                    cid = json.loads(jasub)['data']['elements'][0]['ctjsondata']
                    cid = json.loads(cid)
                    cid = cid['parentCardID']
                    grpname = "Aaa"
                    result = set_card_permissions(grpname, cid, zviceID, "MAIL", headers1)
                    print result


                    # for subT in json.loads(jasub)['data']['elements'][0]['actions']:
                    #     if subT['title'] == "More actions":
                    #         url = subT['actionUrl']
                    #         method = subT['method']
                    #         body = {}
                    #         jasub = CM.hit_url_method(body, headers1, method, url)
                    #         for per in json.loads(jasub)['data']['ondemand_action']:
                    #             if per['title'] == "User Permission Settings":
                    #                 url = per['actionUrl']
                    #                 method = per['method']
                    #                 body = {"cardType" : "EVENT"}
                    #                 jasub = CM.hit_url_method(body, headers1, method, url)
                    #                 for comm in json.loads(jasub)['data']['ondemand_action']:
                    #                     if comm['title'] == "Communication Preferences":
                    #                         body = {}
                    #                         data = json.loads(comm['data'])
                    #                         url = comm['actionUrl']
                    #                         method = comm['method']
                    #                         body['cardType'] = data['cardType']
                    #                         body['cardID'] = data['cardID']
                    #                         jasub = CM.hit_url_method(body, headers1, method, url)
                    #                         url = json.loads(jasub)['data']['elements'][1]['cardsjsonurl']
                    #                         method = json.loads(jasub)['data']['elements'][1]['method']
                    #                         content = json.loads(jasub)['data']['elements'][1]['content']
                    #                         content = json.loads(content)
                    #                         body = {}
                    #                         body['cardType'] = content['cardType']
                    #                         body['cardID'] = content['cardID']
                    #                         body['actionType'] = content['actionType']
                    #                         jasub = CM.hit_url_method(body, headers1, method, url)
                    #                         print jasub