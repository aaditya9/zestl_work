import logon as LL
import common as CM
import json

SERVER = "http://35.154.64.11/"
version = "v5/"
BASE_URL = SERVER + version
zviceID = "876MD568TAUH2"    ####  Business ID
email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    title = "test_case_form"
    if title == a['title']:
        print "1st level"
        for ac in a['actions']:
            title = "New"
            if title == ac['title']:
                print "found"
                body = {}
                body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_SHOW_FORM_SUBMISSIONS"
                body['formID'] = 1718
                body['categoryType'] = "FormCard"
                method = "GET"
                url = ac['actionUrl']
                jaction = CM.hit_url_method(body, headers1, method, url)
                print jaction

                for sub in json.loads(jaction)['data']['elements']:
                    title =  "test_case_form"
                    if title == sub['title']:
                        print "go ahead"
                        for ac in sub['actions']:
                            title = "Edit"
                            if title == ac['title']:
                                print "done"
                                data1 = json.loads(ac['data'])
                                body = {}
                                # body["FormDescription"] = data1["FormDescription"]
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
                                body["FieldLabel"] = "name"
                                body["ElementID"] = "name"
                                body["ElementType"] = "EDIT_TEXT"
                                # body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_SUBMIT_FORM"
                                # body['categorytype'] = "FormCard"
                                # body['FormSubmissionID'] = 1731
                                # body['FormID'] = 1718
                                # body['FormTitle'] = "test_case_form"
                                # body['ZviceID'] = "876MD568TAUH2"
                                # body['ZbotID'] = "876MD568TAUH2"
                                # body['ParentFormSubmissionID'] = ""
                                # body['IsHistory'] = "NO"
                                # body['SubmittedBy'] = "Zestl Admin"
                                body['STRING'] = "sayali"
                                # body['Flags'] = 1
                                # body['ParentFormMetaID'] = 710
                                method = "PUT"
                                url = ac['actionUrl']
                                print url
                                jaction1 = CM.hit_url_method(body, headers1, method, url)
                                print jaction1