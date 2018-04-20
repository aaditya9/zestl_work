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

def visitor_management(body,email,BASE_URL):
    if body['Cmd'] == "form-submit" and body['BusinessTag'] == "83H6LVUBRXWZ5":
        # print "present"
        if body['FormID'] == '44':# Input Form

            ItagID = "9ED7VXL4BF4TN"  ###ShripadTest
            SItagID1 = ""
            SItagID2 = ""

            passkey = body['FormData']['Password']
            headers, headers1 = LL.req_headers(email,passkey,BASE_URL)

            CustomerName = body['FormData']['Business_Name']
            Cname = re.sub('[\W_]+', '', CustomerName)

            Business_flag = body['FormData']['New Business Or not']
            flag_1 = body['FormData']['Do u want new user or not']
            filename = body['FormData']['Write file name']
            Name = body['FormData']['Do you want NAME - press Y / N']
            Phone = body['FormData']['Do you want Phone - press Y / N']
            Email = body['FormData']['Do you want Email - press Y / N']
            to_visit = body['FormData']['Visit list - press Y / N']
            check_box = body['FormData']['Do you want check box - press Y / N']
            Form_Name = body['FormData']['Enter Form name']


            if Business_flag == 'Y' or Business_flag == 'y':
                data = {}
                body = {"DisplayName": Cname, "MaxAllowedTags": 100}
                url = BASE_URL + "customers"
                method = "POST"
                jsonreply = CM.hit_url_method(body, headers1, method, url)
                jsondata = json.loads(jsonreply)
                business_id = jsondata['data'][0]['ZbotID']

                url = BASE_URL + "zvice/interaction/" + business_id
                method = "POST"
                body = {"title": CustomerName, "desc": CustomerName,
                        "interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
                if re.match(r'\w{13}', ItagID):
                    body['PrimaryOwnerITagID'] = ItagID
                if re.match(r'\w{13}', SItagID1):
                    body['SecondaryOwnerITagID1'] = SItagID1
                if re.match(r'\w{13}', SItagID2):
                    body['SecondaryOwnerITagID2'] = SItagID2
                jsonreply = CM.hit_url_method(body, headers1, method, url)

            if Business_flag == 'N' or Business_flag == 'n':
                method = "GET"
                url = BASE_URL + 'customers'
                body = {}
                jsonreply = CM.hit_url_method(body, headers1, method, url)
                jsonreply = json.loads(jsonreply)

                for elements in jsonreply['data']:
                    for cust in elements['mapped_customers']:
                        if CustomerName == cust['Title']:
                            business_id = cust['ZbotID']
                            print "Customer tag ids is : " + business_id
                            # ************************************************************************************

            outputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"
            # outputFile = "/var/www/cgi-bin/workflow/minal_try.csv"

            if flag_1 == "Y" or flag_1 == "y":
                with open(outputFile, "w") as ef:
                    P_name = raw_input("Enter person name: ")
                    p_email = raw_input("Enter email id: ")
                    result = add_user(business_id, P_name, p_email)
                    jsonreply = json.loads(result)
                    user_id = jsonreply['data']['usertagid']
                    efwrite = user_id + "," + P_name + "\n"
                    ef.write(efwrite)
                # form_name = raw_input("Enter Existing Form Name: ")
                # form_ID = fetchCard(business_id, form_name, headers1)
                # print form_ID
                # result = edit_existing_temp_admin(form_ID, business_id)
            else:
                # ***************************

                fname = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/" + filename
                # fname = "/var/www/cgi-bin/workflow/" + filename
                hasHeader = "Y"
                # ****************************  Create users from this file *****************
                with open(fname, 'r') as rf:
                    with open(outputFile, "w") as ef:
                        data = csv.reader(rf, delimiter=',')
                        if hasHeader == "Y":
                            row1 = data.next()
                        counter = 0
                        for row in data:
                            counter += 1
                            # print counter
                            u_name = row[0]
                            u_email = row[1]
                            result = add_user(business_id, u_name, u_email)
                            print result
                            jsonreply = json.loads(result)
                            user_id = jsonreply['data']['usertagid']
                            efwrite = user_id + "," + u_name + "\n"
                            ef.write(efwrite)
                csvFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/file_template.csv"
                # csvFile = "/var/www/cgi-bin/workflow/file_template.csv"
                with open(csvFile, "w") as ef:
                    if Name == "Y":
                        writeString = "Name" + "," + "EDIT_TEXT" + "\n"
                        ef.write(writeString)

                    if Phone == "Y":
                        writeString = "Phone" + "," + "EDIT_TEXT" + "\n"
                        ef.write(writeString)

                    if Email == "Y":
                        writeString = "Email" + "," + "EDIT_TEXT" + "\n"
                        ef.write(writeString)

                    if to_visit == "Y":
                        writeString = "to_visit" + "," + "TEMP_ADMIN_LIST" + "\n"
                        ef.write(writeString)

                    if check_box == "Y":
                        writeString = "Terms and Conditions : If you agree then tick on check box" + "," + "CHECK_BOX" + "\n"
                        ef.write(writeString)

                    # new_user = str(raw_input("Do you want to create new user from visitor - press Y / N : "))


                # ************ Create form card *******************
                form_card_result = create_form(Form_Name,business_id)
                form_card_id = form_card_result['cardid']
                time.sleep(500.0 / 1000.0);

                # *********************  Setting permission to the form card   **********************#
                body = {}
                body['opType'] = 1
                body['actionType'] = "MAIL"
                body['groupID'] = -2001
                body['cardID'] = form_card_id
                body['cardType'] = "GenericCard"
                method = "POST"
                url = BASE_URL + 'card/permissions/' + business_id
                jsonreply = CM.hit_url_method(body, headers1, method, url)
                # print jsonreply
                # **************************   Auto select   ******************************
                body = {'cardType': 'GenericCard', 'cardID': form_card_id, 'policyType': 'AUTO_UPDATE_CARD_MAIL','policyVal': "true"}
                method = "POST"
                url = BASE_URL + "cards/policy/" + business_id
                jsonreply = CM.hit_url_method(body, headers1, method, url)
                # print jsonreply
                # ********************************  Mail / notification ******************************
                body = {'cardType': 'GenericCard', 'cardID': form_card_id, 'actionType': 'MAIL', 'sendMail': "true",'sendNotification': "true"}
                method = "PUT"
                url = BASE_URL + "cards/permsissions/extraperm/" + business_id
                jsonreply = CM.hit_url_method(body, headers1, method, url)
                # print jsonreply
                # ********************************************

                # *********************** Form Content *********************************
                form_content_result = form_content(form_card_id,business_id,Form_Name,csvFile,outputFile)
                Form_Name = "Add Single User"
                form_card_result = create_form(Form_Name, business_id)
                form_card_id_1 = form_card_result['cardid']
                # csvFile = "/var/www/cgi-bin/workflow/user.csv"
                csvFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/user.csv"
                form_content_result = form_content(form_card_id_1, business_id, Form_Name, csvFile, outputFile)






def workflow_genie_1(body, w_ID):
    forms = {u'Packaging-Stage 5': u'12', u'Marketing-Stage2': u'2', u'PD-Stage 5': u'20', u'Packaging-Stage 6': u'13',
             u'PD-Stage 3': u'18', u'Marketing-Stage 6': u'6', u'Marketing-Stage 1': u'1', u'Packaging-Stage 2': u'9',
             u'Packaging - Stage 4': u'11', u'Marketing-Stage 4': u'4', u'Packaging-Stage1': u'8',
             u'PD-Stage 2 W/ R&D': u'16', u'Packaging-Stage3': u'10', u'Marketing-Stage3': u'3', u'PD - Stage 4': u'19',
             u'PD-Stage 2 W/O R&D': u'17', u'PD - Overall Summary': u'21', u'PD - Stage 1': u'15',
             u'Marketing Summary': u'7', u'Packaging Summary': u'14', u'Marketing-Stage 5': u'5'}
    d = {'Yes': 17, 'No': 16}
    if body['Cmd'] == "form-submit" and body['BusinessTag'] == "3QVRRWHHJX3D9":
        if body['FormID'] == '15':  # PD - Stage 1
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            # print result_1
            for sub_id in json.loads(result_1)['data']['matchedRows']:
                # print sub_id['FormID']
                for k, v in d.items():
                    if body['FormData']['Similar Products Available'] == k:
                        if v == sub_id['FormID']:
                            submission_id = sub_id['FormSubmissionID']
                            submission_id = str(submission_id)
                            result = publish_submission(submission_id,body['BusinessTag'])
                            output = {}
                            output['FormID'] = sub_id['FormID']
                            output['FormSubmissionID'] = sub_id['FormSubmissionID']
                            output['BusinessTag'] = '3QVRRWHHJX3D9'
                            print json.dumps(output)

        elif body['FormID'] == '16':    #PD-Stage 2 W/ R&D
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Product Spec Ready'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 18:  #PD-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)

                    if sub_id['FormID'] == 1:  #Marketing-Stage 1
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])

                    if sub_id['FormID'] == 8:  #Packaging-Stage1
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])

        elif body['FormID'] == '17':    #PD-Stage 2 W/O R&D
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Product Spec Ready'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 18:  #PD-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)

                    if sub_id['FormID'] == 1:  #Marketing-Stage 1
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])

                    if sub_id['FormID'] == 8:  #Packaging-Stage1
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])

#****************************************  This Flow Is For Packaging  **************************
        elif body['FormID'] == '8':    #Packaging-Stage1
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Product Feature Spec Ready']=="true" and body['FormData']['Product Attributes Ready']=="true" and body['FormData']['Product Pack Sizes Ready']=="true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 9:  #Packaging-Stage 2
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '9':    #Packaging-Stage 2
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Are 2D packaging spec ready']=="true" and body['FormData']['Are 3D packaging spec ready']=="true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 10:  #Packaging-Stage3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '10':  # Packaging-Stage 3
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Evaluation Result'] == "Approved":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 11:  # Packaging - Stage 4
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)

            elif body['FormData']['Evaluation Result'] == "Suggested changes":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 9:  # Packaging - Stage 2
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        field_name = ["Are 2D packaging spec ready", "Are 3D packaging spec ready"]
                        # result = publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
                        result = edit_form_submission(submission_id, field_name, body['BusinessTag'])


        # elif body['FormID'] == '10':  # Packaging-Stage 3
        #     result_1 = get_submission_id(w_ID, body['BusinessTag'])
        #     d = {'Approved': 11, 'Suggested changes': 9}    # if approved go to "Packaging - Stage 4" else go to "Packaging-Stage 2"
        #     for sub_id in json.loads(result_1)['data']['matchedRows']:
        #         for k, v in d.items():
        #             if body['FormData']['Evaluation Result'] == k:
        #                 if v == sub_id['FormID']:
        #                 # if sub_id['FormID'] == 11:  # Packaging - Stage 4
        #                     submission_id = sub_id['FormSubmissionID']
        #                     submission_id = str(submission_id)
        #                     result = publish_submission(submission_id,body['BusinessTag'])
        #                     output = {}
        #                     output['FormID'] = sub_id['FormID']
        #                     output['FormSubmissionID'] = sub_id['FormSubmissionID']
        #                     output['BusinessTag'] = '3QVRRWHHJX3D9'
        #                     print json.dumps(output)

        elif body['FormID'] == '11':  # Packaging-Stage 4
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Mock-ups ready'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 12:  # Packaging-Stage 5
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '12':  # Packaging-Stage 5
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Mockup Evaluation'] == "Approved":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 13:  # Packaging-Stage 6
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)


        elif body['FormID'] == '13':  # Packaging-Stage 6
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Packaging Signoff'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 18:  # PD-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        field_name = ["Packaging Signoff ready"]
                        # result = edit_form_submission_true(submission_id,field_name,zviceID)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
                        result = edit_form_submission_true(submission_id, field_name, zviceID)



#******************************************************************************************************************

#***************************** This Flow Is For Marketing  ********************************************************
        elif body['FormID'] == '1':    # Marketing-Stage 1
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Ideation Done']=="true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 2:  #Marketing-Stage 2
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '2':  # Marketing-Stage 2
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Briefing Done'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 3:  # Marketing-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '3':  # Marketing-Stage 3
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Received Creatives'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 4:  # Marketing-Stage 4
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '4':  # Marketing-Stage 4
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Vetting Result'] == "Approved":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 5:  # Marketing-Stage 5
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)

            elif body['FormData']['Vetting Result'] == "Suggested Changes":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 3:  # Marketing-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        field_name = ["Received Creatives"]
                        # result = publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
                        result = edit_form_submission(submission_id, field_name, body['BusinessTag'])


        elif body['FormID'] == '5':  # Marketing-Stage 5
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['BOP checking status'] == "Approved":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 6:  # Marketing-Stage 6
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '6':  # Marketing-Stage 6
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Shareholders Signoff'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 18:  # PD-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        field_name = ["Marketing Signoff Ready"]
                        # result = edit_form_submission_true(submission_id,field_name,zviceID)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
                        result = edit_form_submission_true(submission_id, field_name, zviceID)
#*****************************************************************************************************************
#*******************    PD Stage 3  ******************************************************************************

        elif body['FormID'] == '18':  # PD-Stage 3
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['R&D Signoff ready'] == "true" and body['FormData']['Packaging Signoff ready'] == "true" and body['FormData']['Marketing Signoff Ready'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 19:  # PD-Stage 4
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

        elif body['FormID'] == '19':  # PD-Stage 4
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Trial results'] == "Approved":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 20:  # PD-Stage 5
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
            elif body['FormData']['Trial results'] == "Rejected":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 18:  # PD-Stage 3
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        field_name = ["R&D Signoff ready", "Packaging Signoff ready", "Marketing Signoff Ready"]
                        # result = publish_submission(submission_id, body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = '3QVRRWHHJX3D9'
                        print json.dumps(output)
                        result = edit_form_submission(submission_id, field_name, body['BusinessTag'])

#******************************************************************************************************************


#***************************************  Under the sky work flow demo*********************************************
def workflow_genie(body, w_ID):
    d = {'Test 1' : 1637 , 'Test 2' : 1640 , 'Test 3' : 1642}
    if body['Cmd'] == "form-submit" and body['BusinessTag'] == "X5NXPTNGRG2H3":
        if body['FormID'] == '1636':
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            for sub_id in json.loads(result_1)['data']['matchedRows']:
              #  print sub_id['FormID']
                for k,v in d.items():
                    if body['FormData']['Lab Test'] == k:
                        if v == sub_id['FormID']:
                            submission_id = sub_id['FormSubmissionID']
                            submission_id = str(submission_id)
                            result = publish_submission(submission_id,body['BusinessTag'])
                            output = {}
                            output['FormID'] = sub_id['FormID']
                            output['FormSubmissionID'] = sub_id['FormSubmissionID']
                            output['BusinessTag'] = 'X5NXPTNGRG2H3'
                            print json.dumps(output)
        elif body['FormID'] == '1637':
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Approved'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 1638:
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = 'X5NXPTNGRG2H3'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = 'X5NXPTNGRG2H3'
                print json.dumps(output)

    # Form 2A
        elif body['FormID'] == '1640':
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Approved'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 1641:
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = 'X5NXPTNGRG2H3'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = 'X5NXPTNGRG2H3'
                print json.dumps(output)

        # Form 3A
        elif body['FormID'] == '1642':
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Approved'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 1643:
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = 'X5NXPTNGRG2H3'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = 'X5NXPTNGRG2H3'
                print json.dumps(output)

        # Form 2B
        elif body['FormID'] == '1641':
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Approved'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 1643:
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = 'X5NXPTNGRG2H3'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = 'X5NXPTNGRG2H3'
                print json.dumps(output)

                # Form 1C
        elif body['FormID'] == '1639':
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Approved'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 1643:
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = 'X5NXPTNGRG2H3'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = 'X5NXPTNGRG2H3'
                print json.dumps(output)

                # Form 1C
        elif body['FormID'] == '1638':
            result_1 = get_submission_id(w_ID, body['BusinessTag'])
            if body['FormData']['Approved'] == "true":
                for sub_id in json.loads(result_1)['data']['matchedRows']:
                    if sub_id['FormID'] == 1639:
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id,body['BusinessTag'])
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormSubmissionID']
                        output['BusinessTag'] = 'X5NXPTNGRG2H3'
                        print json.dumps(output)
            else:
                output = {}
                output['FormID'] = body['FormID']
                output['FormSubmissionID'] = body['FormSubmissionID']
                output['BusinessTag'] = 'X5NXPTNGRG2H3'
                print json.dumps(output)




def submit_form(a, form_id, zviceID):
    for row in form_id:
        id = row
        body = {}
        url = BASE_URL + "submit_action/" + zviceID + "/form/" + str(id)
        method = "GET"
        jsonresponse = CM.hit_url_method(body, headers1, method, url)
    #    print jsonresponse

        for subac1 in json.loads(jsonresponse)['data']['ondemand_action']:
            data1 = json.loads(subac1['data'])
            c = 0
            for element in data1['Elements'][0]['Elements']:
                # if element['ElementID'] == "Work FlowId":
                if element['ElementID'] == "WorkflowID":
      #              print "found element"
                    data1['Elements'][0]['Elements'][c]["Value"] = a
                c = c + 1
       #         print "Element position: " + str(c)
        body = data1
        method = subac1['method']
        url = subac1['actionUrl']
        jsonresponse = CM.hit_url_method(body, headers1, method, url)
      #  print jsonresponse

def publish_submission(submission_id,zviceID):
    url = "http://www.twig-me.com/v11/formsubmission/" + zviceID + "/publish/" + submission_id
    method = "POST"
    body = {}
    body['Flags'] = "true"
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

#*************************  this part is giving us Form card id and form submission id related to this work flow
def get_submission_id(w_ID, zviceID):
    body = {}
    method = "GET"
    url = "http://www.twig-me.com/v11/" +  zviceID + "/forms/submissions/workflow/" + w_ID
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

if __name__ == "__main__":
    BASE_URL = "http://twig-me.com/v11/"  ### dev server
    zviceID = "83H6LVUBRXWZ5"  # Work flow demo department
    email = "admin@zestl.com"
    pwd = "TwigMeNow"
    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
#*******************  this will take input from PHP   ****************
    # try :
    #print sys.argv[1]
    #inp = '{"Cmd":"form-submit","BusinessTag":"X5NXPTNGRG2H3","FormID":"1637","FormSubmissionID":"1836","FormData":{"1A":null,"WorkflowID":"42","Test results":"https:\/\/s3-ap-south-1.amazonaws.com\/dev-zestl-4\/1502705097_887485580_temporary_holder.jpg","Approved?":"true","Notes":"Now"}}'
    try:
        inp = sys.argv[1]
    except:
        # inp = '{"Cmd":"form-submit","BusinessTag":"X5NXPTNGRG2H3","FormID":"1636","FormSubmissionID":"1904","FormData":{"Start":null,"Lab Test":"Test 1","WorkflowID":"33","Name":null,"Email":null,"Phone Number":null}}'
    # inp = '{"Cmd":"workflow-create","BusinessTag":"3QVRRWHHJX3D9","WorkflowID":5,"WorkflowTypeID":1,"WorkflowTitle":"S220"}'
    # inp = '{"Cmd":"workflow-create","BusinessTag":"3QVRRWHHJX3D9","WorkflowID":1,"WorkflowTypeID":1,"WorkflowTitle":"Suj1"}'
    #     inp = '{"Cmd":"form-submit","BusinessTag":"83H6LVUBRXWZ5","FormID":"44","FormSubmissionID":53,"FormData":{"Input Form":null,"Password":"TwigMeNow","Business_Name":"Minal Dev Server","New Business Or not":"N","Do u want new user or not":"N","Write file name":"one.csv"}}'
    #     inp = '{"Cmd":"form-submit","BusinessTag":"83H6LVUBRXWZ5","FormID":"44","FormSubmissionID":55,"FormData":{"Input Form":null,"Password":"TwigMeNow","Business_Name":"Minal Dev Server","New Business Or not":"N","Do u want new user or not":"N","Write file name":"one.csv","Do you want NAME - press Y \/ N":"Y","Do you want Phone - press Y \/ N":"Y","Do you want Email - press Y \/ N":"Y","Visit list - press Y \/ N":"Y","Do you want check box - press Y \/ N":"Y","Enter Form name":"14 sep"}}'
        inp = '{"Cmd":"form-submit","BusinessTag":"83H6LVUBRXWZ5","FormID":"44","FormSubmissionID":71,"FormData":{"Input Form":null,"Password":"TwigMeNow","Business_Name":"Sayalistestorg","New Business Or not":"N","Do u want new user or not":"N","Write file name":"one.csv","Do you want NAME - press Y \/ N":"Y","Do you want Phone - press Y \/ N":"N","Do you want Email - press Y \/ N":"Y","Visit list - press Y \/ N":"Y","Do you want check box - press Y \/ N":"Y","Enter Form name":"September"}}'
    body = json.loads(inp)


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

    if body['Cmd'] == "workflow-create" and body['BusinessTag'] == "A4CJ2VHTTJS9Y":
        form_id = [1643, 1642, 1641, 1640, 1639, 1638, 1637, 1636]
        result = submit_form(body['WorkflowID'], form_id, 'X5NXPTNGRG2H3')
        result_2 = get_submission_id(str(body['WorkflowID']), body['BusinessTag'])
        for sub_id in json.loads(result_2)['data']['matchedRows']:
            if sub_id['FormID'] == 1636:
                output = {}
                output['FormID'] = 1636
                output['FormSubmissionID'] = sub_id['FormSubmissionID']
                output['BusinessTag'] = 'X5NXPTNGRG2H3'
                print json.dumps(output)
    elif body['Cmd'] == "workflow-create" and body['BusinessTag'] == "3QVRRWHHJX3D9":
        forms = {u'Packaging-Stage 5': u'12', u'Marketing-Stage2': u'2', u'PD-Stage 5': u'20', u'Packaging-Stage 6': u'13',
         u'PD-Stage 3': u'18', u'Marketing-Stage 6': u'6', u'Marketing-Stage 1': u'1', u'Packaging-Stage 2': u'9',
         u'Packaging - Stage 4': u'11', u'Marketing-Stage 4': u'4', u'Packaging-Stage1': u'8',
         u'PD-Stage 2 W/ R&D': u'16', u'Packaging-Stage3': u'10', u'Marketing-Stage3': u'3', u'PD - Stage 4': u'19',
         u'PD-Stage 2 W/O R&D': u'17', u'PD - Overall Summary': u'21', u'PD - Stage 1': u'15',
         u'Marketing Summary': u'7', u'Packaging Summary': u'14', u'Marketing-Stage 5': u'5'}
        form_id = []
        for k,v in forms.items():
            form_id.append(int(v))
        result = submit_form(body['WorkflowID'], form_id, body['BusinessTag'])
        result_2 = get_submission_id(str(body['WorkflowID']), body['BusinessTag'])
        for sub_id in json.loads(result_2)['data']['matchedRows']:
            if sub_id['FormID'] == int(forms['PD - Stage 1']):
                output = {}
                output['FormID'] = sub_id['FormID']
                output['FormSubmissionID'] = sub_id['FormSubmissionID']
                output['BusinessTag'] = '3QVRRWHHJX3D9'
                print json.dumps(output)

    if body['BusinessTag'] == "X5NXPTNGRG2H3" and body['Cmd'] == "form-submit":
        workflow_genie(body, w_ID)


    elif body['BusinessTag'] == "3QVRRWHHJX3D9" and body['Cmd'] == "form-submit":
        workflow_genie_1(body, w_ID)

    elif body['BusinessTag'] == "83H6LVUBRXWZ5" and body['Cmd'] == "form-submit":
        visitor_management(body,email,BASE_URL)