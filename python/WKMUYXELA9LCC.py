##### Genepath


import common as CM
import wfe_parser as WP
import pandas as pd
import logon as LL
import json
import sys
import logging
import re
import csv
import datetime
from datetime import timedelta
import threading
import urllib2


threadLock = threading.Lock()
threads = []

class usualThread(threading.Thread):
    def __init__(self, threadID, val1, ele, body, BASE_URL, headers1, wfectr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.body = body
        self.val1 = val1
        self.BASE_URL = BASE_URL
        self.headers1 = headers1
        self.ele = ele
        self.wfectr = wfectr

    def run(self):
        logging.warning( "Starting " + str(self.threadID) + " " + str(self.ele))
        threadLock.acquire()
        create_usual_forms(self.val1, self.ele, self.body, self.BASE_URL, self.headers1, self.wfectr)
        threadLock.release()


class configThread(threading.Thread):
    def __init__(self, threadID, wfe, lisval, wfesparentID, parentID, filepath, filepath_server, body, BASE_URL, headers1):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.body = body
        self.wfe = wfe
        self.BASE_URL = BASE_URL
        self.headers1 = headers1
        self.lisval = lisval
        self.wfesparentID = wfesparentID
        self.filepath = filepath
        self.filepath_server = filepath_server
        self.parentID = parentID


    def run(self):
        logging.warning( "Starting " + str(self.threadID) + " " + str(self.wfe))
        threadLock.acquire()
        create_config_cards(self.wfe, self.lisval, self.wfesparentID, self.parentID, self.filepath, self.filepath_server, self.body, self.BASE_URL, self.headers1)
        threadLock.release()


class grpThread (threading.Thread):
    def __init__(self, threadID, body, flow, BASE_URL, headers1, parentID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.body = body
        self.flow = flow
        self.BASE_URL = BASE_URL
        self.headers1 = headers1
        self.parentID = parentID
    def run(self):
        logging.warning( "Starting " + str(self.threadID) + " " + self.flow)
        # Get lock to synchronize threads
        threadLock.acquire()
        cardIDs = create_user_grps(self.body, self.flow, self.BASE_URL, self.headers1, self.parentID)
        # logging.warning( cardIDs)
        # Free lock to release next thread
        threadLock.release()


class taskThread (threading.Thread):
    def __init__(self, threadID, s_id, val1, task, body, BASE_URL, headers1, taskTagname):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.body = body
        self.val1 = val1
        self.BASE_URL = BASE_URL
        self.headers1 = headers1
        self.s_id = s_id
        self.task = task
        self.taskTagname = taskTagname
    def run(self):
        logging.warning( "Starting " + str(self.threadID) + " " + str(self.task))
        # Get lock to synchronize threads
        threadLock.acquire()
        create_and_tag_task(self.s_id, self.val1, self.task, self.body, self.BASE_URL, self.headers1, self.taskTagname)
        # Free lock to release next thread
        threadLock.release()



class wfeThread (threading.Thread):
    def __init__(self, threadID, wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.body = body
        self.wfe = wfe
        self.BASE_URL = BASE_URL
        self.headers1 = headers1
        self.wfesparentID = wfesparentID
        self.filepath = filepath
        self.filepath_server = filepath_server
    def run(self):
        logging.warning( "Starting " + str(self.threadID) + " " + str(self.wfe))
        # Get lock to synchronize threads
        threadLock.acquire()
        create_worflow_elements(self.wfe, self.body, self.wfesparentID, self.filepath, self.filepath_server, self.BASE_URL, self.headers1, self.threadID)
        # Free lock to release next thread
        threadLock.release()



def user_addition_using_Form(body, BASE_URL, headers1):
    formID = body['FormID']
    if body['FormData']['User ID'] is None:
        sub_ID = body['FormSubmissionID']

        field_name = body['FormData']
        if "Doctor Name" in field_name:
            name = body['FormData']['Doctor Name']
            email_ID = body['FormData']['Doctor Email 1']
            grp_name = "Doctor"
            flag = 0

        elif "Employee Name" in field_name:
            name = body['FormData']['Employee Name']
            email_ID = body['FormData']['Employee Email']
            grp_name = "Employee"
            flag = 0

        elif "Patient Name" in field_name:
            name = body['FormData']['Patient Name']
            email_ID = ""
            grp_name = "Patient"
            flag = 1

        result = CM.add_user_InBusiness(body['BusinessTag'],name,email_ID, headers1, BASE_URL)
        jsonreply = json.loads(result)
        user_id = jsonreply['data']['usertagid']
        logging.warning("addition is done " + str(user_id))
        card_name = "Favourites"
        CM.hide_card(headers1, BASE_URL, user_id, card_name)
        card_name = "My Memberships"
        CM.hide_card(headers1, BASE_URL, user_id, card_name)
        card_name = "My Connections"
        CM.hide_card(headers1, BASE_URL, user_id, card_name)
        card_name = "Attendance"
        CM.hide_card(headers1, BASE_URL, user_id, card_name)
        CM.convertTo_Grid(BASE_URL,user_id,headers1)



        usergroups = CM.getAllUserGroups(headers1, body['BusinessTag'], BASE_URL, grp_name)
        grpvals = json.loads(usergroups)
        grps = grpvals['output']
        grpname = grps['usergroup']
        dict1 = grpname
        grpID = dict1[grp_name]
        g_ID = str(grpID)
        result = CM.add_user_to_group(g_ID,user_id,body['BusinessTag'], headers1, BASE_URL)
        logging.warning(result)
        if flag == 1:
            body["Contact"] = body['FormData']['Patient Phone No']
            body["EmailID"] = body['FormData']['Patient Email']
            method = "POST"
            url = BASE_URL + 'zvice/interaction/' + user_id
            body["interactionID"] = "CommonInteraction_INTERACTION_TYPE_MODIFY_CONTACT_INFO"
            jsonreply = CM.hit_url_method(body, headers1, method, url)
            logging.warning(jsonreply)
        else:logging.warning("we are not setting Contact details here")
        input_data = {"User ID": str(user_id)}
        result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, formID, input_data, sub_ID)
        logging.warning("resubmitting form")
        logging.warning(result)

    else:logging.warning("User is already created")


def create_worflow_element_filechain(wfe, body, wfesparentID, wfectr, cardList, testname,next_stage):
    #
    filename = filepath + wfe + ".csv"
    filename_server = filepath_server + wfe + ".csv"

    val1 = {}
    try:
        val1 = WP.parse_wfe(filename)
    except:
        val1 = WP.parse_wfe(filename_server)

    result = CM.create_txt_card(val1['desc'], "", body['BusinessTag'], headers1, wfesparentID, BASE_URL, "false","true")
    CardIds = str(result)
    tagName = body['WorkflowID']
    newtag = testname + ":WFID_" + str(tagName) + ", wfe:" + val1['name']
    result = CM.add_tags_future(CardIds, newtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
    CM.create_txt_card("dummy", "dummy", body['BusinessTag'], headers1, CardIds, BASE_URL, "true", "false")

    #### speed bedug comment
    # threadID = threadID + 1000
    # threads = []

    # val1['name'] = testname

    usualForms = ["Estimate", "Skip", "Dependency", "Status"]

    for ele in usualForms:
        # threadID = threadID + 1
        # threadname = "thread" + ele + val1['name']
        # threadname = usualThread(threadID, val1, ele, body, BASE_URL, headers1, wfectr)
        #
        # threadname.start()
        # threads.append(threadname)
        #
        create_usual_forms(val1, ele, body, BASE_URL, headers1, wfectr,next_stage)


        # ************** WFE specibody['BusinessTag']fic forms  submission ******#
    for k, v in val1['forms'].items():
        try:
            grp_name = v['AdminsR']
        except:
            grp_name = "N"
        form_key = val1['name'] + ":" + k

        try:
            try:
                if "Active" in body['FormData']['Status']:
                    fieldsmeta = json.dumps({"HideEditAction": False,"IsFormLinked": "true"})
                else:
                    fieldsmeta = json.dumps({"HideEditAction": False,"IsFormLinked": "true"})
            except:
                fieldsmeta = json.dumps({"HideEditAction": False,"IsFormLinked": "true"})

            result = CM.form_submission_using_NEW_API_meta(BASE_URL, body['BusinessTag'], headers1, cardList[form_key],
                                                           val1['forms'][k]['fields'], fieldsmeta)  # submitting form
        except:
            logging.warning("This is an illegal form submission " + form_key)
        s_id = str(result)
        # logging.warning(s_id)

        tagName = body['WorkflowID']
        cardtag = val1['name'] + ":WFID_" + str(tagName) + "," + k
        tagName = val1['name'] + ":" + val1['subFlow'] + ":WFID_" + str(tagName) + "," + k
        taskTagname = "task:" + tagName
        CM.add_tags_future(s_id, cardtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

        for task in v['taskList']:
            # threadID = threadID + 10000
            # threadname = "thread" + s_id + str(task)
            logging.error(" the task tag generated is  : " + taskTagname)
            create_and_tag_task(s_id, val1, task, body, BASE_URL, headers1, taskTagname)
            # threadname = taskThread(threadID, s_id, val1, task, body, BASE_URL, headers1, taskTagname)
            # threadname.start()
            # threads.append(threadname)

    # tagName = "IDAdmin:GenePath"
    # result = CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1)
    # for f_name in json.loads(result)['data']['elements']:
    #     if "ID Admin" in f_name['title']:
    #         sub_id = f_name['cardID']
    #         data = json.loads(f_name['content'])
    #         for e1 in data['Elements'][0]['Elements']:
    #             if "GPDx ID Prefix" in e1['FieldLabel']:
    #                 gpd_prefix = e1['Value']
    #             if "GPDx ID offset" in e1['FieldLabel']:
    #                 gpd_offset = e1['Value']
    #                 logging.warning("******************************")
    #                 logging.warning(gpd_offset)
    #             # if "Patient ID Prefix" in e1['FieldLabel']:
    #             #     patient_prefix = e1['Value']
    #             # if "Patient ID Offset" in e1['FieldLabel']:
    #             #     patient_offset = e1['Value']
    # gpd_offset = int(gpd_offset) + 1
    # logging.warning(gpd_offset)
    # logging.warning("********************************************")
    # form_ID = 6605
    # input_data = {"GPDx ID Prefix": gpd_prefix, "GPDx ID offset": str(gpd_offset)}
    # logging.warning(input_data)
    # result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID, input_data, sub_id)
    # logging.warning("End of work flow")
    # logging.warning(result)

    # form_ID = "6607"
    # # test_name = "Y chromosome microdeletions"
    # disease_name = body['FormData']['Test Performed'].strip()
    # disease_name = disease_name
    # body = {}
    # method = "GET"
    # url = BASE_URL + body['BusinessTag'] + "/forms/" + form_ID
    # jsonresponse = CM.hit_url_method(body, headers1, method, url)
    #
    # currentIdx = 1
    # for content in json.loads(jsonresponse)['data']['elements']:
    #     if content['cardtype'] == "formcard":
    #         data = json.loads(content['content'])
    #
    #         for elm in data['Elements'][0]['Elements']:
    #             if "Test performed" in elm['ElementID']:
    #                 if disease_name == elm['Value']:
    #                     val = json.loads(jsonresponse)['data']['elements'][currentIdx]
    #                     # data = val['content']
    #                     data_1 = json.loads(val['content'])
    #                     for elm_1 in data_1['Elements'][0]['Elements']:
    #                         if "Analytical Technique" in elm_1['ElementID']:
    #                             analytical_teq = elm_1['Value']
    #                         elif "MRP" in elm_1['ElementID']:
    #                             mrp = elm_1['Value']
    #                         elif "MoU prices" in elm_1['ElementID']:
    #                             mou = elm_1['Value']
    #                         elif "Therapeutic area" in elm_1['ElementID']:
    #                             therap_area = elm_1['Value']
    #                         elif "Seq capacity needed" in elm_1['ElementID']:
    #                             ngs_capacity = elm_1['Value']
    #                         elif "Outsource" in elm_1['ElementID']:
    #                             outsourced = elm_1['Value']
    #                         elif "Test No" in elm_1['ElementID']:
    #                             test_no = elm_1['Value']
    #                         elif "Test performed" in elm_1['ElementID']:
    #                             test_performed = elm_1['Value']
    #
    #         currentIdx = currentIdx + 1
    # try:
    #     tagName = "TOP:WFID_" + str(body['WorkflowID'])
    #     result = CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1)
    #     for f_name in json.loads(result)['data']['elements']:
    #         if "Additional Test Info Form" in f_name['title']:
    #             sub_id = f_name['cardID']
    #             additional_test_info = 5312
    #             input_data = {"Test No": test_no, "Analytical Technique": analytical_teq,
    #                           "Therapeutic area": therap_area, "Outsourced": outsourced,
    #                           "NGS Capacity Reqd": ngs_capacity}
    #             result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, additional_test_info, input_data,sub_id)
    #         elif "Billing Form" in f_name['title']:
    #             sub_id = f_name['cardID']
    #             billing_form_id = 5323
    #             input_data = {"MRP Charges": mrp, "MOU Charges": mou}
    #             result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, billing_form_id, input_data,sub_id)
    #         elif "Sample Reception form" in f_name['title']:
    #             sub_id = f_name['cardID']
    #             billing_form_id = 5319
    #             input_data = {"Sample Type": test_performed}
    #             result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, billing_form_id, input_data,sub_id)
    #         else:
    #             logging.warning("Not able to find any form")
    # except:
    #     logging.warning("some error nothing found")

    # for t in threads:
    #     t.join()

    return threads


def create_wfes_filechain(body):


    masterfileName = "wfe_spec_next.csv"

    masterFile =  filepath + masterfileName
    masterFile_server = filepath_server + masterfileName

    hasHeader = "Y"
    wfeList = {}
    try:

        with open(masterFile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            for row in data:
                if row[0] != "":
                    wfeList[row[0]] = []
                    for i in range(1, len(row)):
                        if row[i] is not "" and row[i] is not "END":
                            wfeList[row[0]].append(row[i])

    except:
        with open(masterFile_server, 'r') as rf:

            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            logging.warning(masterFile_server + "!!!!!!")
            for row in data:
                if row[0] != "":
                    wfeList[row[0]] = []
                    logging.warning("Got here @@@@@")
                    for i in range(1, len(row)):
                        logging.warning(row)
                        logging.warning(len(row))
                        logging.warning(i)
                        if row[i] is not "" and row[i] is not "END":
                            wfeList[row[0]].append(row[i])
                            logging.warning("Got here @@@@^^^@")

    # body['WorkflowID'] = body['FormData']['GPDx ID']

    # filepath = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/wfes/"
    # filepath_server = "/var/www/cgi-bin/workflow/wfes/"

    # standard_C_T_R = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
    logging.warning("Got here @@@@^^^@$$$$")


    standard_C_T_R_server = "/var/www/cgi-bin/workflow/WFE_Time_Cost.csv"
    standard_C_T_R = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/TwigMeScripts/python/WFE_Time_Cost.csv"

    cardIDlistFile = filepath + str(body['BusinessTag']) + "_form_tables.csv"
    cardIDlistFile_server = filepath_server + str(body['BusinessTag']) + "_form_tables.csv"
    ###### one wfe only below :::

    hasHeader = "Y"
    try:

        with open(cardIDlistFile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            cardList = {}
            for row in data:
                cardList[row[0]] = row[1]

    except:
        with open(cardIDlistFile_server, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            cardList = {}
            for row in data:
                cardList[row[0]] = row[1]



    elctrall = {}
    try:
        with open(standard_C_T_R, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            for row in data:
                elctr = {}
                wfekey = row[1]
                elctr['t'] = row[2]
                elctr['c'] = row[4]
                elctr['r'] = row[3]
                elctrall[wfekey] = elctr
    except:
        with open(standard_C_T_R_server, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            for row in data:
                elctr = {}
                wfekey = row[1]
                elctr['t'] = row[2]
                elctr['c'] = row[4]
                elctr['r'] = row[3]
                elctrall[wfekey] = elctr


    #
    # try:
    #     lisval = WP.parse_wfe_list(masterFile)
    # except:
    #     lisval = WP.parse_wfe_list(masterFile_server)

    result = CM.create_txt_card(str(body['WorkflowID']), "workflow_id container", body['BusinessTag'], headers1, "",
                                BASE_URL, "true", "false")
    parentID = str(result)

    CM.hide_card(headers1, BASE_URL, body['BusinessTag'], str(body['WorkflowID']))
    result = CM.create_txt_card((str(body['WorkflowID']) + "wfes"), "workflow_id container", body['BusinessTag'], headers1,
                                "", BASE_URL, "true", "false")
    wfesparentID = str(result)
    CM.hide_card(headers1, BASE_URL, body['BusinessTag'], (str(body['WorkflowID']) + "wfes"))

    ## ########## turning off for speed debug

    threadID = 0


    #************************************  MINAL Testing***********************************************

    try:
        # for flow in lisval['subflows']:
        #     threadID = threadID + 1
        #     threadname = "thread" + flow
        #     threadname = grpThread(threadID, body, flow, BASE_URL, headers1, parentID)
        #     threadname.start()
        #     threads.append(threadname)

        # testname = body['FormData']['Test Performed'].strip()

        #*******************************************  New code   FEB 7_12.21  *******************************************#
        testNumber = body['FormData']['Test No'].strip()
        form_ID = test_master_metadata
        method = "POST"
        url = BASE_URL + "search/" + body['BusinessTag'] + "/forms/" + form_ID + "/submissions"
        b = [{"FieldLabel": "Test No.", "Value": testNumber}]
        jsonresponse = CM.hit_url_method(b, headers1, method, url)
        logging.warning(jsonresponse)
        for testno in json.loads(jsonresponse)['data']['result']:
            if testno['Test No.'] == testNumber:
                testname = testno['Test performed']
                analytical_teq = testno['Analytical Technique']
                mrp = testno['MRP']
                mou = testno['MoU prices']
                therap_area = testno['Therapeutic area']
                ngs_capacity = testno['Seq capacity needed']
                outsourced = testno['outsource']
                test_no = testno['Test No.']
                # sample_req = testno['Sample required']
                tat = testno['TAT(days)']


            logging.warning(testname)

        containername = "LAB"
        # logging.warning(testname)

        create_user_grps(body, containername, BASE_URL, headers1, parentID)

    except:
        logging.warning("No subflow was defined")


    try:
        i = 0
        # lisval = wfeList[testname].reverse()
        wfeList[testname].reverse()
        for wfe in wfeList[testname]:
            if wfe == "END":
                continue
            else:
                next_stage = wfeList[testname][i]
                i = i + 1
                # threadID = threadID  + 10000

                logging.warning(wfe)
                logging.warning("------------------------")

                wfectr = {}
                try:
                    wfectr = elctrall[wfe]
                except:
                    wfectr = {"c" : "", "t" : "", "r" : ""}


                create_worflow_element_filechain(wfe, body, wfesparentID, wfectr, cardList, containername,next_stage)

        create_config_cards("LAB", wfeList[testname], wfesparentID, parentID, filepath, filepath_server, body, BASE_URL, headers1)


        try:
            tagName = "TOP:WFID_" + str(body['WorkflowID'])
            result = CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1)
            logging.warning(result)
            for f_name in json.loads(result)['data']['elements']:
                if "Additional Test Info Form" in f_name['title']:
                    sub_id = f_name['cardID']
                    # additional_test_info = 5312
                    form_ID = additional_test_info
                    input_data = {"Test No": test_no, "Analytical Technique": analytical_teq,"Therapeutic area": therap_area, "Outsourced": outsourced,
                                  "NGS Capacity Reqd": ngs_capacity, "TAT": tat}
                    result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1,form_ID, input_data, sub_id)
                    logging.warning(result)
                elif "Billing Form" in f_name['title']:
                    sub_id = f_name['cardID']
                    # billing_form_id = 5323
                    form_ID = billing_form_id
                    input_data = {"MRP Charges": mrp, "MOU Charges": mou}
                    result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID,input_data, sub_id)
                    logging.warning(result)
                # elif "Sample Reception form" in f_name['title']:
                #     sub_id = f_name['cardID']
                #     # sample_reception_form = 5319
                #     form_ID = sample_reception_form
                #     input_data = {"Sample Type": sample_req}
                #     result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID,input_data, sub_id)
                #     logging.warning(result)
                else:
                    logging.warning("Not able to find any form")

            tagName = "TOP:WFID_" + str(body['WorkflowID'])
            result = CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1)
            logging.warning("********************************   I WANT THIS RESPONSE   *******************************")
            logging.warning(result)
            logging.warning("********************************  I GOT THE RESPONSE    *********************************")
            for f_name in json.loads(result)['data']['elements']:
                if "Sample Reception form" in f_name['title']:
                    data_1 = json.loads(f_name['content'])
                    for elm_1 in data_1['Elements'][0]['Elements']:
                        if "Sample Received Date" in elm_1['ElementID']:
                            s_date = elm_1['Value']
                elif "Additional Test Info Form" in f_name['title']:
                    data_1 = json.loads(f_name['content'])
                    for elm_1 in data_1['Elements'][0]['Elements']:
                        if elm_1['ElementID'] == "TAT":
                            tat = elm_1['Value']

            date_1 = datetime.datetime.strptime(s_date, "20%y-%m-%d")
            end_date = date_1 + datetime.timedelta(days=int(tat))
            end_date = str(end_date)
            details = end_date.split(' ')
            abc = details[0].strip()
            for f_name in json.loads(result)['data']['elements']:
                if "Test Status form" in f_name['title']:
                    sub_id = f_name['cardID']
                    # test_status_form = "5315"
                    form_ID = test_status_form
                    input_data = {"Report Estimated Date": str(abc)}
                    logging.warning(input_data)
                    result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID, input_data, sub_id)
                    logging.warning("Date updated successfully")


        except:
            logging.warning("some error nothing found")


        #***************************************************************************************************************************#


    except:
        logging.error("!!!!!!!!!  Illegal Test name   !!!!!!!!")

        # threadname = "thread" + wfe
        # threadname = wfeThread(threadID, wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1)
        # threadname.start()
        # threads.append(threadname)
    #
    # for t in threads:
    #     t.join()
    #
    #
    # logging.warning(str(lisval))
    # threads1 = []
    #
    # for wfe in lisval['deptwfes']:
    #     # threadID = 15000
    #     # threadname = "thread" + wfe
    #     # logging.warning(" firing off the thread " +  wfe)
    #     # threadname = configThread(threadID, wfe, lisval, wfesparentID, parentID, filepath, filepath_server, body, BASE_URL, headers1)
    #     create_config_cards(wfe, lisval, wfesparentID, parentID, filepath, filepath_server, body, BASE_URL, headers1)
    #     #
    # #     threadname.start()
    # #     logging.warning(" starting off the thread " +  wfe)
    # #
    # #     threads1.append(threadname)
    # #
    # #     # create_config_cards(wfe, lisval, wfesparentID, filepath, filepath_server, body, BASE_URL, headers1)
    # #
    # # logging.warning(threads1)
    # # for t in threads1:
    # #     t.join()



def startTestFlow(body):

    create_wfes_filechain(body)
    # print body



def find_skip_in_nextFlow(depTagname, BASE_URL, zviceID, headers1, skipTag,wfid, nxtstages):
    # next_stage_array = []
    cards = CM.get_all_tagIds(depTagname, BASE_URL, zviceID, headers1)
    try:
        cards = json.loads(cards)
        contents = cards['data']['elements'][0]['content']
        contents = json.loads(contents)
        for a in contents['Elements'][0]['Elements']:
            if "Next Stage" in a['ElementID']:
                logging.warning("checking next stage")
                nextstage = a['Value']
                nextstages = nextstage.split(";")
                for stage in nextstages:
                    logging.warning("these are stages")
                    logging.warning(stage)
                    stage = stage.strip()
                    if "END" in stage:
                        logging.warning("END stage in stage")
                        # nextstage = "END"
                        # return nextstage
                        nxtstages.append(stage)
                        logging.warning("Last stage")
                        ## do nothing
                    else:
                        s_tag = "skip::" + stage + ":WFID_" + str(wfid)
                        result = CM.get_all_tagIds(s_tag, BASE_URL, zviceID, headers1)
                        for s_card in json.loads(result)['data']['elements']:
                            if "Skip" in s_card['allTags']:
                                for el in json.loads(s_card['content'])['Elements'][0]['Elements']:
                                    if "SKIP" in el['FieldLabel']:
                                        if el['Value'] == "true":
                                            tag_b = "backend::" + stage + ":WFID_" + str(wfid)
                                            s_tag = "skip::" + stage + ":WFID_" + str(wfid)
                                            find_skip_in_nextFlow(tag_b, BASE_URL, zviceID, headers1, s_tag, wfid,nxtstages)

                                        else :
                                            # next_stage_array.append(nextstage)
                                            nxtstages.append(stage)
                return nxtstages


    except:logging.warning("No content found")






def complete_wfe_NEW(tagName1, wfid, BASE_URL, body, headers1):
    # filepath = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/wfes/"
    # filepath_server = "/var/www/cgi-bin/workflow/wfes/wfes_GenePath/"

    depTagname = "backend::" + tagName1
    skipTag = "skip::" + tagName1

    tags = tagName1.split(":")
    subname = tags[0]
    wfidtag = tags[1]
    wfids = wfidtag.split("_")
    wfid = wfids[1]

    filename = filepath + subname + ".csv"
    filename_server = filepath_server + subname + ".csv"

    val1 = {}
    try:
        val1 = WP.parse_wfe(filename)
    except:
        val1 = WP.parse_wfe(filename_server)

#****************************************  New SKIP code 19 FEB 1.47  ****************************************************************
    nextstages = []
    nextstages = find_skip_in_nextFlow(depTagname, BASE_URL, body['BusinessTag'], headers1, skipTag, wfid, nextstages)
#************************************************************************************************************************

    ### use tagname1 wfdename:wfid_xx to get the wfe contents from wfe_parser. send messages to the comm pref and use other values correctly.
    #### where to get the project name from? top form?

#******************************* New SKIP code 19 FEB 1.47 ***********************************************************
    # cards = CM.get_all_tagIds(depTagname, BASE_URL, body['BusinessTag'], headers1)
    # try:
    #     cards = json.loads(cards)
    #     contents = cards['data']['elements'][0]['content']
    #     contents = json.loads(contents)
    #     for a in contents['Elements'][0]['Elements']:
    #         if re.search("Next stage", a['ElementID'], re.IGNORECASE):
    #             nextstage = a['Value']
    #             nextstages = nextstage.split(";")
#***************************************************************************************************************
    try:

        for stage in nextstages:
            stage = stage.strip()
            if "END" in stage:
                logging.warning("Last stage")
                ## do nothing
            else:

                st = stage.split('_')
                st = st[0]

                ### fetch cards of next stage with tag

                tagstage = stage + ":WFID_" + wfid
                ###  Fetch the cards
                result = CM.get_all_tagIds(tagstage, BASE_URL, body['BusinessTag'], headers1)

                EntryFlag = False
                for card in json.loads(result)['data']['elements']:
                    if "Entry Checklist" in card['allTags']:
                        EntryFlag = True

                if EntryFlag:
                    logging.warning("entry checklist available in next stage")
                else:
                    filename = filepath + stage + ".csv"
                    filename_server = filepath_server + stage + ".csv"

                    val2 = {}
                    try:
                        val2 = WP.parse_wfe(filename)
                    except:
                        val2 = WP.parse_wfe(filename_server)

                    for status_card in json.loads(result)['data']['elements']:
                        if "Status" in status_card['allTags']:
                            # form_key = "Status Form F5"
                            # value = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1,
                            #                                           body['BusinessTag'], form_key)
                            # value = json.loads(value)
                            # form_ID = value['data']['value']['_value']
                            form_ID = cardList['Status']
                            s_id = status_card['cardID']
                            input_data = {"Status": "Active"}
                            result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'],
                                                                      headers1, form_ID, input_data,s_id)

                            #****************   Top form status change *******************
                            tag = "TOP:WFID_" + str(wfid)
                            form_Name = "Test Status form"
                            # filter_form = "Filter form"
                            result = CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'], headers1)
                            for f_name in json.loads(result)['data']['elements']:
                                if form_Name in f_name['title']:
                                    sub_ID = f_name['cardID']
                                    lab_stage_message = val2['desc']
                                    input_data = {"Lab Stage": lab_stage_message}
                                    # form_ID = 5315
                                    form_ID = test_status_form
                                    result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'],headers1,form_ID, input_data, sub_ID)
                                    logging.warning(result)

    except:
        logging.warning("no contents found")

    try:
        commgroups = val1['Comm'].split(";")
        commgrps_corrected = []
        for grp in commgroups:
            grps = grp.split("_")
            correctName = grps[0] + "_" + wfid
            commgrps_corrected.append(str(correctName))
        b = {}
        b['title'] = "Workflow step complete"
        b['msg'] = "workflow step  " + val1['desc'] + " of workflow " + " ##placeholder for now## " + "is completed"
        b['commtype'] = ["NOTIFY"]
        b['groupname'] = commgrps_corrected
        # b['CardID'] = "63858"

        method = "POST"
        url = BASE_URL + "usergroups/message/" + body['BusinessTag']

        resp = CM.hit_url_method(b, headers1, method, url)
        logging.warning(resp)
    except:
        logging.warning("sending of completion message failed")



def complete_wfe(tagName1, wfid, BASE_URL, body, headers1):
    # filepath = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/wfes/"
    # filepath_server = "/var/www/cgi-bin/workflow/wfes/wfes_GenePath/"

    depTagname = "backend::" + tagName1

    tags = tagName1.split(":")
    subname = tags[0]
    wfidtag = tags[1]
    wfids = wfidtag.split("_")
    wfid = wfids[1]

    filename = filepath + subname + ".csv"
    filename_server = filepath_server + subname + ".csv"

    val1 = {}
    try:
        val1 = WP.parse_wfe(filename)
    except:
        val1 = WP.parse_wfe(filename_server)





    ### use tagname1 wfdename:wfid_xx to get the wfe contents from wfe_parser. send messages to the comm pref and use other values correctly.
    #### where to get the project name from? top form?
    cards = CM.get_all_tagIds(depTagname, BASE_URL, body['BusinessTag'], headers1)
    try:
        cards = json.loads(cards)
        contents = cards['data']['elements'][0]['content']
        contents = json.loads(contents)
        for a in contents['Elements'][0]['Elements']:
            if re.search("Next stage", a['ElementID'], re.IGNORECASE):
                nextstage = a['Value']
                nextstages = nextstage.split(";")
                for stage in nextstages:
                    stage = stage.strip()
                    if "END" in stage:
                        logging.warning("Last stage")
                        ## do nothing
                    else:

                        st = stage.split('_')
                        st = st[0]

                        ### fetch cards of next stage with tag

                        tagstage = stage + ":WFID_" + wfid
                        ###  Fetch the cards
                        result = CM.get_all_tagIds(tagstage, BASE_URL, body['BusinessTag'], headers1)

                        EntryFlag = False
                        for card in json.loads(result)['data']['elements']:
                            if "Entry Checklist" in card['allTags']:
                                EntryFlag = True

                        if EntryFlag:
                            logging.warning("entry checklist available in next stage")
                        else:
                            filename = filepath + stage + ".csv"
                            filename_server = filepath_server + stage + ".csv"

                            val2 = {}
                            try:
                                val2 = WP.parse_wfe(filename)
                            except:
                                val2 = WP.parse_wfe(filename_server)

                            for status_card in json.loads(result)['data']['elements']:
                                if "Status" in status_card['allTags']:
                                    # form_key = "Status Form F5"
                                    # value = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1,
                                    #                                           body['BusinessTag'], form_key)
                                    # value = json.loads(value)
                                    # form_ID = value['data']['value']['_value']
                                    form_ID = cardList['Status']
                                    s_id = status_card['cardID']
                                    input_data = {"Status": "Active"}
                                    result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'],
                                                                              headers1, form_ID, input_data,s_id)

                                    #****************   Top form status change *******************
                                    tag = "TOP:WFID_" + str(wfid)
                                    form_Name = "Test Status form"
                                    # filter_form = "Filter form"
                                    result = CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'], headers1)
                                    for f_name in json.loads(result)['data']['elements']:
                                        if form_Name in f_name['title']:
                                            sub_ID = f_name['cardID']
                                            lab_stage_message = val2['desc']
                                            input_data = {"Lab Stage": lab_stage_message}
                                            # form_ID = 5315
                                            form_ID = test_status_form
                                            result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'],headers1,form_ID, input_data, sub_ID)
                                            logging.warning(result)
                                    #
                                    # for f_name in json.loads(result)['data']['elements']:
                                    #     if filter_form in f_name['title']:
                                    #         sub_ID = f_name['cardID']
                                    #         lab_stage_message = val2['desc']
                                    #         input_data = {"Lab Stage": lab_stage_message}
                                    #         form_ID = 5320
                                    #         result = CM.EDIT_submission_using_NEW_API(BASE_URL,body['BusinessTag'],headers1, form_ID,input_data, sub_ID)
                                    #         logging.warning(result)
                                    #******************************************************************************
    except:
        logging.warning("no contents found")

    try:
        commgroups = val1['Comm'].split(";")
        commgrps_corrected = []
        for grp in commgroups:
            grps = grp.split("_")
            correctName = grps[0] + "_" + wfid
            commgrps_corrected.append(str(correctName))
        b = {}
        b['title'] = "Workflow step complete"
        b['msg'] = "workflow step  " + val1['desc'] + " of workflow " + " ##placeholder for now## " + "is completed"
        b['commtype'] = ["NOTIFY"]
        b['groupname'] = commgrps_corrected
        # b['CardID'] = "63858"

        method = "POST"
        url = BASE_URL + "usergroups/message/" + body['BusinessTag']

        resp = CM.hit_url_method(b, headers1, method, url)
        logging.warning(resp)
    except:
        logging.warning("sending of completion message failed")



def check_for_exit_checklist_in_stage(wfidtag, body, BASE_URL, headers1):
    result = CM.get_all_tagIds(wfidtag, BASE_URL, body['BusinessTag'], headers1)
    flag = False
    for sub_mission in json.loads(result)['data']['elements']:
        if "Exit Checklist" in sub_mission['allTags']:
            flag = True
    return flag

def check_alltasks_complete(tasktag, body, BASE_URL, headers1):
    value = CM.get_all_tagIds(tasktag, BASE_URL, body['BusinessTag'], headers1)
    taskID_array = []
    v = json.loads(value)
    completeFlag = True
    for t_val in json.loads(value)['data']['elements']:
        if "Completed" in t_val['status']:
            continue
        else:
            completeFlag = False
    return completeFlag

def set_wfe_status(tagName1, status, body, BASE_URL, headers1):
    result = CM.get_all_tagIds(tagName1,BASE_URL,body['BusinessTag'],headers1)
    for status_card in json.loads(result)['data']['elements']:
        if "Status" in status_card['allTags']:
            # form_key = "Status Form F5"
            # value = CM.get_formID_using_KEY_Value_API(BASE_URL,headers1,body['BusinessTag'],form_key)
            # value = json.loads(value)
            # form_ID = value['data']['value']['_value']
            form_ID = cardList['Status']
            s_id = status_card['cardID']
            input_data = {"Status" : status}
            result = CM.EDIT_submission_using_NEW_API(BASE_URL,body['BusinessTag'],headers1,form_ID,input_data,s_id)


def create_worflow_elements(wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1, threadID, threads, wfectr, cardList,next_stage):
    #
    filename = filepath + wfe + ".csv"
    filename_server = filepath_server + wfe + ".csv"


    val1 = {}
    try:
        val1 = WP.parse_wfe(filename)
    except:
        val1 = WP.parse_wfe(filename_server)
#*********************** Commented****************
    if "TOP_WFE" in val1['desc']:
        logging.warning("TOP_WFE detected")
    else:
#**************************************************
        result = CM.create_txt_card(val1['desc'], "", body['BusinessTag'], headers1, wfesparentID, BASE_URL, "false","true")
        CardIds = str(result)
        tagName = body['WorkflowID']
        newtag = val1['subFlow'] + ":WFID_" + str(tagName) + ", wfe:" + val1['name']
        result = CM.add_tags_future(CardIds, newtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
        CM.create_txt_card("dummy", "dummy", body['BusinessTag'], headers1, CardIds, BASE_URL, "true", "false")


        #### speed bedug comment
        threadID = threadID + 1000
        threads = []

        usualForms = ["Estimate", "Skip", "Dependency", "Status"]

        for ele in usualForms:

            # threadID = threadID + 1
            # threadname = "thread" + ele + val1['name']
            # threadname = usualThread(threadID, val1, ele, body, BASE_URL, headers1, wfectr)
            #
            # threadname.start()
            # threads.append(threadname)

            create_usual_forms(val1, ele, body, BASE_URL, headers1, wfectr,next_stage)


        # ************** WFE specibody['BusinessTag']fic forms  submission ******#
    for k, v in val1['forms'].items():
        try:
            grp_name = v['AdminsR']
        except:
            grp_name = "N"
        form_key = val1['name'] + ":" + k
        try:
            try:
                if "Active" in body['FormData']['Status'] :
                    fieldsmeta = json.dumps({"HideEditAction": False})
                else:
                    fieldsmeta = json.dumps({"HideEditAction": False})
            except:
                fieldsmeta = json.dumps({"HideEditAction": False})


            # if k == "Filter form":
            #     input_data = {}
            #     input_data['GPDx ID'] = str(body['FormData']['GPDx ID'])
            #     input_data['Patient Name'] = body['FormData']['Patient Name']
            #     input_data['Priority'] = body['FormData']['Priority']
            #     input_data['wid'] = str(body['FormData']['GPDx ID'])
            #     result = CM.form_submission_using_NEW_API_meta(BASE_URL, body['BusinessTag'], headers1,cardList[form_key],input_data, fieldsmeta)
            # else:
            result = CM.form_submission_using_NEW_API_meta(BASE_URL, body['BusinessTag'], headers1, cardList[form_key],
                                                               val1['forms'][k]['fields'], fieldsmeta)  # submitting form
        except:
            logging.warning("This is an illegal form submission " + form_key)
        s_id = str(result)
        # logging.warning(s_id)
#************************************** Commented for debug ******************************
        if "TOP_WFE" in val1['desc']:
            nom = "TOP"
        else:
            nom = val1['name']
#******************************************************************************************

        tagName = body['WorkflowID']
        # cardtag = val1['name'] + ":WFID_" + str(tagName) + "," + k
        # tagName = val1['name'] + ":" + val1['subFlow'] + ":WFID_" + str(tagName) + "," + k
        cardtag = nom + ":WFID_" + str(tagName) + "," + k
        tagName = nom + ":" + val1['subFlow'] + ":WFID_" + str(tagName) + "," + k
        taskTagname = "task:" + tagName
        CM.add_tags_future(s_id, cardtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])


        for task in v['taskList']:
            # threadID = threadID + 10000
            # threadname = "thread" + s_id + str(task)
            logging.error(" the task tag generated is  : " + taskTagname)
            create_and_tag_task(s_id, val1, task, body, BASE_URL, headers1, taskTagname)
            # threadname = taskThread(threadID, s_id, val1, task, body, BASE_URL, headers1, taskTagname)
            # threadname.start()
            # threads.append(threadname)

    tagName = "IDAdmin:GenePath"
    result = CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1)
    for f_name in json.loads(result)['data']['elements']:
        if "ID Admin" in f_name['title']:
            ID_Admin_SubmissionId = f_name['cardID']
            data = json.loads(f_name['content'])
            for e1 in data['Elements'][0]['Elements']:
                if "GPDx ID Prefix" in e1['FieldLabel']:
                    gpd_prefix = e1['Value']
                if "GPDx ID offset" in e1['FieldLabel']:
                    gpd_offset = e1['Value']
                if "Patient ID Prefix" in e1['FieldLabel']:
                    patient_prefix = e1['Value']

    tagName = "TOP:WFID_" + str(body['WorkflowID'])
    result = CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1)
    flag = "N"
    for f_name in json.loads(result)['data']['elements']:
        if "Patient Initiation Form" in f_name['title']:
            sub_id = f_name['cardID']
            data = json.loads(f_name['content'])
            for e1 in data['Elements'][0]['Elements']:
                if "Patient Name (If Existing Patient)" in e1['FieldLabel']:
                    existing_patient_name = e1['Value']
                    if existing_patient_name != "":
                        flag = "Y"
                        patient_ID = existing_patient_name
                        decurl = BASE_URL + "push/dectest/" + patient_ID
                        response = urllib2.urlopen(decurl)
                        html = response.read()
                        decTag = json.loads(html)['decTagID']
                        val = decTag % 1000000
                        patient_ID = ('{:06}'.format(val))
                        patient_ID = patient_prefix + str(patient_ID)
                        logging.warning(patient_ID)
                    else:
                        logging.warning("it is empty")

            val_1 = int(gpd_offset) + 1
            val = ('{:06}'.format(val_1))
            val_2 = gpd_prefix + str(val)
            input_data = {"GPDx ID": val_2}
            # form_ID = 5322
            form_ID = patient_initiation_form
            # cardList[form_key]
            result_1 = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID, input_data,sub_id)
            logging.warning(result_1)


    gpd_val = int(gpd_offset) + 1

    # tagName = "TOP:WFID_" + str(body['WorkflowID'])
    # result = CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1)
    for f_name in json.loads(result)['data']['elements']:
        if "ID Tracking" in f_name['title']:
            val = ('{:06}'.format(gpd_val))
            gpd_val = gpd_prefix + str(val)
            sub_id = f_name['cardID']
            # form_ID = 6606
            form_ID = id_tracking
            if flag == "N":
                input_data = {"GPDx ID": gpd_val}
            else:
                input_data = {"GPDx ID": gpd_val, "Patient ID": patient_ID}
            result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID, input_data,sub_id)
            logging.warning(result)

        # form_ID = 6605
        form_ID = id_admin
        input_data = {"GPDx ID Prefix": gpd_prefix, "GPDx ID offset": str(val_1)}
        logging.warning(input_data)
        result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID, input_data, ID_Admin_SubmissionId)
        logging.warning("End of work flow")
        logging.warning(result)

    # for t in threads:
    #     t.join()

    return threads

def create_and_tag_task(s_id, val1, task, body, BASE_URL, headers1, taskTagname):

    logging.warning(val1)
    logging.warning(taskTagname)
    logging.warning(s_id)
    logging.warning(task)
    logging.warning(body)

    try:
        tagnames = taskTagname.split(",")
        for tag1 in tagnames:
            tag2 = tag1.split(":")
            # logging.warning(str(tag2))
            if len(tag2) == 4:
                toptag = "TOP:" + tag2[3]
                wfid_keyVal = tag2[3].split("_")
                wfid_keyVal = wfid_keyVal[1]
        logging.warning(toptag)
    except:
        logging.warning("eureka")

    try:
        task_priority = body['FormData']['Project Priority?']
        # task_priority = priority
        if task_priority == "1 (Highest)":
            priority = "Priority1"
        elif task_priority == "2":
            priority = "Priority2"
        elif task_priority == "3":
            priority = "Priority3"
        elif task_priority == "4":
            priority = "Priority4"
        elif task_priority == "5 (Lowest)":
            priority = "Priority5"
    except:
        try:
            result = json.loads(CM.get_all_tagIds(toptag, BASE_URL, body['BusinessTag'], headers1))
            result = json.loads(result['data']['elements'][0]['content'])
            for el in result['Elements'][0]['Elements']:
                if "Project Priority" in el['FieldLabel']:
                    priority = el['Value']

            task_priority = priority
            if task_priority == "1 (Highest)":
                priority = "Priority1"
            elif task_priority == "2":
                priority = "Priority2"
            elif task_priority == "3":
                priority = "Priority3"
            elif task_priority == "4":
                priority = "Priority4"
            elif task_priority == "5 (Lowest)":
                priority = "Priority5"

        except:
            logging.error("Priority error")
            priority = "Priority3"

    response = CM.create_task_for_workflow(BASE_URL, body['BusinessTag'], headers1, s_id, task, val1['subFlow'],priority)

    # response = CM.create_task_for_workflow(BASE_URL, body['BusinessTag'], headers1, s_id, task, val1['subFlow'])
    logging.warning(taskTagname)
    if response['error'] == False:
        t_id = str(response['taskID'])
        keyname = "tasksOf" + s_id
        try:
            writeVal = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], keyname)
            result = json.loads(writeVal)
            form_id = result['data']['value']['_value']
            writeVal = form_id + "," + t_id

            CM.add_val_in_table(BASE_URL, headers1, keyname, writeVal, body['BusinessTag'],int(wfid_keyVal))

        except:
            writeVal = t_id
            CM.add_val_in_table(BASE_URL, headers1, keyname, writeVal, body['BusinessTag'],int(wfid_keyVal))

        logging.warning("The task ID written in table was " + writeVal)

        resp = CM.add_tags_future(t_id, taskTagname, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

def create_user_grps(body, flow, BASE_URL, headers1, parentID):
    tagName = body['WorkflowID']
    tagNameTop = "WFID_" + str(tagName)
    grpname = flow + "p_" + str(tagName)
    try:
        newgrpID = CM.create_groups(grpname, flow + " group for project", headers1, body['BusinessTag'], BASE_URL)
        grp_name = "Manasi"
        grp_ID = CM.find_out_grp_ID(grp_name, headers1, body['BusinessTag'], BASE_URL)
        by = {'grpUserGroupID': grp_ID}
        CM.add_usergrps_grps(BASE_URL, json.dumps(by), headers1, body['BusinessTag'], newgrpID)
    except:
        logging.error("could not create user group " + flow + str(body['WorkflowID']))
    try:
        grp_name = flow + "mgr"
        grp_ID = CM.find_out_grp_ID(grp_name, headers1, body['BusinessTag'], BASE_URL)
        by = {'grpUserGroupID': grp_ID}
        CM.add_usergrps_grps(BASE_URL, json.dumps(by), headers1, body['BusinessTag'], newgrpID)

    except:
        logging.error("could not add manager group ")

    result = CM.create_txt_card(flow, "", body['BusinessTag'], headers1, parentID, BASE_URL, "false", "true")
    CardIds = str(result)

    tagnames = tagNameTop + "," + "subflow:" + flow
    CM.add_tags_future(CardIds, tagnames, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
    CM.create_txt_card("dummy", "dummy", body['BusinessTag'], headers1, CardIds, BASE_URL, "true", "false")
    return CardIds

def create_usual_forms(val1, ele, body, BASE_URL, headers1, wfectr,next_stage):
    tagName1 = val1['name'] + ":WFID_" + str(body['WorkflowID']) + "," + ele
    form_key = ele



    usuallistFile = filepath + str(body['BusinessTag']) + "_usualform_tables.csv"
    usuallistFile_server = filepath_server + str(body['BusinessTag']) + "_usualform_tables.csv"
    ###### one wfe only below :::

    hasHeader = "Y"
    try:

        with open(usuallistFile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            cardList = {}
            for row in data:
                cardList[row[0]] = row[1]

    except:
        with open(usuallistFile_server, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            cardList = {}
            for row in data:
                cardList[row[0]] = row[1]


    try:
        # result = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'],
        #                                            form_key)  # gettings key value pair

        ### change this to read from the xls.

        # result = json.loads(result)
        form_id = cardList[ele]
    except:
        logging.error("such a form does not exist" + ele)
        form_id = ""

    if ele == "Estimate":
        try:
            fields = val1['estimates']
            fields['Standard Cost'] = wfectr['c']
            fields['Standard Time'] = wfectr['t']
            fields['Standard Resource'] = wfectr['r']

        except:
            fields = {}
        # depTagname = "estimate::" + tagName1 ### enable this one for prod
        depTagname = "estimate::" + tagName1 + "," + tagName1
        # fieldsmeta = json.dumps({"HideEditAction": True})
        result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_id, fields)
        CM.add_tags_future(str(result), depTagname, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])


    if ele == "Skip":
        fieldname = {}
        try:
            fieldname['SKIP'] = val1['Skip']
        except:
            fieldname['SKIP'] = "false"
        fields = fieldname
        skiptag = "skip::" + tagName1 + "," + tagName1
        result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_id, fields)
        CM.add_tags_future(str(result), skiptag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])


    if ele == "Status":
        fieldname = {}
        try:
            fieldname['Status'] = val1['status']
        except:
            fieldname['Status'] = "Not Started"
        fields = fieldname

        fieldsmeta = json.dumps({"HideEditAction": False})

        # try:
        #     if "Active" in body['FormData']['Status']:
        #         fieldsmeta = json.dumps({"HideEditAction": False})
        #     else:
        #         fieldsmeta = json.dumps({"HideEditAction": True})
        # except:
        #     fieldsmeta = json.dumps({"HideEditAction": True})
        result = CM.form_submission_using_NEW_API_meta(BASE_URL, body['BusinessTag'], headers1, form_id, fields, fieldsmeta)
        CM.add_tags_future(str(result), tagName1, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

    if ele == "Dependency":
        try:
            # fields = []
            fieldname = {}
            fieldname['Next Stage'] = next_stage
            fields = fieldname
        except:
            fields = {}
        # try:
        #     fields = val1['dependencies']
        # except:
        #     fields = []
        depTagname = "backend::" + tagName1 ### enable this one for prod
        # depTagname = "backend::" + tagName1 + "," + tagName1
        result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_id, fields)
        CM.add_tags_future(str(result), depTagname, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

    # return firstelemFlag


def create_wfes(body, masterfileName, headers1, BASE_URL):
    threads = []

    body['WorkflowID'] = body['FormData']['wid']

    # filepath = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/wfes/"
    # filepath_server = "/var/www/cgi-bin/workflow/wfes/"
    masterFile =  filepath + masterfileName
    masterFile_server = filepath_server + masterfileName
    # standard_C_T_R = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
    standard_C_T_R = "/var/www/cgi-bin/workflow/WFE_Time_Cost.csv"
    # standard_C_T_R = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/TwigMeScripts/python/WFE_Time_Cost.csv"
    # body['BusinessTag']

    cardIDlistFile = filepath + str(body['BusinessTag']) + "_form_tables.csv"
    cardIDlistFile_server = filepath_server + str(body['BusinessTag']) + "_form_tables.csv"
    # ###### one wfe only below :::
    #
    hasHeader = "Y"
    try:

        with open(cardIDlistFile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            cardList = {}
            for row in data:
                cardList[row[0]] = row[1]

    except:
        with open(cardIDlistFile_server, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            cardList = {}
            for row in data:
                cardList[row[0]] = row[1]



    elctrall = {}
    with open(standard_C_T_R, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        if hasHeader == "Y":
            row1 = data.next()
        for row in data:
            elctr = {}
            wfekey = row[1]
            elctr['t'] = row[2]
            elctr['c'] = row[4]
            elctr['r'] = row[3]
            elctrall[wfekey] = elctr





    try:
        lisval = WP.parse_wfe_list(masterFile)
    except:
        lisval = WP.parse_wfe_list(masterFile_server)


    #### check for pre-existence of the said card - if yes - Don't create

    result = CM.create_txt_card(str(body['WorkflowID']), "workflow_id container", body['BusinessTag'], headers1, "",
                                BASE_URL, "true", "false")
    parentID = str(result)

    CM.hide_card(headers1, BASE_URL, body['BusinessTag'], str(body['WorkflowID']))
    result = CM.create_txt_card((str(body['WorkflowID']) + "wfes"), "workflow_id container", body['BusinessTag'], headers1,
                                "", BASE_URL, "true", "false")
    wfesparentID = str(result)
    CM.hide_card(headers1, BASE_URL, body['BusinessTag'], (str(body['WorkflowID']) + "wfes"))

    ## ########## turning off for speed debug

    threadID = 0

    try:
        for flow in lisval['subflows']:
            threadID = threadID + 1
            threadname = "thread" + flow
            threadname = grpThread(threadID, body, flow, BASE_URL, headers1, parentID)
            threadname.start()
            threads.append(threadname)
    except:
        logging.warning("No subflow was defined")


    for wfe in lisval['wfes']:
        next_stage = ""
        threadID = threadID + 10000

        logging.warning(wfe)
        # logging.warning(str(body))
        # logging.warning(wfesparentID)
        # logging.warning(filepath)
        # logging.warning(filepath_server)
        logging.warning("------------------------")


        wfectr = {}
        try:
            wfectr = elctrall[wfe]
        except:
            wfectr = {"c" : "", "t" : "", "r" : ""}



        threads = create_worflow_elements(wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1, threadID, threads, wfectr, cardList,next_stage)

        # threadname = "thread" + wfe
        # threadname = wfeThread(threadID, wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1)
        # threadname.start()
        # threads.append(threadname)
    #
    # for t in threads:
    #     t.join()
    #

    logging.warning(str(lisval))
    threads1 = []

    for wfe in lisval['deptwfes']:
        # threadID = 15000
        # threadname = "thread" + wfe
        # logging.warning(" firing off the thread " +  wfe)
        # threadname = configThread(threadID, wfe, lisval, wfesparentID, parentID, filepath, filepath_server, body, BASE_URL, headers1)
        create_config_cards(wfe, lisval, wfesparentID, parentID, filepath, filepath_server, body, BASE_URL, headers1)
        #
    #     threadname.start()
    #     logging.warning(" starting off the thread " +  wfe)
    #
    #     threads1.append(threadname)
    #
    #     # create_config_cards(wfe, lisval, wfesparentID, filepath, filepath_server, body, BASE_URL, headers1)
    #
    # logging.warning(threads1)
    # for t in threads1:
    #     t.join()


def create_config_cards(wfe, lisval, wfesparentID, parentID, filepath, filepath_server, body, BASE_URL, headers1):

    topname = wfe + "_CONFIG"
    logging.warning(str(topname))
    result = CM.create_txt_card(topname, "Configure the workflow here", body['BusinessTag'], headers1,wfesparentID,BASE_URL, "false", "true")

    CardIds = str(result)
    logging.warning(CardIds)
    tagName = body['WorkflowID']
    tagNameTop = wfe + ":WFID_" + str(tagName)
    # tagNameTop = wfe + ":WFID:" + str(tagName)

    # allowedusers = wfe + "mgr"

    CM.set_card_permissions(BASE_URL, "All Org Users", CardIds, body['BusinessTag'], "VIEW", headers1)

    tagnames = tagNameTop + "," + "wfe:" + topname
    result = CM.add_tags_future(CardIds, tagnames, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
    CM.create_txt_card("dummy", "dummy", body['BusinessTag'], headers1, CardIds, BASE_URL, "true", "false")

    # tagT = ""
    # for ele in lisval['wfes']:
    #     if wfe in ele:
    #
    #         # newtag = "task:" + ele + ":WFID:" + str(body['WorkflowID'])
    #         newtag = "task:" + ele + ":" + wfe + ":WFID_" + str(body['WorkflowID'])
    #         if tagT == "":
    #             tagT = newtag
    #         else:
    #             tagT = tagT + "," + newtag
    #
    # result = json.loads(CM.get_all_tagIds(tagT, BASE_URL, body['BusinessTag'], headers1))
    #
    # form_element = []
    # grp_name = wfe + "p_" + str(body['WorkflowID'])
    # grp_ID = CM.find_out_grp_ID(grp_name, headers1, body['BusinessTag'], BASE_URL)
    #
    # alltasks = []
    # alltasks = CM.unpaginate(result['data']['elements'], alltasks, headers1)
    #
    # for deptTasks in alltasks:
    #     elem = {}
    #     subid = ""
    #     wfename = ""
    #     for tag in deptTasks['tags']:
    #         subid = str(tag['CardID'])
    #         if (re.search(r'task:(.*):\w+:', tag['TagName'])):
    #             sstring = re.search(r'task:(.*):\w+:', tag['TagName'])
    #             wfename = sstring.group(1)
    #
    #     filename = filepath + wfename + ".csv"
    #     filename_server = filepath_server + wfename + ".csv"
    #     ###### one wfe only below :::
    #     val1 = {}
    #     # try:
    #     #     # val1 = WP.parse_wfe(filename)
    #     #     data = pd.read_csv(filename, names=[0, 1, 2])
    #     #     desc = data[1][2]
    #     # except:
    #     #     # val1 = WP.parse_wfe(filename_server)
    #     #     data = pd.read_csv(filename_server, names=[0, 1, 2])
    #     #     desc = data[1][2]
    #
    #     try:
    #         val1 = WP.parse_wfe(filename)
    #         desc = val1['desc']
    #     except:
    #         val1 = WP.parse_wfe(filename_server)
    #         desc = val1['desc']
    #
    #     # elem['label'] = val1['desc'] + " : " + deptTasks['title']
    #     elem['label'] = desc + " : " + deptTasks['title']
    #     elem['type'] = "AUTO_COMPLETE"
    #     elem['required'] = 0
    #     elem['placeholder'] = ""
    #     elem['editable'] = "true"
    #     elem['values'] = grp_ID
    #     elem['python'] = subid
    #     elem['tagsUsed'] = tagT
    #     form_element.append(elem)
    #
    # logging.error("Got her fine for task creation form " + grp_ID)
    #
    # form = "Task Assignment Form"
    # cardID = CM.form_card(BASE_URL, headers1, form, body['BusinessTag'], parentID)
    # # logging.error("Got her fine for task creation form " + str(cardID))
    #
    # CM.set_card_permissions(BASE_URL, "All Org Users", str(cardID), body['BusinessTag'], "ALLLOWED_USERS",
    #                         headers1)
    # # form = "Web Tasks"
    # result = CM.create_form_elements(BASE_URL, headers1, body['BusinessTag'], cardID, form, form_element)
    # fields = {}
    # logging.error("Got her fine for form elements creation " + result)
    #
    # result1 = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, str(cardID), fields)
    # newtag = topname + ":WFID_" + str(tagName) + "," + form
    # resp = CM.add_tags_future(str(result1), newtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

    #####
    try:
        s_arr = []
        # lisval.reverse()
        for wfe in lisval:
            elem_1 = {}
            if wfe == "END":
                logging.warning("ignore")
            else:
                next_stage = wfe
                filename = filepath + next_stage + ".csv"
                filename_server = filepath_server + next_stage + ".csv"
                tag = next_stage + ":WFID_" + str(body['WorkflowID'])
                result = json.loads(CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'], headers1))
                val1 = {}
                try:
                    val1 = WP.parse_wfe(filename)
                    desc = val1['desc']
                except:
                    val1 = WP.parse_wfe(filename_server)
                    desc = val1['desc']

                    for alltag in result['data']['elements']:
                        logging.warning(alltag)
                        if "Skip" in alltag['allTags']:
                            sid = str(alltag['cardID'])
                            elem_1['label'] = desc
                            elem_1['type'] = "CHECK_BOX"
                            elem_1['required'] = 0
                            elem_1['placeholder'] = ""
                            elem_1['editable'] = "true"
                            elem_1['python'] = sid
                            s_arr.append(elem_1)
        # print s_arr
        form = "Skip workflow stages form"
        cardID = CM.form_card(BASE_URL, headers1, form, body['BusinessTag'], parentID)
        logging.warning(cardID)
        logging.warning("Form card created successfully")
        CM.set_card_permissions(BASE_URL, "All Org Users", str(cardID), body['BusinessTag'], "ALLLOWED_USERS",headers1)

        s_arr_reversed_list = list(reversed(s_arr))
        result = CM.create_form_elements(BASE_URL, headers1, body['BusinessTag'], cardID, form, s_arr_reversed_list)
        logging.warning(result)
        logging.warning("elemets are created")
        fields = {}
        result1 = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, str(cardID), fields)
        logging.warning(result1)
        logging.warning("submission was succesfull")
        newtag = topname + ":WFID_" + str(tagName) + "," + form
        resp = CM.add_tags_future(str(result1), newtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
        logging.warning(resp)
        logging.warning("tag added successfully")


    except:logging.warning("---")

    # e_arr = []
    # for ele in lisval['wfes']:
    #     elem = {}
    #     tag = ele + ":WFID_" + str(body['WorkflowID'])
    #     if wfe in ele:
    #         filename = filepath + ele + ".csv"
    #         filename_server = filepath_server + ele + ".csv"
    #         ###### one wfe only below :::
    #         val1 = {}
    #         # try:
    #         #     # val1 = WP.parse_wfe(filename)
    #         #     data = pd.read_csv(filename, names=[0, 1, 2])
    #         #     desc = data[1][2]
    #         # except:
    #         #     # val1 = WP.parse_wfe(filename_server)
    #         #     data = pd.read_csv(filename_server, names=[0, 1, 2])
    #         #     desc = data[1][2]
    #
    #         try:
    #             val1 = WP.parse_wfe(filename)
    #             desc = val1['desc']
    #         except:
    #             val1 = WP.parse_wfe(filename_server)
    #             desc = val1['desc']
    #
    #         result = json.loads(CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'], headers1))
    #         for alltag in result['data']['elements']:
    #             if "Estimate" in alltag['allTags']:
    #                 sid = str(alltag['cardID'])
    #                 elem['label'] = desc + " : Estimated Time"
    #                 elem['type'] = "EDIT_TEXT"
    #                 elem['required'] = 0
    #                 elem['placeholder'] = ""
    #                 elem['editable'] = "true"
    #                 elem['python'] = sid
    #                 e_arr.append(elem)
    # # print e_arr
    # form = "Update estimated Time Form"
    # cardID = CM.form_card(BASE_URL, headers1, form, body['BusinessTag'], parentID)
    # CM.set_card_permissions(BASE_URL, "All Org Users", str(cardID), body['BusinessTag'], "ALLLOWED_USERS",
    #                         headers1)
    # # CM.set_card_permissions(BASE_URL, allowedusers, str(cardID), body['BusinessTag'], "OPERATOR", headers1)
    # result = CM.create_form_elements(BASE_URL, headers1, body['BusinessTag'], cardID, form, e_arr)
    # fields = {}
    # result1 = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, str(cardID), fields)
    # newtag = topname + ":WFID_" + str(tagName) + "," + form
    # resp = CM.add_tags_future(str(result1), newtag, BASE_URL, body['BusinessTag'], headers1,
    #                           body['BusinessTag'])


def packagingSubmit(body, BASE_URL, headers1, packagingform):
    if len(body['tags']) > 0:

        logging.warning("@@@@@@@@@@@@@@@@@@@@@@@@@")
        logging.warning(datetime.datetime.now())
        logging.warning("@@@@@@@@@@@@@@@@@@@@@@@@@")


        input_data = body['FormData']['Packaging Type?']
        formtags = CM.get_tags_by_cardID(body['FormSubmissionID'],BASE_URL,body['BusinessTag'],headers1)
        formtags = json.loads(formtags)
        formtags = formtags['data']['elements'][0]['allTags']
        for tag in formtags:
            if(re.search(r"WFID_(\d+)", tag)):
                ids = re.search(r"WFID_(\d+)", tag)
                wfid = ids.group(1)

        formkey = "created_packaging" + wfid
        body['FormData']['wid'] = wfid
        try:
            createdvalue = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], formkey)
            createdvalue = json.loads(createdvalue)
            createdvalue = createdvalue['data']['value']['_value']
            if createdvalue == "112":
                logging.warning("packaging form is resubmitted")
            else:
                logging.error("something is wrong in the packaging form submission")

        except:
            CM.add_val_in_table(BASE_URL, headers1, formkey, 112, body['BusinessTag'],int(wfid))
            if "Carton" in body['FormData']['Packaging Type?']:
                masterFileName = "WFE_subflow_PKG1.csv"
                create_wfes(body, masterFileName, headers1, BASE_URL)
            elif "Flexible" in body['FormData']['Packaging Type?']:
                masterFileName = "WFE_subflow_PKG2.csv"
                create_wfes(body, masterFileName, headers1, BASE_URL)
            elif "Rigid" in body['FormData']['Packaging Type?']:
                masterFileName = "WFE_subflow_PKG2.csv"
                create_wfes(body, masterFileName, headers1, BASE_URL)
            else:
                logging.warning("packaging form is blank")

        else:
            try:
                createdvalue = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], formkey)
                createdvalue = json.loads(createdvalue)
                createdvalue = createdvalue['data']['value']['_value']
                if createdvalue == "112":
                    logging.warning("resubmit")
                else:
                    CM.add_val_in_table(BASE_URL, headers1, formkey, 112, body['BusinessTag'],int(wfid))
                    result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1,
                                                              packagingform, input_data)
            except:
                CM.add_val_in_table(BASE_URL, headers1, formkey, 112, body['BusinessTag'],int(wfid))
                result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, packagingform,
                                                          input_data)


def topformSubmit(body, workflowTopFormID, headers1, BASE_URL):


    logging.warning("@@@@@@@@@@@@@@@@@@@@@@@@@")
    logging.warning(datetime.datetime.now())
    logging.warning("@@@@@@@@@@@@@@@@@@@@@@@@@")


    input_data = body['FormData']
    formkey =  body['BusinessTag'] + body['FormData']['wid']
    tagNamesub = "WFID_" + body['FormData']['wid']
    wid = body['FormData']['wid']

    # if body['FormData']['Patient Name (If Existing Patient)'] or body['FormData']['Patient Name (If New Patient)'] is None:
    if body['FormData']['Date of Birth'] is None:
        logging.warning("Blank form submission")
    else:

        try:
            createdvalue = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], formkey)
            logging.warning("***********************************")
            logging.warning(createdvalue)
            logging.warning("--------------------------------------")
            createdvalue = json.loads(createdvalue)
            createdvalue = createdvalue['data']['value']['_value']
            logging.warning("*********************-----------")
            logging.warning(createdvalue)
            if createdvalue == "113":
                logging.warning("resubmit")
                try:
                    if body['FormData']['Staff Only: Create new patient entry'] == "true":
                        pname = body['FormData']['Patient Name (If New Patient)']

                        email_ID = ""
                        result = CM.add_user_InBusiness(body['BusinessTag'], pname, email_ID, headers1, BASE_URL)
                        jsonreply = json.loads(result)
                        user_id = jsonreply['data']['usertagid']
                        logging.warning("addition is done " + str(user_id))

                        body["Contact"] = body['FormData']['Patient Phone No']
                        body["EmailID"] = body['FormData']['Patient Email']
                        method = "POST"
                        url = BASE_URL + 'zvice/interaction/' + user_id
                        body["interactionID"] = "CommonInteraction_INTERACTION_TYPE_MODIFY_CONTACT_INFO"
                        jsonreply = CM.hit_url_method(body, headers1, method, url)
                        logging.warning(jsonreply)
                        decurl = BASE_URL + "push/dectest/" + user_id
                        response = urllib2.urlopen(decurl)
                        html = response.read()
                        decTag = json.loads(html)['decTagID']
                        user_id_1 = decTag % 1000000

                        tagName = "IDAdmin:GenePath"
                        result = CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1)
                        for f_name in json.loads(result)['data']['elements']:
                            if "ID Admin" in f_name['title']:
                                data = json.loads(f_name['content'])
                                for e1 in data['Elements'][0]['Elements']:
                                    if "Patient ID Prefix" in e1['FieldLabel']:
                                        patient_prefix = e1['Value']


                        tagName = "TOP:WFID_" + str(body['FormData']['wid'])
                        result = CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1)
                        for f_name in json.loads(result)['data']['elements']:
                            if "ID Tracking" in f_name['title']:
                                val = ('{:06}'.format(user_id_1))
                                patient_ID = patient_prefix + str(val)
                                sub_id = f_name['cardID']
                                # form_ID = 6606
                                form_ID = id_tracking
                                input_data = {"Patient ID": patient_ID}
                                result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID,input_data,sub_id)
                                logging.warning(result)
                        form_ID = patient_form
                        p_number = body['FormData']['Patient Phone No']
                        p_email = body['FormData']['Patient Email']
                        p_dob = body['FormData']['Date of Birth']
                        p_age = body['FormData']['Age']
                        p_sex = body['FormData']['Sex']
                        input_data = {"Patient Name":pname,"Patient Phone No":str(p_number),"Patient Email":p_email,"User ID":str(user_id),"Date of Birth":p_dob,
                                      "Age":p_age,"Sex":p_sex}
                        result = CM.form_submission_using_NEW_API_genepath(BASE_URL, body['BusinessTag'], headers1, form_ID, input_data)
                        logging.warning(result)

                        input_data = {"Patient Name (If Existing Patient)": user_id}
                        result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1,body['FormData']['FormID'], input_data,body['FormData']['FormSubmissionID'])
                        logging.warning(result)



                except:logging.warning("Missing field")


                ### debug only
                # masterFileName = "WFE_subflow_TOP.csv"
                # create_wfes(body, masterFileName, headers1, BASE_URL)
                ## end debug


            else:
                CM.add_val_in_table(BASE_URL, headers1, formkey, 113, body['BusinessTag'],int(wid))
                masterFileName = "WFE_subflow_TOP.csv"
                create_wfes(body, masterFileName, headers1, BASE_URL)


        except:
            result = CM.add_val_in_table(BASE_URL, headers1, formkey, 113, body['BusinessTag'],int(wid))
            logging.warning(result)
            masterFileName = "WFE_subflow_TOP.csv"
            logging.warning("**********  creating starts*******************")
            create_wfes(body, masterFileName, headers1, BASE_URL)
            logging.warning("****************** creation ends******************")
            # if body['FormData']['Project Type?'] == "New Brand/Product" or body['FormData'][
            #     'Project Type?'] == "Product Variant":
            #     masterFileName = "WFE_subflow_NPD1.csv"
            #     # masterFileName = "WFE_subflow_try.csv"
            #     create_wfes(body, masterFileName, headers1, BASE_URL)
            # elif body['FormData']['Project Type?'] == "New SKU/Pack":
            #     masterFileName = "WFE_subflow_NPD2.csv"
            #     create_wfes(body, masterFileName, headers1, BASE_URL)
            # else:
            #     logging.error("Project type not specified. Doing Nothing")


    logging.warning("@@@@@@@@@@@@@@@@@@@@@@@@@")
    logging.warning(datetime.datetime.now())
    logging.warning("@@@@@@@@@@@@@@@@@@@@@@@@@")


def mainworkflow(body, h1, B_URL):


    global filepath
    global filepath_server

    global BASE_URL
    global headers1

    global test_master_metadata
    global additional_test_info
    global billing_form_id
    global sample_reception_form
    global id_tracking
    global patient_initiation_form
    global id_admin
    global test_status_form
    global patient_form

    BASE_URL = B_URL
    headers1 = h1

    test_master_metadata = "6607"
    additional_test_info = "5312"
    billing_form_id = "5323"
    sample_reception_form = "5319"
    id_tracking = "6606"
    patient_initiation_form = "5322"
    id_admin = "6605"
    test_status_form = "5315"
    patient_form = "13577"


    # filepath = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/wfes_GenePath/"
    # filepath = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/wfes_GenePath_DEV_nov28/"
    filepath = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/GenePath/wfes_GenePath/"
    filepath_server = "/var/www/cgi-bin/workflow/wfes_GenePath/"
    # filepath_server = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/GenePath/wfes_GenePath/"


    # workflowTopFormID = "92"    ### patient intimation form previous
    workflowTopFormID = "5322"  ### patient intimation form
    create_user_formID_DOCTOR = "13340"    # add user doctor
    create_user_formID_EMP = "11010"    # add user employee
    packagingform = "15150"
    create_user_formID_PATIENT = "13577"    #add user patient

    usuallistFile = filepath + str(body['BusinessTag']) + "_usualform_tables.csv"
    usuallistFile_server = filepath_server + str(body['BusinessTag']) + "_usualform_tables.csv"
    ###### one wfe only below :::

    hasHeader = "Y"

    global cardList
    cardList = {}

    try:

        with open(usuallistFile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            for row in data:
                cardList[row[0]] = row[1]

    except:
        with open(usuallistFile_server, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            if hasHeader == "Y":
                row1 = data.next()
            for row in data:
                cardList[row[0]] = row[1]

    # try:
    #     w_ID = body['FormData']['WorkflowID']
    #     w_ID = str(w_ID)
    # except:
    #     w_ID = 0

    if body['Cmd'] == "workflow-create":
        outdict = {}
        input_data = {"wid" : str(body['WorkflowID'])}
        result = CM.form_submission_using_NEW_API(BASE_URL,body['BusinessTag'],headers1,workflowTopFormID,input_data)   #form submission
        CardIds = str(result)
        tagName = "TOP:WFID_" + str(body['WorkflowID'])
        CM.add_tags_future(CardIds, tagName, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
        #submit a project config form with the correct workflowID
        tagArray = [tagName]
        outdict['tags'] = tagArray
        # logging.warning(outdict)
        print json.dumps(outdict)
        ## open up the workflowTopFormID for submission


    if body['Cmd'] == "form-submit":

        # if body['FormID'] == packagingform:
        #     packagingSubmit(body, BASE_URL, headers1, packagingform)

        if body['FormID'] == workflowTopFormID:
            topformSubmit(body, workflowTopFormID, headers1, BASE_URL)

        elif body['FormID'] == create_user_formID_DOCTOR:
            user_addition_using_Form(body, BASE_URL, headers1)

        elif body['FormID'] == create_user_formID_EMP:
            user_addition_using_Form(body, BASE_URL, headers1)

        elif body['FormID'] == create_user_formID_PATIENT:
            user_addition_using_Form(body, BASE_URL, headers1)



        elif len(body['tags']) > 0:

            try:
                tagsoncard = body['tags']
            except:
                try:
                    tags = CM.get_tags_by_cardID(body['FormSubmissionID'], BASE_URL, body['BusinessTag'], headers1 )
                    tagsoncard = json.loads(tags)['data']['elements'][0]['allTags']
                except:
                    logging.warning("Nothing to do here")

            # logging.warning(tagsoncard)

            try:
                if len(tagsoncard) < 1:
                    logging.warning("not a tagged card")
                for tag in tagsoncard:
                    tags = tag.split(":")
                    if len(tags) == 2:
                        tagName = tag
                        decisionname = tags[0]
                        wfidtag = tags[1]
                        wfid = re.search("WFID_(\d+)", tags[1])
                        wfid = wfid.group(1)
                    if len(tags) == 1:
                        formname = tag
                    st = decisionname.split("_")
                    st = st[0]
                    st = "LAB"
                    st_task = "LAB"

                logging.warning(formname  +  "$$$$$$$$$")
                logging.warning(decisionname + "$$$$$$$$$^^^^")


                if "_CONFIG" in decisionname:
                    # logging.warning(decisionname)
                    result = json.loads(CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1))
                    for alltag in result['data']['elements']:
                        if "Task Assignment Form" in alltag['allTags'] and "Task Assignment Form" in formname:
                            data = json.loads(alltag['content'])
                            elem = {}
                            statusd = {}
                            for subelm in data['Elements'][0]['Elements']:
                                try:
                                    g_ID = subelm['Value']
                                    g_ID = json.loads(g_ID)
                                    g_ID = g_ID['GroupIDs']
                                    c_id = subelm['MetaData']['PYTHON']
                                    elem[c_id] = g_ID
                                    # tagT = subelm['MetaData']['tagsUsed']
                                    # statusd[c_id] = subelm['status']
                                except:
                                    logging.warning("no user grp assigned")


                            grp_name = st + "p_" + wfid

                            parentID = CM.find_out_grp_ID(grp_name, headers1, body['BusinessTag'], BASE_URL)

                            uniqgrps = []
                            for k,v in elem.items():
                                for gr in v:
                                    if gr in uniqgrps:
                                        continue
                                    else:
                                        uniqgrps.append(gr)

                            for group in uniqgrps:
                                try:
                                    by = {'grpUserGroupID': group}
                                    CM.add_usergrps_grps(BASE_URL, json.dumps(by), headers1, body['BusinessTag'], parentID)
                                except:
                                    logging.warning("group couldnt be added")


                            statusd = "temp holder"

                            for k, v in elem.items():
                                for gid in v:
                                    task_Id = int(k)
                                    g_Id = gid
                                    method = "GET"
                                    b = {}
                                    url = BASE_URL + "tasks/getsingle/" + body['BusinessTag'] + "/" + str(task_Id)
                                    resp = CM.hit_url_method(b, headers1, method, url)
                                    try:
                                        statusd = json.loads(resp)['data']['elements'][0]['status']
                                    except:
                                        statusd = "Assigned"
                                    if "Assigned" not in statusd:
                                        result = CM.edit_task_for_workflow_stat(BASE_URL, body['BusinessTag'], headers1, task_Id, g_Id, "")
                                    else:
                                        result = CM.edit_task_for_workflow_stat(BASE_URL, body['BusinessTag'], headers1, task_Id, g_Id, "Assigned")

                        if "Update estimated Time Form" in alltag['allTags'] and "Update estimated Time Form" in formname:
                            data = json.loads(alltag['content'])
                            for subelm in data['Elements'][0]['Elements']:
                                s_id = subelm['MetaData']['PYTHON']
                                estimate_value = subelm['Value']
                                form_ID = 10
                                input_data = {"Estimated Time": estimate_value}
                                result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID,
                                                                          input_data, s_id)

                        if "Skip workflow stages form" in alltag['allTags'] and "Skip workflow stages form" in formname:
                            data = json.loads(alltag['content'])
                            for subelm in data['Elements'][0]['Elements']:
                                s_id = subelm['MetaData']['PYTHON']
                                skip_flag = subelm['Value']
                                form_ID = 82
                                input_data = {"SKIP": skip_flag}
                                result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1,form_ID, input_data, s_id)

                elif "Test Selection Form" in formname:

                    body['WorkflowID'] = wfid
                    logging.warning(str(body)  +  "###")

                    startTestFlow(body)


                elif "Status" in formname:

                    status = body['FormData']['Status']
                    estimateTag = "estimate::" + tagName
                    tasktag = "task:" + decisionname + ":" + st + ":" + wfidtag
                    estimateTag = "estimate::" + tagName

                    result = CM.get_all_tagIds(estimateTag, BASE_URL, body['BusinessTag'], headers1)
                    show = json.loads(result)
                    # value = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], "Estimate")
                    # value = json.loads(value)
                    # form_ID = value['data']['value']['_value']

                    try:
                        # result = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'],
                        #                                            form_key)  # gettings key value pair

                        ### change this to read from the xls.

                        # result = json.loads(result)
                        form_ID = cardList["Estimate"]
                    except:
                        logging.error("such a form does not exist")
                        form_ID = ""


                    startdate = datetime.datetime.utcnow()
                    sd = startdate.strftime('%Y-%m-%d %H:%M:%S')
                    startExists = False
                    for sub_mission in json.loads(result)['data']['elements']:
                        if "Estimate" in sub_mission['allTags']:
                            s_id = sub_mission['cardID']
                            try:
                                for el in json.loads(sub_mission['content'])['Elements'][0]['Elements']:
                                    if "Start Date" in el['FieldLabel']:
                                        if el['Value'] == None:
                                            continue
                                        else:
                                            startExists = True
                            except:
                                continue
                            input_data = {}
                            if status == "Completed":
                                input_data['End Date'] = sd

                            input_data["Status"]  = status
                            result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID,
                                                                  input_data, s_id)


                    ## deal with the tasks in the said wfe ----------------------

                    if "Completed" in status:
                        complete_wfe(tagName, wfid, BASE_URL, body, headers1)
                        ###complete all tasks in that workflow
                    elif status == "Active":
                        # tasktag = 'task:WFE1_1:LAB:WFID_18'
                        value = CM.get_all_tagIds(tasktag, BASE_URL, body['BusinessTag'], headers1)
                        v = json.loads(value)
                        taskID_array = []
                        for t_val in json.loads(value)['data']['elements']:
                            if "Assigned" in t_val['status']:
                                t_id = t_val['taskID']
                                taskID_array.append(t_id)
                            else:
                                continue
                        url = BASE_URL + "tasks/edit/" + body['BusinessTag']
                        method = "POST"
                        rb = {}
                        rb['Status'] = "Active"
                        startdate = datetime.datetime.utcnow()
                        sd = startdate.strftime('%Y-%m-%d %H:%M:%S')
                        rb['StartDate'] = sd
                        for taskno in taskID_array:
                            rb['TaskID'] = taskno
                            response = json.loads(CM.hit_url_method(rb, headers1, method, url))

                        if startExists == False:
                            input_data = {"Start Date": sd}
                            result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID, input_data, s_id)
                        else:
                            logging.warning("Start already exists")

                else:
                    try:
                    #************************************  We are not putting thiscode on prod. so we are commenting this code  ***********************
                        flag = "s"
                        if "donotcall" in body['url_params']:
                            logging.warning("we are inside DONOTCALL")
                            check_flag = body['url_params']['donotcall']
                            flag = check_flag

                        if flag == "t":
                            logging.warning("do not proceed for Linked submission")

                        else:
                            logging.warning("WE are going inside METADATA")
                            result = CM.get_form_submission(body['FormSubmissionID'], body['BusinessTag'], BASE_URL,headers1)
                            for elm in json.loads(result)['data']['ondemand_action']:
                                if elm['MetaData'] != None:
                                    logging.warning("metadata is not NONE")
                                    link_proj = json.loads(elm['MetaData'])
                                    for sub_link_proj in link_proj:
                                        if "LinkedProjects" in sub_link_proj:
                                            logging.warning("we are inside LINKED PROJECTS")
                                            wf_array = link_proj['LinkedProjects']

                                            if len(wf_array) != 0:
                                                logging.warning("array is not empty")
                                                for work_id in wf_array:
                                                    form = formname
                                                    tag = decisionname + ":WFID_" + str(work_id)
                                                    combine_tag = form + "," + tag
                                                    form_ID = body['FormID']
                                                    input_data = body['FormData']
                                                    result = CM.combine_tag_gives_cardID(BASE_URL, body['BusinessTag'],headers1, combine_tag)
                                                    for sub_cardID in json.loads(result)['data']['elements']:
                                                        if form in sub_cardID['Tags']:
                                                            submission_cardID = sub_cardID['CardID']
                                                            result = CM.EDIT_submission_using_NEW_API_using_ChangeIn_URL(BASE_URL, body['BusinessTag'],
                                                                headers1, form_ID, input_data, submission_cardID)
                                                        else:
                                                            logging.warning("Form name is not found")
                                            else:
                                                logging.warning("Multiselect workflow array is empty")
                                        else:
                                            logging.warning("not able to find Linked Project")
                                else:
                                    logging.warning("Meta data is NULL dont do anything")
                        #*****************************************************************************************************************

                        hasHeader = "Y"
                        # mapping_TOP = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/Mapping_GENEpath.csv"
                        mapping_TOP = "/var/www/cgi-bin/workflow/Mapping_GENEpath.csv"
                        # Test_status_formID = 5315   #we are changing value only in one form. thats  why we hard coded this form id.
                        form_ID = test_status_form
                        # Filter_formID = 5320
                        c_tag = tagName
                        result = json.loads(CM.get_all_tagIds(c_tag, BASE_URL, body['BusinessTag'], headers1))
                        for alltag in result['data']['elements']:

                            with open(mapping_TOP, 'r') as rf:
                                data = csv.reader(rf, delimiter=',')
                                if hasHeader == "Y":
                                    row1 = data.next()
                                for row in data:
                                    if formname in alltag['allTags']:
                                        data = json.loads(alltag['content'])
                                        for subelm in data['Elements'][0]['Elements']:
                                            if row[2].strip() == subelm['ElementID'].strip():
                                                if subelm['Value'].strip() == row[4].strip():
                                                    tag = "TOP:WFID_" + str(wfid)
                                                    result = CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'],headers1)
                                                    for f_name in json.loads(result)['data']['elements']:
                                                        if row[5] in f_name['title']:
                                                            sub_ID = f_name['cardID']
                                                            input_data = {row[6]:row[8]}
                                                            result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'],headers1,form_ID, input_data,sub_ID)
                                                        else:logging.warning("Title not found")
                                                else:logging.warning("Value not matching")
                                    else:logging.warning("Form not found")


                        result = CM.get_form_submission(body['FormSubmissionID'], body['BusinessTag'], BASE_URL, headers1)
                        result = json.loads(result)['data']['ondemand_action'][0]['inputs']
                        checkboxes = {}
                        for ele in result:
                            if "CheckBox" in ele['widget']:
                                for prop in ele['properties']:
                                    if prop['name'] == "text":
                                        key = prop['value']
                                    elif prop['name'] == "default":
                                        value = prop['value']
                                checkboxes[key] = value
                    except:
                        logging.warning("No checkboxes found")
                    flag = False
                    try:
                        for k,v in checkboxes.items():
                            if v == "false":
                                flag = True
                        if flag == False:
                            st = decisionname.split('_')
                            st = st[0]
                            # tag = "task:" + decisionname + ":" + st + ":WFID_" + wfid  #### this is wrong
                            key = "tasksOf" + body['FormSubmissionID']
                            writeVal = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], key)
                            taskID_1_array = []
                            try:
                                result = json.loads(writeVal)
                                taskid = result['data']['value']['_value']
                                taskid = taskid.split(',')
                                for t_val in taskid:
                                    t_id = t_val
                                    taskID_1_array.append(t_id)
                            except:
                                logging.warning("no tasks found")

                            url = BASE_URL + "tasks/edit/" + body['BusinessTag']
                            method = "POST"
                            rb = {}
                            rb['Status'] = "Completed"
                            for taskno in taskID_1_array:
                                rb['TaskID'] = int(taskno)
                                response = json.loads(CM.hit_url_method(rb, headers1, method, url))

                            exitchecklistFlag = check_for_exit_checklist_in_stage((decisionname + ":" + wfidtag), body, BASE_URL, headers1)
                            if exitchecklistFlag:
                                logging.warning("stage has exitchecklist")
                            else:
                                tasktag = "task:" + decisionname + ":" + st_task + ":" + wfidtag
                                completeFlag = check_alltasks_complete(tasktag, body, BASE_URL, headers1)
                                if completeFlag:
                                    set_wfe_status(decisionname + ":" + wfidtag, "Completed", body, BASE_URL, headers1)
                                    # complete_wfe((decisionname + ":" + wfidtag), wfid, BASE_URL, body, headers1)

                            if "Exit Checklist" in formname:
                                tagName1 = decisionname + ":WFID_" + wfid
                                set_wfe_status(tagName1, "Completed", body, BASE_URL, headers1)
                                # complete_wfe(tagName1, wfid, BASE_URL, body, headers1)

                            elif "Entry Checklist" in formname:
                                tagName1 = decisionname + ":WFID_" + wfid
                                set_wfe_status(tagName1, "Active", body, BASE_URL, headers1)


                    except:
                        logging.warning("Nothing to do in this form")
            except:
                logging.warning("Not a tagged form")


    if body['Cmd'] == "workflow-click":
        tagName = "WFID_" + str(body['WorkflowID'])
        outdict = {}
        tagArray = [tagName]
        outdict['tags'] = tagArray
        logging.warning(outdict)
        print json.dumps(outdict)
    if body['Cmd'] == "textcard-click":
        for tag in  body['Tags']:
            if "wfe:" in tag:
                wfe = re.match(r"wfe:(.*)", tag)
                cardname = wfe.group(1)
            elif "WFID_" not in tag:
                cardname = tag
        for tag in body['Tags']:
            if cardname in tag:
                if (re.match(r"subflow:(\w+)", tag)):
                    tagNamem = re.match(r"subflow:(\w+)", tag)
                    tagName = tagNamem.group(1)
                else:
                    tagName = cardname
            if "WFID_" in tag:
                wfidm = re.search(r"(WFID_\d+)",tag)
                wfid = wfidm.group(1)
        outdict = {}
        tagArray = [tagName + ":" + wfid]
        outdict['tags'] = tagArray
        logging.warning(outdict)
        print json.dumps(outdict)