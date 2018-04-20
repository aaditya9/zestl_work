import common as CM
import logon as LL
import json
import logging
import requests
import wfe_parser as WP
import time
import csv
import datetime


# SERVER = "http://twig-me.com/" #Dev
BASE_URL = "http://52.39.248.136/v13/"  # New FG server
# SERVER = "http://13.126.76.186/"    #future group server
# version = "v13/"
# BASE_URL = SERVER + version
zviceID = "WHGJ7HTVTDFH3" # Future group
# zviceID = "83H6LVUBRXWZ5"   # MInal dev server
# zviceID = "WKMUYXELA9LCC"  #Gene Path
email = "admin@zestl.com"
pwd = "TwigMeNow"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)


def add_val_in_table(BASE_URL,headers1, key, value, zviceID):
    url = BASE_URL + "workflow/" + zviceID + "/" + key + "/value/" + str(value)
    method = "POST"
    body = {}
    response = CM.hit_url_method(body, headers1, method, url)


def form_card(BASE_URL,headers1,title,zviceID,p_cardID):
    r = requests.get("http://twig.me/v1/push/dectest/" + zviceID)
    tagnum = r.json()['decTagID']
    body = {"FormTitle": title, "FormDescription": "", "ZviceID": tagnum, "ZbotID": zviceID,"LinkType": "FORM", "parentCardID" : str(p_cardID)}
    method = "POST"
    url = BASE_URL+ zviceID +"/forms"
    jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
    return jsondata['cardid']
#**************************************************************************************************#

def create_form_elements(BASE_URL,headers1,zviceID,cardID,form,form_element):
    method = "GET"
    url = BASE_URL + zviceID + "/forms/" + str(cardID)
    body = {}
    j1 = json.loads(CM.hit_url_method(body, headers1, method, url))
    for element in j1['data']['elements']:
        if form in element['title']:
            for action in element['actions']:
                if 'More actions' in action['title']:
                    body = {}
                    url = BASE_URL + "all_actions/" + zviceID + "/form/" + str(cardID)
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
                                zeroelem["FieldLabel"] = form
                                elarray = []
                                seqNo = 1
                                for row in form_element:
                                    elID = row['label']
                                    fldlabel = row['label']
                                    type = row['type']
                                    hint = row['placeholder']
                                    req = row['required']
                                    isEdit = row['editable']
                                    de_value = row['placeholder']

                                    # isAdmin = CM.force_decode(row[6])
                                    # isAdmin = isAdmin.lower()
                                    seqNo += 1
                                    addElement = {}
                                    addElement['ElementID'] = elID
                                    addElement['ElementType'] = type
                                    addElement['FieldLabel'] = fldlabel
                                    addElement['Hint'] = hint
                                    addElement['Required'] = req
                                    addElement['SequenceNo'] = seqNo
                                    addElement['MetaData'] = {"IsEditable": isEdit}

                                    if addElement['ElementType'] == "EDIT_TEXT":
                                        addElement['DefaultValue'] = hint
                                    else:addElement['DefaultValue'] = de_value

                                    if type == "SPINNER" or type == "RADIO_GROUP":
                                        spinelements = row['values'].split(";")
                                        addElement['Options'] = spinelements

                                    elarray.append(dict(addElement))
                                zeroelem['Elements'] = elarray
                                tempAr.append(dict(zeroelem))
                            body['Elements'] = tempAr
                            body['DataSource'] = data['DataSource']
                            # print body
                            jsonresponse = CM.hit_url_method(body, headers1, method, url)
                            return jsonresponse

#**********************************************************************************************************#


filename = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/wfe_list.csv"
filepath = 'C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/'
# filename = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/wfe_list.csv"
# filepath = '/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/wfes/'
outfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/form_tables.csv"


# t_id = str(response['taskID'])
s_id = str(65781)
keyname = "tasksOf" + s_id
# try:
    # writeVal = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], keyname)
    # result = json.loads(writeVal)
    # form_id = result['data']['value']['_value']
t_id =str(64008)
form_id = str(65780)
writeVal = form_id + "," + t_id

result = CM.add_val_in_table(BASE_URL, headers1, keyname, writeVal, zviceID)
print result





# val1['name'] + ":WFID_" + str(tagName) + "," + k
# result = 65785
# # form_name = "MARKET SIZE STUDY FORM"
# tagName = "COE_WFE1_1:WFID_10101,Exit Checklist"
# wid = 10101
# sub_result = CM.add_tags_future(str(result),tagName,BASE_URL,zviceID,headers1,wid)
# print sub_result



# with open(outfile, 'w') as of:
#     startdate = datetime.datetime.utcnow()
#     sd = startdate.strftime('%Y-%m-%d %H:%M:%S')
#     of.write(sd + "\n")
#     with open(filename, 'r') as rf:
#         data = csv.reader(rf, delimiter=',')
#         for row in data:
#             wfename = row[0]
#             print "working on wfe " + wfename
#             parsefile = filepath + wfename
#             val1 = {}
#             # val1 = parse_wfe(filename)
#             val1 = WP.parse_formcreate(parsefile)
#             val2 = WP.parse_wfe(parsefile)
#
#             jsondata = CM.getBaseStructure(zviceID,headers1,BASE_URL)
#             wfename = val2['name']
#             tname = "WFE:" + wfename
#             # tname = "WFE:Artwork Creation"
#             # print tname
#             # tname = "MINAL"
#             flag = True
#             # cardID = 1
#             for a in jsondata['data']['elements']:
#                 if a['title'] == tname:
#                     p_cardID = a['cardID']
#                     flag = False
#                     break
#
#
#             if flag == False:
#                 if val1['error'] == False:
#                     try:
#                         for form in val1['forms']:
#                             print form
#                             cardID = form_card(BASE_URL, headers1, form, zviceID, p_cardID)
#                             key = wfename + ":" + form
#                             # add_val_in_table(BASE_URL, headers1, key, cardID, zviceID)
#                             of.write(key + "," + str(cardID) + "\n")
#                             form_element = val1['forms'][form]
#                             time.sleep(500.0 / 1000.0);
#                             result = create_form_elements(BASE_URL, headers1, zviceID, cardID, form, form_element)
#                             print result
#                     except:
#                         logging.error("Sending error TRUE")
#             else:
#                 tcardname = tname
#                 icardDes = ""
#                 parentCardID = ""
#                 disallowcom = "false"
#                 publish = "true"
#                 p_cardID = CM.create_txt_card(tcardname, icardDes, zviceID, headers1, parentCardID, BASE_URL, disallowcom,publish)
#                 if val1['error'] == False:
#                     try:
#                         for form in  val1['forms']:
#                             print form
#                             cardID = form_card(BASE_URL,headers1,form,zviceID,p_cardID)
#                             key = wfename + ":" + form
#                             # add_val_in_table(BASE_URL, headers1, key, cardID, zviceID)
#                             of.write(key + "," + str(cardID) + "\n")
#                             form_element = val1['forms'][form]
#                             time.sleep(500.0 / 1000.0);
#                             result = create_form_elements(BASE_URL,headers1,zviceID,cardID,form,form_element)
#                             print result
#                             time.sleep(500.0 / 1000.0);
#                             input_data = {}
#                             result = CM.form_submission_using_NEW_API(BASE_URL,zviceID,headers1,cardID,input_data)
#                             print result
#                             tagName = form
#                             wid = 1
#                             sub_result = CM.add_tags_future(str(result),tagName,BASE_URL,zviceID,headers1,wid)
#                             print sub_result
#
#                     except:
#                         logging.error("Sending error TRUE")
