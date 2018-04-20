
import json

import hashlib \
 \
    # import lib.login1 as LL
import lib.login1 as LL
import common as CM


def getBaseStructure(zbotID):
    url = LL.BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    response = hit_url(RequestBody, headers1, LL.zbotID, url)
    with open('tmp', 'w') as f:
        f.write(str(response))
    return json.loads(response)


def method_url(body, headers, BASE_URL, method):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def getTagID(jsondata, details):
    try:
        for a in jsondata['data']['elements']:
            if 'basecard' in a['cardtype']:
                details[a['tagId']] = a['title']

            elif 'nextcard' in a['cardtype']:
                actionUrl = a['url']
                method = 'POST'
                body = json.loads(a['content'])
                body['pagesize'] = 5000
                jsondata = method_url(body, headers1, actionUrl, method)
                if jsondata == None:
                    return details
                else:
                    jsondata = json.loads(jsondata)
                #
                if jsondata == None:
                    return details
                else:
                    print len(details)
                    details = getTagID(jsondata, details)
    except KeyError:
        return details
    return details


if __name__ == '__main__':
    cardType = {}
    cardDetails = {}
    zbotID = LL.zbotID
    details = {}
    outfile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\indus_details.csv"
    # outfile = "/home/ec2-user/scripts/input_files/indus_details.csv"

    # timestamp = time.strftime("%d%m%Y_%H_%M_%S", time.localtime())
    # report = "tempfiles/userlist_" + timestamp
    #
    # reportfile = open (report, 'w')

    ### read the file structure into columns

    # i login
    headers, headers1 = LL.req_headers()

    # response = getBaseStructure(zbotID)
    # print response

    actionUrl = LL.BASE_URL + "zvice/interaction/" + zbotID
    method = "POST"
    responseBody = {'username': '', 'expired': 'false',
                    'interactionID': 'CommonInteraction_INTERACTION_TYPE_SEARCH_LIB_USER_PROFILE', "pagesize": 5000}

    jsondata = method_url(responseBody, headers1, actionUrl, method)
    print jsondata
    jsondata = json.loads(jsondata)

    details = getTagID(jsondata, details)
    # details = get_emailID(jsondata, details)

    print details

    with open(outfile, "w") as of:

        for k, v in details.items():
            # of.write("=============================================\n")
            of.write("\n" + k + ",")
            print k
            jdata = CM.getBaseStructure(k, headers1, LL.BASE_URL)
            for element in jdata['data']['elements']:
                if element['cardtype'] == "basecard":
                    of.write(CM.force_decode(element['title']) + ",")
                    # of.write(CM.force_decode(element['content']) + ",")
                    # of.write(CM.force_decode(element['contact']) + ",")
                elif element['title'] == "Contact Details":
                    url = element['cardsjsonurl']
                    body = json.loads(element['content'])
                    method = element['method']
                    contact = json.loads(CM.hit_url_method(body, headers1, method, url))
                    contact = contact['data']['elements'][0]['content'].split("<br>")
                    writecount = 0
                    for detail in contact:
                        if detail != "" or detail != None:
                            detail = CM.force_decode(detail)
                            of.write(detail + ",")
                            writecount += 1
                    if writecount == 0:
                        of.write(",,")
                    if writecount == 1:
                        of.write(",")

                    # print contact
                    print "contacts done"

                elif element['title'] == "More Details":
                    url = element['cardsjsonurl']
                    body = json.loads(element['content'])
                    method = element['method']
                    moreDetails = json.loads(CM.hit_url_method(body, headers1, method, url))
                    try:
                        for detail in moreDetails['data']['elements']:
                            of.write(CM.force_decode(detail['title']) + " : " + CM.force_decode(detail['content']) + ",")
                    except:
                        print "No more details fields"
                    print "more details done"
                    print "done"