import logon as LL
import common as CM
import json
import auth as AA
import csv

# SERVER = "https://www.twig.me/"
SERVER = "http://twig-me.com/"
version = "v13/"
BASE_URL = SERVER + version
# zviceID = "83H6LVUBRXWZ5"    ####  Business ID
zviceID = "WHGJ7HTVTDFH3"   # Future grp dev
email = "admin@zestl.com"
pwd = "TwigMeNow"
# pwd = AA.pwd

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

formElementFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"

hasHeader1 = "Y"

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    title = "WFE Form Linking"
    if title == a['title']:
        print "1st level"
        for action in a['actions']:
            if 'More actions' in action['title']:
                body = {}
                url = action['actionUrl']
                print url
                # url = "https://twig.me/v7/all_actions/8SFKZCV5PFAXV/form/59"
                method = "GET"
                jsonresponse = CM.hit_url_method(body, headers1, method, url)
                print jsonresponse
                print "done"
                for sub in json.loads(jsonresponse)['data']['ondemand_action']:
                    if "Edit" in sub['title']:
                        url = sub['actionUrl']
                        data1 = sub['data']
                        print data1
                        data1 = json.loads(sub['data'])
                        method = sub['method']
                        print " &&&&&&&&&&&&&&&&&&&&&&& "
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

                        val = data1['Elements'][0]['Elements']  # This line is for taking existing elements from FORM #
                        # for elm in val:
                        #     if "SPINNER" in elm['ElementType']:
                        #         print "found"
                        #         spiner = elm['Options']
                        #         print spiner
                        print val
                        cc = len(val)
                        print cc
                        # for a in range(cc):     # if there are multiple elements present , then for each array remove the "ParentFormMetaID"
                        #     del val[a]["ParentFormMetaID"]
                        #     print val

                        passthrough = True
                        if passthrough:
                            tempAr = []
                            zeroelem["ElementType"] = "SECTION"
                            zeroelem["SequenceNo"] = 1
                            zeroelem["FieldLabel"] = title
                            print zeroelem["FieldLabel"]
                            elarray = []

                            with open(formElementFile, 'r') as my_file:
                                data2 = csv.reader(my_file, delimiter=',')
                                if hasHeader1 == "Y":
                                    row1 = data2.next()
                                seqNo = cc+1    #here we changed the sequence number beacause if there are already 2 elements are present then this sequence number should be differenet
                                for row in data2:

                                    elID = CM.force_decode(row[0].strip())
                                    fldlabel = CM.force_decode(row[0].strip())
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
                                    # elarray.append(dict(addElement))
                                    val.append(dict(addElement))    # here we are adding existing elemenets and new elements using function append
                                    # print elarray
                            zeroelem['Elements'] = val

                            tempAr.append(dict(zeroelem))

                        body['Elements'] = tempAr
                        print body['Elements']
                        body['DataSource'] = data1['DataSource']
                        print body
                        jsonresponse = CM.hit_url_method(body, headers1, method, url)
                        print jsonresponse