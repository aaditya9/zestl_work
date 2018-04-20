import json
import logon as LL
import common as CM
import re
import requests
import csv


SERVER = "http://35.154.64.11/"
# SERVER = "https://www.twig.me/"
version = "v5/"
BASE_URL = SERVER + version

# zviceID = "876MD568TAUH2"    ####  Business ID
# zviceID = "EFK3P7M69HQ36"

email = "admin@zestl.com"
pwd = "TwigMeNow"
# pwd = "Zspladmin99"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

# formElementFile = "/home/ec2-user/scripts/input_files/sujoy/body_Measurements_form.csv"
# title = "Grade 8 SUBJECT SELECTION FORM"
# desc = "Click new to submit"
# zbotFile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/g_4_form.csv"
# zbotFile = "/home/ec2-user/scripts/input_files/sujoy/all_member_tags_wokout.csv"
formElementFile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/Monday_form.csv"
# title = "Grade 8 SUBJECT SELECTION FORM"
# desc = "Click new to submit"
zbotFile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/test.csv"
hasHeader1 = "Y"
hasHeaders = True



with open(zbotFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeaders:
        row1 = data.next()
    for row in data:
        zviceID = row[0]
        jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

        for a in jsondata['data']['elements']:
            title = "Body Analysis"
            if title in a['title']:
                parentCardID = json.loads(a['ctjsondata'])['parentCardID']
                url = a['cturl']
                body = json.loads(a['ctjsondata'])
                method = "POST"
                ja = CM.hit_url_method(body, headers1, method, url)
                print "Found 1st level"

                for ac in json.loads(ja)['data']['elements']:
                    if "Body Analysis" in ac['title']:
                        print "2nd level"

                        for subac in ac['actions']:
                            title = "More Actions"
                            if title in subac['title']:
                                print "3rd level"

                                for subac1 in subac['actions']:
                                    title = "Edit"
                                    if title in subac1['title']:
                                        print "-------"

                                        url = subac1['actionUrl']
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
                                        # print " &&&&&&&&&&&&&&&&&&&&&&& "
                                        print jsonresponse
