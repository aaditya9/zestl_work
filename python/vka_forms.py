
import json
import csv
import logon as LL
import common as CM

SERVER = "https://twig.me/"
version = "v4/"
BASE_URL = SERVER + version

zviceID = "5VZ8JN4ZBFYHX"

email = "admin@zestl.com"
pwd = "Zspladmin99"

delfile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/delgrps.csv"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
tagids = []
for element in jsondata['data']['elements']:
    if element['cardtype'] == "basecard" and element['tagId'] != zviceID and element['tagId'] != "EF9PHJBFDZ2GA":
        tagids.append(element['tagId'])
    # print element['title'] + " : " + element['backgroundImageUrl']
print tagids

formElementFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/SiteVisitReport.csv"
title = "Site Visit Report"
hasHeader1 = "Y"

for tag in tagids:
    print tag
    jsondata = CM.getBaseStructure(tag, headers1, BASE_URL)
    for card in jsondata['data']['elements']:
        if "Progress" in card['title']:
            print card['ctjsondata']
            url = card['cturl']
            body = json.loads(card['ctjsondata'])
            method = "POST"
            jcards = CM.hit_url_method(body, headers1, method, url)
            # print jcards
            for element in json.loads(jcards)['data']['elements']:
                if title  in element['title']:
                    print element['title']

                    print title + " found"
                    print "============================"
                    for action in element['actions']:
                        print action
                        if 'More Actions' in action['title']:
                            for a in action['actions']:
                                if "Edit" in a['title']:
                                    url = a['actionUrl']
                                    data = json.loads(a['data'])
                                    method = a['method']
                                    print " &&&&&&&&&&&&&&&&&&&&&&& "
                                    body = {}

                                    body["FormDescription"] = data["FormDescription"]
                                    body["FormID"] = data["FormID"]

                                    body["FormTitle"] = data["FormTitle"]
                                    # body["ZviceID"]=  "CVEPKDHYA2FCS"
                                    body["ZviceID"] = data["ZviceID"]
                                    body["ZbotID"] = data["ZbotID"]
                                    body["ModifiedBy"] = data["ModifiedBy"]
                                    body["DateModified"] = data["DateModified"]
                                    body["CreatedBy"] = data["CreatedBy"]
                                    body["DateCreated"] = data["DateCreated"]
                                    body["query"] = data["query"]
                                    body["Flags"] = data["Flags"]
                                    zeroelem = {}
                                    print data['Elements']
                                    if data['Elements'] == None:
                                        tempAr = []
                                        zeroelem["ElementType"] = "SECTION"
                                        zeroelem["SequenceNo"] = 1
                                        zeroelem["FieldLabel"] = title
                                        elarray = []
                                        with open(formElementFile, 'r') as my_file:
                                            data1 = csv.reader(my_file, delimiter=',')
                                            if hasHeader1 == "Y":
                                                row1 = data1.next()
                                            seqNo = 1
                                            for row in data1:

                                                elID = row[0]
                                                fldlabel = row[0]
                                                type = row[1]
                                                hint = row[2]
                                                req = row[3]
                                                seqNo += 1
                                                addElement = {}
                                                addElement['ElementID'] = elID
                                                addElement['ElementType'] = type
                                                addElement['FieldLabel'] = fldlabel
                                                addElement['Hint'] = hint
                                                addElement['Required'] = req
                                                addElement['SequenceNo'] = seqNo
                                                if type == "SPINNER":
                                                    spinelements = row[4].split(";")
                                                    addElement['Options'] = spinelements
                                                elarray.append(dict(addElement))

                                        zeroelem['Elements'] = elarray
                                        tempAr.append(dict(zeroelem))


                                    body['Elements'] = tempAr

                                    body['DataSource'] = data['DataSource']

                                    print body

                                    jsonresponse = CM.hit_url_method(body, headers1, method, url)
                                    print " &&&&&&&&&&&&&&&&&&&&&&& "
                                    print jsonresponse
