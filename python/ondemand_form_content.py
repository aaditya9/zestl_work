import json
import logon as LL
import common as CM
import re
import requests
import csv


SERVER = "http://35.154.177.221/"
version = "v8/"
BASE_URL = SERVER + version

zviceID = "3HN3XLHST9YZB"    ####  Business ID
# zviceID = "EFK3P7M69HQ36"

email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

formElementFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/Tree_planed_data.csv"
# title = "Grade 8 SUBJECT SELECTION FORM"
# desc = "Click new to submit"
hasHeader1 = "Y"


jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

for a in jsondata['data']['elements']:
    title = "Category 2: Criterion 6"
    if title == a['title']:
        print "present"
        # parentCardID = json.loads(a['ctjsondata'])['parentCardID']
        url = a['cturl']
        # url = "http://35.154.177.221/v8/genericcards/3HN3XLHST9YZB"
        body = json.loads(a['ctjsondata'])
        method = "POST"
        ja = CM.hit_url_method(body, headers1, method, url)
        print ja
        # cardid = a['cardID']
        # print cardid
        print "Found 1st level"

        for ac in json.loads(ja)['data']['elements']:
            if "Tree Planted Data" == ac['title']:
                print "2nd level"
                cardid = ac['cardID']
                print cardid

                for subac in ac['actions']:
                    title = "More actions"
                    if title in subac['title']:
                        print "3rd level"
                        body = {}
                        url = "http://35.154.177.221/v8/all_actions/3HN3XLHST9YZB/form/" + str(cardid)
                        # url = BASE_URL + "all_actions/" + card['zvice'][0] + "/form/" + str(cardID)
                        method = "GET"
                        jsonresponse = CM.hit_url_method(body, headers1, method, url)
                        print jsonresponse
                        for subac1 in json.loads(jsonresponse)['data']['ondemand_action']:
                            title = "Edit"
                            if title in subac1['title']:
                                print "-------"
                                url = subac1['actionUrl']
                                print url
                                print subac1['data']
                                data1 = json.loads(subac1['data'])
                                method = subac1["method"]
                                # print data1

                                body = {}
                                body["FormDescription"] = data1["FormDescription"]
                                body["FormID"] = data1["FormID"]
                                body["FormTitle"] = data1["FormTitle"]
                                print data1["FormTitle"]
                                body["ZviceID"] = data1["ZviceID"]
                                body["ZbotID"] = data1["ZbotID"]
                                body["ModifiedBy"] = data1["ModifiedBy"]
                                body["DateModified"] = data1["DateModified"]
                                body["CreatedBy"] = data1["CreatedBy"]
                                body["DateCreated"] = data1["DateCreated"]
                                body["query"] = data1["query"]
                                body["Flags"] = data1["Flags"]

                                zeroelem = {}
                                print data1['Elements']
                                passthrough = True
                                # if data['Elements'] == None:
                                if passthrough:
                                    tempAr = []
                                    zeroelem["ElementType"] = "SECTION"
                                    zeroelem["SequenceNo"] = 1
                                    zeroelem["FieldLabel"] = title
                                    elarray = []
                                    # print "222222222"

                                    with open(formElementFile, 'r') as my_file:
                                        data2 = csv.reader(my_file, delimiter=',')
                                        if hasHeader1 == "Y":
                                            row1 = data2.next()
                                        seqNo = 1
                                        for row in data2:

                                            elID = CM.force_decode(row[0])
                                            fldlabel = CM.force_decode(row[0])
                                            type = CM.force_decode(row[1])
                                            hint = CM.force_decode(row[2])
                                            req = CM.force_decode(row[3])
                                            seqNo += 1
                                            addElement = {}
                                            addElement['ElementID'] = elID
                                            addElement['ElementType'] = type
                                            addElement['FieldLabel'] = fldlabel
                                            addElement['Hint'] = hint
                                            addElement['Required'] = req
                                            addElement['SequenceNo'] = seqNo
                                            if type == "SPINNER" or type == "RADIO_GROUP":
                                                spinelements = row[4].split(";")
                                                addElement['Options'] = spinelements
                                            elarray.append(dict(addElement))

                                    zeroelem['Elements'] = elarray
                                    tempAr.append(dict(zeroelem))

                                body['Elements'] = tempAr

                                body['DataSource'] = data1['DataSource']

                                print body

                                jsonresponse = CM.hit_url_method(body, headers1, method, url)
                                print jsonresponse