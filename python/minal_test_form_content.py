import json
import logon as LL
import common as CM
import re
import requests
import csv

SERVER = "https://www.twig.me/"
version = "v8/"
BASE_URL = SERVER + version
zviceID = "9J5EDAR3Y2PZA"    ####  Business ID
email = "minal@zestl.com"
pwd = "minal123"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/radhika.csv"

hasHeader1 = "Y"

# User Group Info :--- Users in Group1#

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
url = "https://twig.me/v8/usergroups/9J5EDAR3Y2PZA" + "?filter={\"limit\":1000,\"offset\":0}"
method = "GET"
body = {}
jsonresponse = CM.hit_url_method(body, headers1, method, url)
print jsonresponse
for a in json.loads(jsonresponse)['data']['elements']:
    with open(inputFile, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        if hasHeader1 == "Y":
            row1 = data.next()
        for row in data:
            gname = row[0].strip()
            if gname == a['title']:
                print "*************** Working on this Group : " + gname + "  ******************"
                url = a['cardsjsonurl']
                method = a['method']
                body = {}
                jsonresponse = CM.hit_url_method(body, headers1, method, url)
                print jsonresponse
                for sub in json.loads(jsonresponse)['data']['elements']:
                    if "basecard" == sub['cardtype']:
                        print "present"
                        for subac in sub['actions']:
                            if "Remove User?" == subac['title']:
                                print "ready to delete"
                                body = {}
                                method = subac['method']
                                print method
                                url = subac['actionUrl']
                                print url
                                print "------------"
                                ja = CM.hit_url_method(body, headers1, method, url)
                                print ja

                    else: print "next level not present"




    #         parentCardID = json.loads(a['ctjsondata'])['parentCardID']
#         url = a['cturl']
#         body = json.loads(a['ctjsondata'])
#         method = "POST"
#         ja = CM.hit_url_method(body, headers1, method, url)
#         print "Found 1st level"

# for ac in jsondata['data']['elements']:
#     if "sayali form" in ac['title']:
#         print "2nd level"
#
#         for subac in ac['actions']:
#             title = "More Actions"
#             if title in subac['title']:
#                 print "3rd level"
#
#                 for subac1 in subac['actions']:
#                     title = "Edit"
#                     if title in subac1['title']:
#                         print "-------"
#
#                         url = subac1['actionUrl']
#                         print url
#                         print subac1['data']
#                         data1 = json.loads(subac1['data'])
#                         method = subac1["method"]
#                         # print data1
#
#                         body = {}
#                         body["FormDescription"] = data1["FormDescription"]
#                         body["FormID"] = data1["FormID"]
#                         body["FormTitle"] = data1["FormTitle"]
#                         print data1["FormTitle"]
#                         body["ZviceID"] = data1["ZviceID"]
#                         body["ZbotID"] = data1["ZbotID"]
#                         body["ModifiedBy"] = data1["ModifiedBy"]
#                         body["DateModified"] = data1["DateModified"]
#                         body["CreatedBy"] = data1["CreatedBy"]
#                         body["DateCreated"] = data1["DateCreated"]
#                         body["query"] = data1["query"]
#                         body["Flags"] = data1["Flags"]
#
#                         zeroelem = {}
#                         print data1['Elements']
#                         passthrough = True
#                         # if data['Elements'] == None:
#                         if passthrough:
#                             tempAr = []
#                             zeroelem["ElementType"] = "SECTION"
#                             zeroelem["SequenceNo"] = 1
#                             zeroelem["FieldLabel"] = title
#                             elarray = []
#                             # print "222222222"
#
#                             with open(formElementFile, 'r') as my_file:
#                                 data2 = csv.reader(my_file, delimiter=',')
#                                 if hasHeader1 == "Y":
#                                     row1 = data2.next()
#                                 seqNo = 1
#                                 for row in data2:
#
#                                     elID = CM.force_decode(row[0])
#                                     fldlabel = CM.force_decode(row[0])
#                                     type = CM.force_decode(row[1])
#                                     hint = CM.force_decode(row[2])
#                                     req = CM.force_decode(row[3])
#                                     seqNo += 1
#                                     addElement = {}
#                                     addElement['ElementID'] = elID
#                                     addElement['ElementType'] = type
#                                     addElement['FieldLabel'] = fldlabel
#                                     addElement['Hint'] = hint
#                                     addElement['Required'] = req
#                                     addElement['SequenceNo'] = seqNo
#                                     if type == "SPINNER" or type == "RADIO_GROUP":
#                                         spinelements = row[4].split(";")
#                                         addElement['Options'] = spinelements
#                                     elarray.append(dict(addElement))
#
#                             zeroelem['Elements'] = elarray
#                             tempAr.append(dict(zeroelem))
#
#                         body['Elements'] = tempAr
#
#                         body['DataSource'] = data1['DataSource']
#
#                         # print body
#                         #
#                         jsonresponse = CM.hit_url_method(body, headers1, method, url)
#                         # # print " &&&&&&&&&&&&&&&&&&&&&&& "
#                         # print jsonresponse
