
import common as CM
import wfe_parser as WP
import logon as LL
import json
import sys
import logging
import re
import csv


BASE_URL = "http://twig-me.com/v13/"  ### dev server
email = "admin@zestl.com"
pwd = "TwigMeNow"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

# zviceID = "83H6LVUBRXWZ5"
# cardID = 70
#
# e_arr = []
# elem = {}
# # sid = str(alltag['cardID'])
# elem['label'] = "ABC"
# elem['type'] = "AUTO_COMPLETE"
# # elem['type'] = "EDIT_TEXT"
# elem['required'] = 0
# elem['placeholder'] = ""
# elem['editable'] = "false"
# elem['python'] = "2222202222202222"
# elem['values'] = 3
# e_arr.append(elem)
# print e_arr
# form = "Add Single User"
# # cardID = CM.form_card(BASE_URL, headers1, form, body['BusinessTag'], "")
# result = CM.create_form_elements(BASE_URL, headers1, zviceID, cardID, form, e_arr)
# print result



inp = '{"Cmd":"workflow-create","BusinessTag":"WHGJ7HTVTDFH3","WorkflowID":210,"WorkflowTypeID":1,"WorkflowTitle":"S214"}'
body = json.loads(inp)

hasHeader = "Y"

try:
    w_ID = body['FormData']['WorkflowID']
    w_ID = str(w_ID)
except:
    w_ID = 0

inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"

if body['Cmd'] == "workflow-create":

    tagName = "MKT_CONFIG:WFID_210"
    # result = CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1)
    result = json.loads(CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1))
    # print result

    for alltag in result['data']['elements']:

        with open(inputFile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            for row in data:
                tagName = "estimate::" + row[1] + ":WFID_" + str(body['WorkflowID'])
                print tagName
                result = json.loads(CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1))
                for alltag in result['data']['elements']:
                    if "Estimate" in alltag['allTags']:
                        sid = str(alltag['cardID'])
                        print sid
                        form_ID = 10
                        input_data = {"Standard Time":row[2],"Standard Resource":row[3],"Standard Cost":row[4]}
                        result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID, input_data,sid)
                        print result


#************************  updating "update estimated time form ******************#
        # if "Update estimated Time Form" in alltag['allTags']:
        #     data = json.loads(alltag['content'])
        #     for subelm in data['Elements'][0]['Elements']:
        #         s_id = subelm['MetaData']['PYTHON']
        #         estimate_value = subelm['Value']
        #         form_ID = 10
        #         input_data = {"Estimated Time": estimate_value}
        #         result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID, input_data,s_id)


#*************************************************************************#