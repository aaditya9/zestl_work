import json
import logon as LL
import common as CM
import sys
import re
import csv
import requests
import time

def create_form(Form_Name,business_id):
    method = "POST"
    r = requests.get("http://twig.me/v1/push/dectest/" + business_id)
    tagnum = r.json()['decTagID']
    r = requests.get("http://twig.me/v1/push/dectest/" + business_id)
    zbotnum = r.json()['decTagID']
    body = {"FormID": "", "FormDescription": Form_Name, "FormTitle": Form_Name,
            "ZviceID": tagnum, "ZbotID": zbotnum, "LinkType": "FORM", "LinkID": "",
            "parentCardID": None}
    url = BASE_URL + business_id + "/forms"
    jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
    return jsondata


def form_content(form_card_id,business_id,Form_Name,csvFile,outputFile):
    method = "GET"
    url = BASE_URL + business_id + "/forms/" + str(form_card_id)
    body = {}
    j1 = json.loads(CM.hit_url_method(body, headers1, method, url))
    for element in j1['data']['elements']:
        if Form_Name in element['title']:
            for action in element['actions']:
                if 'More actions' in action['title']:
                    body = {}
                    url = BASE_URL + "all_actions/" + business_id + "/form/" + str(form_card_id)
                    method = "GET"
                    jsonresponse = CM.hit_url_method(body, headers1, method, url)
                    for a in json.loads(jsonresponse)['data']['ondemand_action']:
                        if "Edit" in a['title']:
                            url = a['actionUrl']
                            data = json.loads(a['data'])
                            method = a['method']
                            body = {}
                            body["FormDescription"] = data["FormDescription"]
                            body["FormID"] = data["FormID"]
                            body["FormTitle"] = data["FormTitle"]
                            body["ZviceID"] = data["ZviceID"]
                            body["ZbotID"] = data["ZbotID"]
                            body["ModifiedBy"] = data["ModifiedBy"]
                            body["DateModified"] = data["DateModified"]
                            body["CreatedBy"] = data["CreatedBy"]
                            body["DateCreated"] = data["DateCreated"]
                            body["query"] = data["query"]
                            body["Flags"] = data["Flags"]
                            zeroelem = {}
                            passthrough = True
                            if passthrough:
                                tempAr = []
                                zeroelem["ElementType"] = "SECTION"
                                zeroelem["SequenceNo"] = 1
                                zeroelem["FieldLabel"] = Form_Name
                                elarray = []
                                seqNo = 1
                                with open(csvFile, 'r') as my_file:
                                    data1 = csv.reader(my_file, delimiter=',')
                                    seqNo = 1
                                    for row in data1:

                                        elID = CM.force_decode(row[0])
                                        fldlabel = CM.force_decode(row[0])
                                        type = CM.force_decode(row[1])
                                        hint = ""
                                        req = 1
                                        seqNo += 1
                                        addElement = {}
                                        addElement['ElementID'] = elID
                                        addElement['ElementType'] = type
                                        addElement['FieldLabel'] = fldlabel
                                        addElement['Hint'] = hint
                                        addElement['Required'] = req
                                        addElement['SequenceNo'] = seqNo

                                        temp_list = []
                                        temp_options = []
                                        if type == "TEMP_ADMIN_LIST":
                                            with open(outputFile, 'r') as my_temp_list:
                                                data2 = csv.reader(my_temp_list, delimiter=',')
                                                for row in data2:
                                                    a = {"MapKey": row[1],
                                                         "MapValue": [
                                                             {"title": row[1], "subtitle": "User", "id": row[0],
                                                              "type": "USER"}]}
                                                    temp_list.append(a)
                                                    temp_options.append(row[1])
                                        addElement['Options'] = temp_options
                                        addElement['MetaData'] = {"TempAdminList": temp_list}
                                        elarray.append(dict(addElement))
                                zeroelem['Elements'] = elarray
                                tempAr.append(dict(zeroelem))
                            body['Elements'] = tempAr
                            body['DataSource'] = data['DataSource']
                            # print body
                            jsonresponse = CM.hit_url_method(body, headers1, method, url)
                            print jsonresponse


#**********************   Code for add new users **************
def add_user(business_id,u_name,u_email):
    method = "POST"
    url = BASE_URL + 'zvice/interaction/' + business_id
    body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat', 'long': 'long', 'tagprofile': 0,
            'media_type': 'image/jpg',
            'media_ext': 'jpg', 'media': "", 'media_size': 0, 'zbotid': business_id}
    body['title'] = u_name
    body['linkemail'] = u_email
    body['autogentag'] = "true"
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"
    jsonreply = CM.hit_url_method(body, headers1, method, url)
    return jsonreply



#***********************************************************
def invoke_rest(request_type, rest_url, payload=None, headers=None):
    count = 1
    while True:
        try:
            api_url = rest_url
            if request_type == 'GET':
                r = requests.get(api_url, headers=headers)

                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            elif request_type == 'POST':
                r = requests.post(api_url, data=payload, headers=headers)
                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            elif request_type == 'PUT':
                r = requests.put(api_url, data=payload, headers=headers)
                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            else:
                return "Invalid request type ", request_type
        except Exception, e:
            print "Error in invoking " + request_type + ", " + api_url + ", Reattempting " + str(count)
            count = count + 1
            time.sleep(50.0 / 1000.0);  # Sleep 50 milli sec



def set_groups(BASE_URL, body, headers, zviceID):
    return invoke_rest('POST', BASE_URL + 'usergroups/add/' + zviceID, json.dumps(body), headers)

def create_user_group(BASE_URL,headers1,grpname,zviceID):
    body = {'groupName': grpname, 'groupDesc': ""}
    result = set_groups(BASE_URL, body, headers1, zviceID)
    return result
#***********************************************************
#******************* This code is for Editing the Submissions ***********************************
def edit_form_submission_true(submission_id,field_name,zviceID):
    for row in field_name:
        body = {}
        url = "http://www.twig-me.com/v8/submission_edit_action/" + zviceID + "/formsubmission/" + submission_id
        method = "GET"
        jsonresponse = CM.hit_url_method(body, headers1, method, url)

        for subac1 in json.loads(jsonresponse)['data']['ondemand_action']:
            data1 = json.loads(subac1['data'])
            c = 0
            for element in data1['Elements'][0]['Elements']:
                if element['ElementID'] == row:
                    print "found element"
                    data1['Elements'][0]['Elements'][c]["Value"] = "true"
                c = c + 1
        body = data1
        method = subac1['method']
        url = subac1['actionUrl']
        jsonresponse = CM.hit_url_method(body, headers1, method, url)


def edit_form_submission(submission_id,field_name,zviceID):
    for row in field_name:
        body = {}
        url = "http://www.twig-me.com/v8/submission_edit_action/" + zviceID + "/formsubmission/" + submission_id
        method = "GET"
        jsonresponse = CM.hit_url_method(body, headers1, method, url)

        for subac1 in json.loads(jsonresponse)['data']['ondemand_action']:
            data1 = json.loads(subac1['data'])
            c = 0
            for element in data1['Elements'][0]['Elements']:
                if element['ElementID'] == row:
                    print "found element"
                    data1['Elements'][0]['Elements'][c]["Value"] = "false"
                c = c + 1
        body = data1
        method = subac1['method']
        url = subac1['actionUrl']
        jsonresponse = CM.hit_url_method(body, headers1, method, url)

#**************************      Add User To Group   *******************************
def add_user_to_group(g_ID,user_id,zviceID):
    body = {}
    body['grpUserZviceID'] = user_id
    body['groupid'] = g_ID
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_SEARCH_FOR_AUTOCOMPLETE"
    body['searchType'] = 1
    method = "POST"
    url = BASE_URL + 'usergroups/user/add/' + zviceID
    jsonreply = CM.hit_url_method(body, headers1, method, url)
    return jsonreply
#********************************************************************************

def visitor_management(body,email,BASE_URL):
    if body['Cmd'] == "form-submit" and body['BusinessTag'] == "WHGJ7HTVTDFH3":
        if body['FormID'] == '63881':# Input Form
            print "hitting correct"
            name = body['FormData']['User Name ']
            department = body['FormData']['Department ']
            role = body['FormData']['Role']
            email = body['FormData']['Email ID']
            phone_no = body['FormData']['Mobile number ']
            # link_user = body['FormData']['Link User?']

            if body['FormData']['Link Stage'] == "Link Now":
                email_ID = email
            else:email_ID = ""

            result = add_user(body['BusinessTag'],name,email_ID)
            print result
            jsonreply = json.loads(result)
            # result = '{"error":false,"message":"","error_code":-1,"data":{"usertagid":"EJSWWXDFF4B6G","elements":null,"disableExpandToolbar":true},"title":"Future Group","toolbarbgimgurl":"https:\/\/s3-ap-south-1.amazonaws.com\/dev-zestl-4\/1507537696_556864179_FutureConsumerWhiteBg%5B1%5D.png","isBusiness":true,"homeurl":"http:\/\/www.twig-me.com\/v11\/zvice\/detailscard\/WHGJ7HTVTDFH3","homemethod":"POST","homejsondata":null,"businesstagid":"WHGJ7HTVTDFH3","users":[{"usertagid":"33PQMYD4N77DP","usertagtitle":"Super Admin User"},{"usertagid":"FJBSBPYQMRZZN","usertagtitle":"ALL","selected":true}],"bottom_bar":[{"title":"My Reports","icon":"ic_action_timelapse","url":"Test","method":"GET","jsonData":null},{"title":"My Tasks","icon":"ic_action_dns","url":"http:\/\/twig-me.com\/v13\/user\/tasks\/get\/WHGJ7HTVTDFH3","method":"GET","jsonData":null},{"title":"My Projects","icon":"ic_action_dashboard","url":"http:\/\/twig-me.com\/v13\/myworkflows\/WHGJ7HTVTDFH3","method":"GET","jsonData":null},{"title":"My Team","icon":"ic_action_group","url":"http:\/\/www.twig-me.com\/v13\/usergroups\/business\/user\/","method":"GET","jsonData":null},{"title":"Workflow","icon":"ic_action_open_in_browser","url":"http:\/\/twig-me.com\/v11\/workflow\/WHGJ7HTVTDFH3\/cards","method":"GET","jsonData":null},{"title":"L My Projects","icon":"ic_action_local_offer","url":"http:\/\/twig-me.com\/lankesh\/v13\/myworkflows\/WHGJ7HTVTDFH3","method":"GET","jsonData":null}]}'
            jsonreply = json.loads(result)
            user_id = jsonreply['data']['usertagid']

            result = create_user_group(BASE_URL, headers1, name, body['BusinessTag'])
            print result
            # result = {'reply': u'{"error":false,"message":"","error_code":-1,"refresh":true,"output":{"groupdetails":{"groupid":2440}}}', 'code': 200}
            result = result['reply']
            result_1 = json.loads(result)
            g_ID = result_1['output']['groupdetails']['groupid']

            result = add_user_to_group(g_ID,user_id,body['BusinessTag'])

            # if body['FormData']['Link Stage'] == "Link Now":
            #     email_ID = email
            # else:email_ID = ""
            # result = add_user(body['BusinessTag'],name,email_ID)
            # print result
            # jsonreply = json.loads(result)
            # user_id = jsonreply['data']['usertagid']
            # result = CM.create_user_group(BASE_URL,headers1,name,body['BusinessTag'])




            #
            # if flag_1 == "Y" or flag_1 == "y":
            #     with open(outputFile, "w") as ef:
            #         P_name = raw_input("Enter person name: ")
            #         p_email = raw_input("Enter email id: ")
            #         result = add_user(business_id, P_name, p_email)
            #         jsonreply = json.loads(result)
            #         user_id = jsonreply['data']['usertagid']
            #         efwrite = user_id + "," + P_name + "\n"
            #         ef.write(efwrite)
            #     # form_name = raw_input("Enter Existing Form Name: ")
            #     # form_ID = fetchCard(business_id, form_name, headers1)
            #     # print form_ID
            #     # result = edit_existing_temp_admin(form_ID, business_id)
            # else:
            #     # ***************************
            #
            #     fname = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/" + filename
            #     # fname = "/var/www/cgi-bin/workflow/" + filename
            #     hasHeader = "Y"
            #     # ****************************  Create users from this file *****************
            #     with open(fname, 'r') as rf:
            #         with open(outputFile, "w") as ef:
            #             data = csv.reader(rf, delimiter=',')
            #             if hasHeader == "Y":
            #                 row1 = data.next()
            #             counter = 0
            #             for row in data:
            #                 counter += 1
            #                 # print counter
            #                 u_name = row[0]
            #                 u_email = row[1]
            #                 result = add_user(business_id, u_name, u_email)
            #                 print result
            #                 jsonreply = json.loads(result)
            #                 user_id = jsonreply['data']['usertagid']
            #                 efwrite = user_id + "," + u_name + "\n"
            #                 ef.write(efwrite)



if __name__ == "__main__":
    BASE_URL = "http://twig-me.com/v11/"  ### dev server
    zviceID = "WHGJ7HTVTDFH3"  # minal dev business
    email = "admin@zestl.com"
    pwd = "TwigMeNow"
    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
#*******************  this will take input from PHP   ****************
    try:
        inp = sys.argv[1]
    except:
        # inp = '{"Cmd":"form-submit","BusinessTag":"X5NXPTNGRG2H3","FormID":"1636","FormSubmissionID":"1904","FormData":{"Start":null,"Lab Test":"Test 1","WorkflowID":"33","Name":null,"Email":null,"Phone Number":null}}'
    # inp = '{"Cmd":"workflow-create","BusinessTag":"3QVRRWHHJX3D9","WorkflowID":5,"WorkflowTypeID":1,"WorkflowTitle":"S220"}'
    # inp = '{"Cmd":"workflow-create","BusinessTag":"3QVRRWHHJX3D9","WorkflowID":1,"WorkflowTypeID":1,"WorkflowTitle":"Suj1"}'
    #     inp = '{"Cmd":"form-submit","BusinessTag":"83H6LVUBRXWZ5","FormID":"44","FormSubmissionID":53,"FormData":{"Input Form":null,"Password":"TwigMeNow","Business_Name":"Minal Dev Server","New Business Or not":"N","Do u want new user or not":"N","Write file name":"one.csv"}}'
    #     inp = '{"Cmd":"form-submit","BusinessTag":"83H6LVUBRXWZ5","FormID":"44","FormSubmissionID":55,"FormData":{"Input Form":null,"Password":"TwigMeNow","Business_Name":"Minal Dev Server","New Business Or not":"N","Do u want new user or not":"N","Write file name":"one.csv","Do you want NAME - press Y \/ N":"Y","Do you want Phone - press Y \/ N":"Y","Do you want Email - press Y \/ N":"Y","Visit list - press Y \/ N":"Y","Do you want check box - press Y \/ N":"Y","Enter Form name":"14 sep"}}'
    #     inp = '{"Cmd":"form-submit","BusinessTag":"83H6LVUBRXWZ5","FormID":"44","FormSubmissionID":71,"FormData":{"Input Form":null,"Password":"TwigMeNow","Business_Name":"Sayalistestorg","New Business Or not":"N","Do u want new user or not":"N","Write file name":"one.csv","Do you want NAME - press Y \/ N":"Y","Do you want Phone - press Y \/ N":"N","Do you want Email - press Y \/ N":"Y","Visit list - press Y \/ N":"Y","Do you want check box - press Y \/ N":"Y","Enter Form name":"September"}}'

        # inp = '{"Cmd":"form-submit","BusinessTag":"83H6LVUBRXWZ5","FormID":"179","FormSubmissionID":180,"FormData":{"User Name":"Minal","Department":null,"Role":null,"Email ID":null,"Phone Number":null,"link user?":"false","link usinh":null},"tags":[]}'
        inp = '{"Cmd":"form-submit","BusinessTag":"83H6LVUBRXWZ5","FormID":"179","FormSubmissionID":181,"FormData":{"User Name":"Minal","Department":"Abc","Role":"Mgr","Email ID":"Minal@zestl.com","Phone Number":"9637707494","link user?":"false","link using":"Email"},"tags":[]}'
        inp = '{"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"63881","FormSubmissionID":64881,"FormData":{"User Name ":null,"Department ":null,"Role":null,"Mobile number ":null,"Email ID":null,"Link User?":"false","Link Stage":"Link Now"},"tags":[]'
        inp = '{"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"63881","FormSubmissionID":64875,"FormData":{"User Name ":"Minal","Department ":"COM","Role":"Manager","Mobile number ":"9637707494","Email ID":"minal@zestl.com","Link User to the FG app":"Link Later","Link Stage":"Link Now"},"tags":[]}'
        inp = '{"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"63881","FormSubmissionID":64882,"FormData":{"User Name ":"Sayali","Department ":null,"Role":null,"Mobile number ":null,"Email ID":"minal@zestl.com","Link User?":"false","Link Stage":"Link Now"},"tags":[]}'
    body = json.loads(inp)

# Form ID = 179
    try:
        with open("/var/www/cgi-bin/workflow/o.txt", 'w') as wf:
            wf.write("i was here\n")
            wf.write(sys.argv[1])

    except:
        a = 1
    try:
        w_ID = body['FormData']['WorkflowID']
        # w_ID = 21
        w_ID = str(w_ID)
    except:
        w_ID = 0

    if body['BusinessTag'] == "WHGJ7HTVTDFH3" and body['Cmd'] == "form-submit":
        visitor_management(body,email,BASE_URL)