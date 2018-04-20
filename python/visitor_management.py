import requests
import json
import re
from urllib import urlopen
import csv
import time
import common as CM
import lib.login_admin as LL

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def registerZvice(headers, body, zviceID):
    return LL.invoke_rest('PUT', LL.BASE_URL + 'zvice/register/' + zviceID, body, headers)

def getBaseStructure(zbotID, headers1):
    url = LL.BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    response = hit_url(RequestBody, headers1, zbotID, url)
    return response


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def getPublicIp():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)


def getAllUserGroups(headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('GET', BASE_URL + 'usergroups/' + zbotID, None, headers)
    return jsondata['reply']


def change_view_permissions_fullurl(body, headers, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL , json.dumps(body), headers)
    return jsondata['reply']

def add_user(business_id,u_name,u_email):
    method = "POST"
    url = LL.BASE_URL + 'zvice/interaction/' + business_id
    body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat', 'long': 'long', 'tagprofile': 0,
            'media_type': 'image/jpg',
            'media_ext': 'jpg', 'media': "", 'media_size': 0, 'zbotid': business_id}
    body['title'] = u_name
    body['linkemail'] = u_email
    body['autogentag'] = "true"
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"
    jsonreply = hit_url_method(body, headers1, method, url)
    return jsonreply

def edit_existing_temp_admin():
    body = {}
    url = "http://35.154.64.119/v8/all_actions/876MD568TAUH2/form/1858"
    method = "GET"
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    print jsonresponse

    # ElementFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"
    outputFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"
    for subac1 in json.loads(jsonresponse)['data']['ondemand_action']:
        if subac1['title'] == "Edit":
            print "i am here"
            data1 = json.loads(subac1['data'])
            c = 0
            for element in data1['Elements'][0]['Elements']:
                if element['ElementType'] == "TEMP_ADMIN_LIST":
                    for b in element['MetaData']['TempAdminList']:
                        for sub_b in b['MapValue']:
                            # time.sleep(500.0 / 1000.0);
                            with open(outputFile, "a") as ef:
                                efwrite = sub_b['id'] + "," + sub_b['title'] + "\n"
                                print efwrite
                                ef.write(efwrite)
                                print sub_b
                                print sub_b['id']
                                print sub_b['title']

                if element['ElementID'] == "admin 1":
                    print "found element"
                    temp_list = []
                    temp_options = []
                    addElement = {}
                    with open(outputFile, 'r') as my_temp_list:
                        data2 = csv.reader(my_temp_list, delimiter=',')
                        print data2
                        for row in data2:
                            a = {"MapKey": row[1],
                                 "MapValue": [{"title": row[1], "subtitle": "User", "id": row[0], "type": "USER"}]}
                            temp_list.append(a)
                            temp_options.append(row[1])
                    data1['Elements'][0]['Elements'][c]["Options"] = temp_options
                    data1['Elements'][0]['Elements'][c]["MetaData"] = {"TempAdminList": temp_list}
                c = c + 1
                print "Element position: " + str(c)
    body = data1
    print body
    url = "http://35.154.64.119/v8/876MD568TAUH2/forms/1858"
    method = "PUT"
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    print jsonresponse


ItagID = "9ED7VXL4BF4TN"    ###ShripadTest
SItagID1 = ""
SItagID2 = ""


passkey = str(raw_input("Enter password : "))
print "... Working ....."
headers, headers1 = LL.req_headers(passkey)

CustomerName = str(raw_input("Enter customer name : "))
Cname = re.sub('[\W_]+', '', CustomerName)

flag = str(raw_input("New Business - press Y for yes : Otherwise press N :"))
#*************************  Code for old and New business  **********
if flag == 'Y' or flag == 'y':
    data = {}
    body = {"DisplayName": Cname, "MaxAllowedTags": 100}
    url = LL.BASE_URL + "customers"
    print url
    method = "POST"
    jsonreply = hit_url_method(body, headers1, method, url)
    print jsonreply

    jsondata = json.loads(jsonreply)
    business_id = jsondata['data'][0]['ZbotID']
    print business_id

    url = LL.BASE_URL + "zvice/interaction/" + business_id
    method = "POST"
    body = {"title": CustomerName, "desc": CustomerName,
            "interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
    if re.match(r'\w{13}', ItagID):
        body['PrimaryOwnerITagID'] = ItagID
    if re.match(r'\w{13}', SItagID1):
        body['SecondaryOwnerITagID1'] = SItagID1
    if re.match(r'\w{13}', SItagID2):
        body['SecondaryOwnerITagID2'] = SItagID2
    jsonreply = hit_url_method(body, headers1, method, url)
    print jsonreply

if flag == 'N' or flag == 'n':
    method = "GET"
    url = LL.BASE_URL + 'customers'
    body = {}
    print " .... Working ....."
    jsonreply = hit_url_method(body, headers1, method, url)
    print jsonreply
    jsonreply = json.loads(jsonreply)

    for elements in jsonreply['data']:
        for cust in elements['mapped_customers']:
            if CustomerName == cust['Title']:
                business_id = cust['ZbotID']
                print "Customer tag ids is : " + business_id
#************************************************************************************

#******************* If U want to add single user **********************
outputFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"
flag_1 = str(raw_input("You want to add single user - press Y for yes : Otherwise press N :"))
if flag_1 == "Y" or flag_1 == "y":
    with open(outputFile, "w") as ef:
        P_name = raw_input("Enter person name: ")
        p_email = raw_input("Enter email id: ")
        result = add_user(business_id,P_name,p_email)
        jsonreply = json.loads(result)
        user_id = jsonreply['data']['usertagid']
        efwrite = user_id + "," + P_name + "\n"
        ef.write(efwrite)
    result = edit_existing_temp_admin()
else:
#***************************
    filename = raw_input("Enter Filename: ")
    fname = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/" + filename
    hasHeader = "Y"
    #****************************  Create users from this file *****************
    with open(fname, 'r') as rf:
        with open(outputFile, "w") as ef:

            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            counter = 0
            for row in data:
                counter += 1
                print counter
                u_name = row[0]
                u_email = row[1]
                result = add_user(business_id,u_name,u_email)
                print result
                jsonreply = json.loads(result)
                user_id = jsonreply['data']['usertagid']
                efwrite = user_id + "," + u_name + "\n"
                ef.write(efwrite)


    #******************* Taking Input *******************

    # Notify = str(raw_input("Should user be notified - press Y / N : "))
    #
    csvFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/file_template.csv"
    with open(csvFile, "w") as ef:
        Name = str(raw_input("Do you want NAME - press Y / N : "))
        # print Name
        if Name == "Y":
            writeString = "Name" + "," + "EDIT_TEXT" + "\n"
            ef.write(writeString)

        Phone = str(raw_input("Do you want Phone - press Y / N : "))
        if Phone == "Y":
            writeString = "Phone" + "," + "EDIT_TEXT" + "\n"
            ef.write(writeString)

        Email = str(raw_input("Do you want Email - press Y / N : "))
        if Email == "Y":
            writeString = "Email" + "," + "EDIT_TEXT" + "\n"
            ef.write(writeString)

        to_visit = str(raw_input("Visit list - press Y / N : "))
        if to_visit == "Y":
            writeString = "to_visit" + "," + "TEMP_ADMIN_LIST" + "\n"
            ef.write(writeString)

        check_box = str(raw_input("Do you want check box - press Y / N : "))
        if check_box == "Y":
            writeString = "Terms and Conditions : If you agree then tick on check box" + "," + "CHECK_BOX" + "\n"
            ef.write(writeString)

        new_user = str(raw_input("Do you want to create new user from visitor - press Y / N : "))

    Form_Name = str(raw_input("Enter Form name : "))
    #************************************************************


    #************ Create form card *******************
    method = "POST"
    r = requests.get("http://twig.me/v1/push/dectest/" + business_id)
    tagnum = r.json()['decTagID']
    r = requests.get("http://twig.me/v1/push/dectest/" + business_id)
    zbotnum = r.json()['decTagID']
    body = {"FormID": "", "FormDescription": Form_Name, "FormTitle": Form_Name,
            "ZviceID": tagnum, "ZbotID": zbotnum, "LinkType": "FORM", "LinkID": "",
            "parentCardID": None}
    url = LL.BASE_URL + business_id + "/forms"
    jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
    print jsondata
    form_card_id = jsondata['cardid']
    time.sleep(500.0 / 1000.0);

    #*********************  Setting permission to the form card   **********************#
    body = {}
    body['opType'] = 1
    body['actionType'] = "MAIL"
    body['groupID'] = -2001
    body['cardID'] = form_card_id
    body['cardType'] = "GenericCard"
    method = "POST"
    url = LL.BASE_URL + 'card/permissions/' + business_id
    jsonreply = hit_url_method(body, headers1, method, url)
    print jsonreply
    #**************************   Auto select   ******************************
    body = {'cardType': 'GenericCard', 'cardID': form_card_id, 'policyType': 'AUTO_UPDATE_CARD_MAIL', 'policyVal': "true"}
    method = "POST"
    url = LL.BASE_URL + "cards/policy/" + business_id
    jsonreply = hit_url_method(body, headers1, method, url)
    print jsonreply
    #********************************  Mail / notification ******************************
    body = {'cardType': 'GenericCard', 'cardID': form_card_id, 'actionType': 'MAIL', 'sendMail': "true",'sendNotification': "true"}
    method = "PUT"
    url = LL.BASE_URL + "cards/permsissions/extraperm/" + business_id
    jsonreply = hit_url_method(body, headers1, method, url)
    print jsonreply
    #********************************************

    def take_val(val,cc):

        for a in range(cc):  # if there are multiple elements present , then for each array remove the "ParentFormMetaID"
            del val[a]["ParentFormMetaID"]
            return val

    #*********************** Form Content *********************************
    method = "GET"
    # hasHeader1 = "Y"
    # ElementFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"
    url = LL.BASE_URL + business_id + "/forms/" + str(form_card_id)
    body = {}
    j1 = json.loads(CM.hit_url_method(body, headers1, method, url))
    for element in j1['data']['elements']:
        if Form_Name in element['title']:
            for action in element['actions']:
                if 'More actions' in action['title']:
                    body = {}
                    url = LL.BASE_URL + "all_actions/" + business_id+ "/form/" + str(form_card_id)
                    method = "GET"
                    jsonresponse = CM.hit_url_method(body, headers1, method, url)
                    for a in json.loads(jsonresponse)['data']['ondemand_action']:
                        if "Edit" in a['title']:
                            url = a['actionUrl']
                            data = json.loads(a['data'])
                            method = a['method']
                            print " &&&&&&&&&&&&&&&&&&&&&&& "
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
                                    # if hasHeader1 == "Y":
                                    #     row1 = data1.next()
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
                                                # if hasHeader1 == "Y":
                                                #     row1 = data2.next()
                                                for row in data2:
                                                    a = {"MapKey": row[1],
                                                         "MapValue": [{"title": row[1], "subtitle": "User",
                                                                       "id": row[0], "type": "USER"}]}
                                                    temp_list.append(a)
                                                    temp_options.append(row[1])
                                        addElement['Options'] = temp_options
                                        addElement['MetaData'] = {"TempAdminList": temp_list}
                                        elarray.append(dict(addElement))
                                zeroelem['Elements'] = elarray
                                tempAr.append(dict(zeroelem))
                            body['Elements'] = tempAr
                            body['DataSource'] = data['DataSource']
                            print body
                            jsonresponse = CM.hit_url_method(body, headers1, method, url)
                            print jsonresponse