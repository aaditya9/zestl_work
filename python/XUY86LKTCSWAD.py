
import common as CM
import wfe_parser as WP
# import pandas as pd
# import logon as LL
import json
import sys
import logging
import re
import csv
import datetime
# from datetime import timedelta
import threading


threadLock = threading.Lock()
threads = []




def setup_logger(logger_name, log_file, level=logging.WARN):

    log_setup = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    log_setup.setLevel(level)
    log_setup.addHandler(fileHandler)
    log_setup.addHandler(streamHandler)




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

#***********************   Creating new function here (Created by MINAL) ***********************

def find_skip_in_nextFlow(depTagname, BASE_URL, zviceID, headers1, skipTag,wfid, nxtstages):
    # next_stage_array = []
    cards = CM.get_all_tagIds(depTagname, BASE_URL, zviceID, headers1)
    try:
        cards = json.loads(cards)
        contents = cards['data']['elements'][0]['content']
        contents = json.loads(contents)
        for a in contents['Elements'][0]['Elements']:
            if "Next stage" in a['ElementID']:
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

#***************************************************************************

def complete_wfe(tagName1, wfid, BASE_URL, body, headers1):
    # filepath = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/wfes/"
    # filepath_server = "/var/www/cgi-bin/workflow/wfes/wfes_GenePath/"

    depTagname = "backend::" + tagName1
    skipTag = "skip::" + tagName1

    tags = tagName1.split(":")
    subname = tags[0]
    text_name = subname.split("_")
    t_name = text_name[0]
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

#******************************  Minal code ***********************
    #
    nextstages = []
    nextstages = find_skip_in_nextFlow(depTagname, BASE_URL, body['BusinessTag'], headers1,skipTag,wfid, nextstages)
    # print result
    ### use tagname1 wfdename:wfid_xx to get the wfe contents from wfe_parser. send messages to the comm pref and use other values correctly.
    #### where to get the project name from? top form?
    # cards = CM.get_all_tagIds(depTagname, BASE_URL, body['BusinessTag'], headers1)
    #
    #
    # try:
    #     cards = json.loads(cards)
    #     contents = cards['data']['elements'][0]['content']
    #     contents = json.loads(contents)
    #     for a in contents['Elements'][0]['Elements']:
    #         if "Next stage" in a['ElementID']:
#             nextstage = a['Value']
#     nextstages = result.split(";")
    try:
        for stage in nextstages:
            logging.warning("we are inside COMPLETE_WFES function")
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
                            result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'],headers1, form_ID, input_data,s_id)

    except:
        logging.warning("no contents found")

    try:
        commgroups = val1['Comm'].split(";")
        commgrps_corrected = []

        # tag = "TOP:WFID_" + str(body['WorkflowID'])
        tag = "TOP:WFID_" + str(wfid)
        result = json.loads(CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'], headers1))
        for f_name in result['data']['elements']:
            if "Application" in f_name['title']:
                data = json.loads(f_name['content'])
                for e1 in data['Elements'][0]['Elements']:
                    if "Applicant Name" in e1['FieldLabel']:
                        workFlow_Name = e1['Value']

        t_tag = t_name + ":WFID_" + str(wfid)
        sub_tag = "wfe:" + subname
        combine_tag = t_tag + "," + sub_tag
        result = CM.combine_tag_gives_cardID(BASE_URL,body['BusinessTag'], headers1,combine_tag)
        for sub_cardID in json.loads(result)['data']['elements']:
            if sub_tag in sub_cardID['Tags']:
                t_cardID = sub_cardID['CardID']

        for grp in commgroups:
            grps = grp.split("_")
            correctName = grps[0] + "_" + wfid
            commgrps_corrected.append(str(correctName))
#**********************  This code is for sending NOTIFICATIONS ************************************

    #************* this code for extra grps for notification************
        manager = val1['subFlow'] + "mgr"
        commgrps_corrected.append(manager)
        proj_team = val1['subFlow'] + "p_" + wfid
        commgrps_corrected.append(str(proj_team))
    #*****************************************************

        b = {}
        b['title'] = workFlow_Name + ": " + val1['desc'] + " completed"
        # b['msg'] = workFlow_Name + ":" + val1['subFlow'] + ":" + "Status for " + val1['desc'] + " changed to completed"
        b['msg'] = workFlow_Name + ":" + val1['subFlow'] + ":" + val1['desc'] + " is now complete"
        # b['msg'] = "workflow step  " + val1['desc'] + " of workflow " + workFlow_Name + "is completed"
        b['commtype'] = ["NOTIFY"]
        b['groupname'] = commgrps_corrected
        b['CardID'] = t_cardID
        method = "POST"
        url = BASE_URL + "usergroups/message/" + body['BusinessTag']
        resp = CM.hit_url_method(b, headers1, method, url)
        logging.warning("Sending notification on Stage completion")
        logging.warning(resp)
#*********************************************************************************
#************    This Code is for sending MAIL  **********************************
        mail = {}
        mail['title'] = workFlow_Name + ": " + val1['desc'] + " completed"
        # mail['title'] = "Workflow step complete"
        mail['msg'] = workFlow_Name + " : " + val1['subFlow'] + " : " + val1['desc'] + " is now complete."
        mail['commtype'] = ["MAIL"]
        mail['groupname'] = commgrps_corrected
        mail['CardID'] = t_cardID
        method = "POST"
        url = BASE_URL + "usergroups/message/" + body['BusinessTag']
        resp = CM.hit_url_method(mail, headers1, method, url)
        logging.warning("Sending MAIL on Stage completion")
        logging.warning(resp)
#****************************************************************************
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
            # s_id = status_card['cardID']
            form_ID = cardList['Status']
            s_id = status_card['cardID']
            input_data = {"Status" : status}
            result = CM.EDIT_submission_using_NEW_API(BASE_URL,body['BusinessTag'],headers1,form_ID,input_data,s_id)


def create_worflow_elements(wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1, threadID, threads, wfectr, cardList, top_status):
    #
    filename = filepath + wfe + ".csv"
    filename_server = filepath_server + wfe + ".csv"


    val1 = {}
    try:
        val1 = WP.parse_wfe_ordered(filename)
    except:
        val1 = WP.parse_wfe_ordered(filename_server)

    result = CM.create_txt_card(val1['desc'], "", body['BusinessTag'], headers1, wfesparentID, BASE_URL, "false",
                                "true")
    CardIds = str(result)
    tagName = body['WorkflowID']
    newtag = val1['subFlow'] + ":WFID_" + str(tagName) + ", wfe:" + val1['name']
    result = CM.add_tags_future(CardIds, newtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
    CM.create_txt_card("dummy", "dummy", body['BusinessTag'], headers1, CardIds, BASE_URL, "true", "false")


    #### speed bedug comment
    threadID = threadID + 1000
    threads = []

    usualForms = ["Estimate", "Skip", "Status", "Dependencies"]

    for ele in usualForms:

        # threadID = threadID + 1
        # threadname = "thread" + ele + val1['name']
        # threadname = usualThread(threadID, val1, ele, body, BASE_URL, headers1, wfectr)

        create_usual_forms(val1, ele, body, BASE_URL, headers1, wfectr)


        # ************** WFE specibody['BusinessTag']fic forms  submission ******#
    mul_forms = list(reversed(val1['forms']))
    for item in mul_forms:
        for k, v in item.items():
            try:
                grp_name = v['AdminsR']
            except:
                grp_name = "N"
            form_key = val1['name'] + ":" + k

            try:
                try:

                    # if top_status in body['FormData']['Status']:

                    if "Active" in top_status :
                        fieldsmeta = json.dumps({"HideEditAction": False})
                    else:
                        fieldsmeta = json.dumps({"HideEditAction": True})
                except:
                    fieldsmeta = json.dumps({"HideEditAction": True})
                result = CM.form_submission_using_NEW_API_meta(BASE_URL, body['BusinessTag'], headers1, cardList[form_key],item[k]['fields'], fieldsmeta)  # submitting form
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

    # for t in threads:
    #     t.join()

    return threads


def create_special_worflow_elements(wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1, threadID, threads, wfectr, cardList, top_status):
    #
    filename = filepath + wfe + ".csv"
    filename_server = filepath_server + wfe + ".csv"


    val1 = {}
    try:
        val1 = WP.parse_wfe_ordered(filename)
    except:
        val1 = WP.parse_wfe_ordered(filename_server)

    # result = CM.create_txt_card(val1['desc'], "", body['BusinessTag'], headers1, wfesparentID, BASE_URL, "false",
    #                             "true")
    # CardIds = str(result)
    tagName = body['WorkflowID']
    newtag = val1['subFlow'] + ":WFID_" + str(tagName) + ", wfe:" + val1['name']

    if wfe == "DOSSIER_WFE":
        newtag = "DOSSIER:WFID_" + str(tagName) + ", wfe:" + val1['name']
    else:newtag = "TOP:WFID_" + str(tagName) + ", wfe:" + val1['name']
    # result = CM.add_tags_future(CardIds, newtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
    # CM.create_txt_card("dummy", "dummy", body['BusinessTag'], headers1, CardIds, BASE_URL, "true", "false")


    #### speed bedug comment
    # threadID = threadID + 1000
    # threads = []
    #
    # usualForms = ["Estimate", "Form F4", "Form F6", "Status Form F5"]
    #
    # for ele in usualForms:
    #
    #     threadID = threadID + 1
    #     threadname = "thread" + ele + val1['name']
        # threadname = usualThread(threadID, val1, ele, body, BASE_URL, headers1, wfectr)

        # create_usual_forms(val1, ele, body, BASE_URL, headers1, wfectr)


        # ************** WFE specibody['BusinessTag']fic forms  submission ******#
    for item in val1['forms']:
        for k, v in item.items():
            try:
                grp_name = v['AdminsR']
            except:
                grp_name = "N"
            form_key = val1['name'] + ":" + k

            try:
                try:

                    # if top_status in body['FormData']['Status']:

                    if "Active" in top_status :
                        fieldsmeta = json.dumps({"HideEditAction": False,"IsFormLinked": "true"})
                    else:
                        fieldsmeta = json.dumps({"HideEditAction": True,"IsFormLinked": "true"})
                except:
                    fieldsmeta = json.dumps({"HideEditAction": True,"IsFormLinked": "true"})
                result = CM.form_submission_using_NEW_API_meta(BASE_URL, body['BusinessTag'], headers1, cardList[form_key],
                                                      item[k]['fields'], fieldsmeta)  # submitting form
            except:
                logging.warning("This is an illegal form submission " + form_key)
            s_id = str(result)
            # logging.warning(s_id)

            # tagName = body['WorkflowID']
            # cardtag = val1['name'] + ":WFID_" + str(tagName) + "," + k
            # tagName = val1['name'] + ":" + val1['subFlow'] + ":WFID_" + str(tagName) + "," + k
            # taskTagname = "task:" + tagName
            CM.add_tags_future(s_id, newtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])


            # for task in v['taskList']:
            #     # threadID = threadID + 10000
            #     # threadname = "thread" + s_id + str(task)
            #     logging.error(" the task tag generated is  : " + taskTagname)
            #     create_and_tag_task(s_id, val1, task, body, BASE_URL, headers1, taskTagname)
            #     # threadname = taskThread(threadID, s_id, val1, task, body, BASE_URL, headers1, taskTagname)
            #     # threadname.start()
            #     # threads.append(threadname)

        # for t in threads:
        #     t.join()

    return threads




def create_and_tag_task(s_id, val1, task, body, BASE_URL, headers1, taskTagname):

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
        task_priority = body['FormData']['Priority']
        # task_priority = priority
        if task_priority == "FastTrack":
            priority = "Priority1"
        else:
            priority = "Priority5"
        # elif task_priority == "3":
        #     priority = "Priority3"
        # elif task_priority == "4":
        #     priority = "Priority4"
        # elif task_priority == "5 (Lowest)":
        #     priority = "Priority5"
    except:
        try:
            result = json.loads(CM.get_all_tagIds(toptag, BASE_URL, body['BusinessTag'], headers1))
            for f_name in result['data']['elements']:
                if "Project Initiation" in f_name['title']:
                    data = json.loads(f_name['content'])
            # result = json.loads(result['data']['elements'][0]['content'])
                    for e1 in data['Elements'][0]['Elements']:
                        if "Priority" in e1['FieldLabel']:
                            priority = e1['Value']

            task_priority = priority
            if task_priority == "FastTrack":
                priority = "Priority1"
            else:priority = "Priority5"
            # elif task_priority == "2":
            #     priority = "Priority2"
            # elif task_priority == "3":
            #     priority = "Priority3"
            # elif task_priority == "4":
            #     priority = "Priority4"
            # elif task_priority == "5 (Lowest)":
            #     priority = "Priority5"

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
    mgrgroup = flow + "mgr_" + str(tagName)
    try:
        newgrpID = CM.create_groups(grpname, flow + " group for project : " + body['FormData']['Applicant Name'], headers1, body['BusinessTag'], BASE_URL)
        mgrgrpID = CM.create_groups(mgrgroup, flow + " group for project : " + body['FormData']['Applicant Name'],headers1, body['BusinessTag'], BASE_URL)
    except:
        logging.error("could not create user group " + flow + str(body['WorkflowID']))


     #**********  this code is commented (Hardik told) *************************************
    # try:
    #     grp_name = flow + "mgr"
    #     grp_ID = CM.find_out_grp_ID(grp_name, headers1, body['BusinessTag'], BASE_URL)
    #     by = {'grpUserGroupID': grp_ID}
    #     CM.add_usergrps_grps(BASE_URL, json.dumps(by), headers1, body['BusinessTag'], newgrpID)
    #
    # except:
    #     logging.error("could not add manager group ")
    #******************************************************************************************

    if "CHAT" in flow:
        forum_id = CM.create_FORUM_card("CHAT", body['BusinessTag'], BASE_URL, headers1,parentID)
        CardIds = str(forum_id)

    elif "COE" in flow:
        result = CM.create_txt_card("BRAND ENTREPRENEUR", "", body['BusinessTag'], headers1, parentID, BASE_URL, "false", "true")
        CardIds = str(result)
    else:
        result = CM.create_txt_card(flow, "", body['BusinessTag'], headers1, parentID, BASE_URL, "false", "true")
        CardIds = str(result)

    if "CHAT" in flow:
        tagnames = tagNameTop + "," + "subflow:" + flow + "," + "CHAT:"+tagNameTop
    else:
        tagnames = tagNameTop + "," + "subflow:" + flow

    CM.add_tags_future(CardIds, tagnames, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

    if "CHAT" in flow:
        logging.warning("no need to add text card")
        # newtag = flow + ":WFID_" + str(tagName)
        # forum_id = CM.create_FORUM_card("FORUM",body['BusinessTag'],BASE_URL,headers1,CardIds)
        # result = CM.add_tags_future(str(forum_id), newtag, BASE_URL, body['BusinessTag'], headers1, tagName)
    else:
        CM.create_txt_card("dummy", "dummy", body['BusinessTag'], headers1, CardIds, BASE_URL, "true", "false")
    return CardIds

def create_usual_forms(val1, ele, body, BASE_URL, headers1, wfectr):
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
            fields['Estimated Cost'] = wfectr['c']
            fields['Estimated Time'] = wfectr['t']
            fields['Estimated Resource'] = wfectr['r']

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
        # skiptag = "skip::" + tagName1  ### enable this one for prod
        result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_id, fields)
        CM.add_tags_future(str(result), skiptag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])


    if ele == "Status":
        fieldname = {}
        try:
            fieldname['Status'] = val1['status']
        except:
            fieldname['Status'] = "Not Started"
        fields = fieldname
        try:
            if "Active" in body['FormData']['Status']:
                fieldsmeta = json.dumps({"HideEditAction": False})
            else:
                fieldsmeta = json.dumps({"HideEditAction": True})
        except:
            fieldsmeta = json.dumps({"HideEditAction": True})
        result = CM.form_submission_using_NEW_API_meta(BASE_URL, body['BusinessTag'], headers1, form_id, fields, fieldsmeta)
        CM.add_tags_future(str(result), tagName1, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

    if ele == "Dependencies":
        try:
            fields = val1['dependencies']
        except:
            fields = []
        depTagname = "backend::" + tagName1
        result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_id, fields)
        CM.add_tags_future(str(result), depTagname, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

    # return firstelemFlag


def create_wfes(body, masterfileName, headers1, BASE_URL):
    # k = str(body['BusinessTag']) + "_" + str(body['FormData']['wid'])
    # v = "S"
    # CM.writeshelf(k, v)
    #
    # result = CM.readshelf(k)
    # logging.warning(result)



    threads = []

    body['WorkflowID'] = body['FormData']['wid']

    # filepath = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/wfes/"
    # filepath_server = "/var/www/cgi-bin/workflow/wfes/"
    masterFile =  filepath + masterfileName
    masterFile_server = filepath_server + masterfileName
    # standard_C_T_R = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
    # standard_C_T_R = "/var/www/cgi-bin/workflow/WFE_Time_Cost.csv"
    # standard_C_T_R = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/TwigMeScripts/python/WFE_Time_Cost.csv"


    cardIDlistFile = filepath + "form_tables.csv"
    cardIDlistFile_server = filepath_server + "form_tables.csv"
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
    # with open(standard_C_T_R, 'r') as rf:
    #     data = csv.reader(rf, delimiter=',')
    #     if hasHeader == "Y":
    #         row1 = data.next()
    #     for row in data:
    #         elctr = {}
    #         wfekey = row[1]
    #         elctr['t'] = row[2]
    #         elctr['c'] = row[4]
    #         elctr['r'] = row[3]
    #         elctrall[wfekey] = elctr


    try:
        lisval = WP.parse_wfe_list(masterFile)
    except:
        lisval = WP.parse_wfe_list(masterFile_server)

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


    # createFile = "./wfcreate_" + body['WorkflowID'] + ".log"
    #
    # setup_logger('log_one', createFile)
    #
    # log = logging.getLogger('log_one')

    createFile = "/var/www/cgi-bin/workflow/log/wfcreate_" + body['WorkflowID'] + ".log"
    createFile_PKG = "/var/www/cgi-bin/workflow/log/wfcreate_PKG_" + body['WorkflowID'] + ".log"
    # createFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/wfcreate_" + body['WorkflowID'] + ".log"
    # createFile_PKG = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/wfcreatePKG_" + body['WorkflowID'] + ".log"
    logging.error(createFile)
    if "WFE_subflow_PKG" in masterfileName:
        setup_logger('log_one', createFile_PKG)
    else:
        setup_logger('log_one', createFile)
    logging.error("fail")
    log = logging.getLogger('log_one')
    log.warning(masterfileName)


    try:
        for flow in lisval['subflows']:
            log.warning(flow)
            # threadID = threadID + 1
            # threadname = "thread" + flow
            # threadname = grpThread(threadID, body, flow, BASE_URL, headers1, parentID)
            # threadname.start()
            # threads.append(threadname)
            create_user_grps(body, flow, BASE_URL, headers1, parentID)
    except:
        logging.warning("No subflow was defined")

    try:
        tag = "TOP:WFID_" + str(body['WorkflowID'])
        result = json.loads(CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'], headers1))
        for formname in result['data']['elements']:
            if "Application" in formname['title']:
                data = json.loads(formname['content'])
                for el in data['Elements'][0]['Elements']:
                    if "Status" in el['FieldLabel']:
                        top_status = el['Value']

        # result = json.loads(result['data']['elements'][0]['content'])
        #     for el in data['Elements'][0]['Elements']:
        #         if "Status" in el['FieldLabel']:
        #             top_status = el['Value']
        #             print top_status
    except:
        top_status = "Not Started"

    for wfe in lisval['wfes']:
        threadID = threadID + 10000

        logging.warning(wfe)
        log.warning(wfe)
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



        threads = create_worflow_elements(wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1, threadID, threads, wfectr, cardList, top_status)

        # threadname = "thread" + wfe
        # threadname = wfeThread(threadID, wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1)
        # threadname.start()
        # threads.append(threadname)
    #
    # for t in threads:
    #     t.join()
    #

    # logging.warning(str(lisval))
    # threads1 = []
    for wfe in lisval['spewfes']:
        log.warning(wfe)
        create_special_worflow_elements(wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1, threadID,
                                threads, wfectr, cardList, top_status)

    for wfe in lisval['deptwfes']:
        logName = wfe + "_CONFIG"
        log.warning(logName)
        # threadID = 15000
        # threadname = "thread" + wfe
        # logging.warning(" firing off the thread " +  wfe)
        # threadname = configThread(threadID, wfe, lisval, wfesparentID, parentID, filepath, filepath_server, body, BASE_URL, headers1)
        create_config_cards(wfe, lisval, wfesparentID, parentID, filepath, filepath_server, body, BASE_URL, headers1)

    # try:
    #     if "Active" in top_status:
    #         fieldsmeta = json.dumps({"HideEditAction": False,"IsFormLinked": "true"})
    #     else:
    #         fieldsmeta = json.dumps({"HideEditAction": True,"IsFormLinked": "true"})
    # except:
    #     fieldsmeta = json.dumps({"HideEditAction": True,"IsFormLinked": "true"})
    #
    # input_data = {}
    # form_key = 95653        # form for WFE Form Linking
    # result = CM.form_submission_using_NEW_API_meta(BASE_URL, body['BusinessTag'], headers1,form_key,input_data, fieldsmeta)
    # logging.warning(result)
    # s_id = str(result)
    # newtag = "TOP:WFID_" + str(body['WorkflowID'])
    # CM.add_tags_future(s_id, newtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

    # k = str(body['BusinessTag']) + "_" + str(body['FormData']['wid'])
    # v = "F"
    # CM.writeshelf(k, v)
    #
    # result = CM.readshelf(k)
    # logging.warning(result)


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
    if wfe == "COE":
        result = CM.create_txt_card("BRAND ENTREPRENEUR_CONFIG", "Configure the workflow here", body['BusinessTag'], headers1,wfesparentID,BASE_URL, "false", "true")
    else:
        result = CM.create_txt_card(topname, "Configure the workflow here", body['BusinessTag'], headers1,wfesparentID,BASE_URL, "false", "true")

    CardIds = str(result)
    logging.warning(CardIds)
    tagName = body['WorkflowID']
    tagNameTop = wfe + ":WFID_" + str(tagName)
    # tagNameTop = wfe + ":WFID:" + str(tagName)

    # allowedusers = wfe + "mgr"
    # operator_per = wfe + "HOD"
    # config_permission = ["SMGT","MGR","HOD"]
    # for per in config_permission:
        # CM.set_card_permissions(BASE_URL, allowedusers, CardIds, body['BusinessTag'], "VIEW", headers1)
    CM.set_card_permissions(BASE_URL, "All Org Users", CardIds, body['BusinessTag'], "VIEW", headers1)
    #     CM.set_card_permissions(BASE_URL, per, CardIds, body['BusinessTag'], "OPERATOR", headers1)
        # CM.set_card_permissions(BASE_URL, operator_per, CardIds, body['BusinessTag'], "OPERATOR", headers1)

    tagnames = tagNameTop + "," + "wfe:" + topname
    result = CM.add_tags_future(CardIds, tagnames, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
    CM.create_txt_card("dummy", "dummy", body['BusinessTag'], headers1, CardIds, BASE_URL, "true", "false")

    tagT = ""
    for ele in lisval['wfes']:
        if wfe in ele:

            # newtag = "task:" + ele + ":WFID:" + str(body['WorkflowID'])
            newtag = "task:" + ele + ":" + wfe + ":WFID_" + str(body['WorkflowID'])
            if tagT == "":
                tagT = newtag
            else:
                tagT = tagT + "," + newtag

    result = json.loads(CM.get_all_tagIds(tagT, BASE_URL, body['BusinessTag'], headers1))

    form_element = []
    grp_name = wfe + "p_" + str(body['WorkflowID'])
    grp_ID = CM.find_out_grp_ID(grp_name, headers1, body['BusinessTag'], BASE_URL)

    alltasks = []
    alltasks = CM.unpaginate(result['data']['elements'], alltasks, headers1)

    for deptTasks in alltasks:
        elem = {}
        subid = ""
        wfename = ""
        for tag in deptTasks['tags']:
            subid = str(tag['CardID'])
            if (re.search(r'task:(.*):\w+:', tag['TagName'])):
                sstring = re.search(r'task:(.*):\w+:', tag['TagName'])
                wfename = sstring.group(1)

        filename = filepath + wfename + ".csv"
        filename_server = filepath_server + wfename + ".csv"
        ###### one wfe only below :::
        val1 = {}
        # try:
        #     # val1 = WP.parse_wfe(filename)
        #     data = pd.read_csv(filename, names=[0, 1, 2])
        #     desc = data[1][2]
        # except:
        #     # val1 = WP.parse_wfe(filename_server)
        #     data = pd.read_csv(filename_server, names=[0, 1, 2])
        #     desc = data[1][2]

        try:
            val1 = WP.parse_wfe(filename)
            desc = val1['desc']
        except:
            val1 = WP.parse_wfe(filename_server)
            desc = val1['desc']

        # elem['label'] = val1['desc'] + " : " + deptTasks['title']
        elem['label'] = desc + " : " + deptTasks['title']
        elem['type'] = "AUTO_COMPLETE"
        elem['required'] = 0
        elem['placeholder'] = ""
        elem['editable'] = "true"
        elem['values'] = grp_ID
        elem['python'] = subid
        elem['tagsUsed'] = tagT
        form_element.append(elem)

    logging.error("Got her fine for task creation form " + grp_ID)

    form = "Task Assignment Form"
    cardID = CM.form_card(BASE_URL, headers1, form, body['BusinessTag'], parentID)
    # logging.error("Got her fine for task creation form " + str(cardID))

    CM.set_card_permissions(BASE_URL, "All Org Users", str(cardID), body['BusinessTag'], "ALLLOWED_USERS",headers1)

    elem = {}
    elem['label'] = "Apply to all tasks in this form (adding a name in other task will override that particular task assignment)"
    elem['type'] = "AUTO_COMPLETE"
    elem['required'] = 0
    elem['placeholder'] = ""
    elem['editable'] = "true"
    elem['values'] = grp_ID
    elem['python'] = ""
    elem['tagsUsed'] = tagT

    form_element.append(elem)


    form_element_reversed_list = list(reversed(form_element))
    result = CM.create_form_elements(BASE_URL, headers1, body['BusinessTag'], cardID, form, form_element_reversed_list)
    fields = {}
    logging.error("Got her fine for form elements creation " + result)

    result1 = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, str(cardID), fields)
    newtag = topname + ":WFID_" + str(tagName) + "," + form
    resp = CM.add_tags_future(str(result1), newtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

    #####
    e_arr = []
    s_arr = []
    fields = {}
    logging.warning("###%%%%%%%%%%#####")
    logging.warning(lisval['wfes'])
    for ele in lisval['wfes']:
        elem = {}
        elem_1 = {}
        # tag = "estimate::" + ele + ":WFID_" + str(body['WorkflowID'])
        tag = ele + ":WFID_" + str(body['WorkflowID'])

        if wfe in ele:
            filename = filepath + ele + ".csv"
            filename_server = filepath_server + ele + ".csv"
            ###### one wfe only below :::
            val1 = {}

            try:
                val1 = WP.parse_wfe(filename)
                desc = val1['desc']
            except:
                val1 = WP.parse_wfe(filename_server)
                desc = val1['desc']

            result = json.loads(CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'], headers1))

            for alltag in result['data']['elements']:
                logging.warning(alltag)
                if "Estimate" in alltag['allTags']:
                    title = desc + " : Estimated Time"
                    sid = str(alltag['cardID'])
                    elem['label'] = title
                    elem['type'] = "EDIT_TEXT"
                    elem['required'] = 0
                    elem['placeholder'] = ""
                    elem['editable'] = "true"
                    elem['python'] = sid
                    e_arr.append(elem)

                    data = json.loads(alltag['content'])
                    for subelm in data['Elements'][0]['Elements']:
                        if "Estimated Time" in subelm['ElementID']:
                            val = subelm['Value']
                            fields[title] = val

                if "Skip" in alltag['allTags']:
                    sid = str(alltag['cardID'])
                    elem_1['label'] = desc
                    elem_1['type'] = "CHECK_BOX"
                    elem_1['required'] = 0
                    elem_1['placeholder'] = ""
                    elem_1['editable'] = "true"
                    elem_1['python'] = sid
                    s_arr.append(elem_1)

    form = "Update estimated Time Form"
    cardID = CM.form_card(BASE_URL, headers1, form, body['BusinessTag'], parentID)
    CM.set_card_permissions(BASE_URL, "All Org Users", str(cardID), body['BusinessTag'], "ALLLOWED_USERS",
                            headers1)

    # CM.set_card_permissions(BASE_URL, allowedusers, str(cardID), body['BusinessTag'], "OPERATOR", headers1)
    e_arr_reversed_list = list(reversed(e_arr))
    result = CM.create_form_elements(BASE_URL, headers1, body['BusinessTag'], cardID, form, e_arr_reversed_list)
    # fields = {}
    result1 = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, str(cardID), fields)
    newtag = topname + ":WFID_" + str(tagName) + "," + form
    resp = CM.add_tags_future(str(result1), newtag, BASE_URL, body['BusinessTag'], headers1,body['WorkflowID'])


    form = "Skip workflow stages form"
    cardID = CM.form_card(BASE_URL, headers1, form, body['BusinessTag'], parentID)
    CM.set_card_permissions(BASE_URL, "All Org Users", str(cardID), body['BusinessTag'], "ALLLOWED_USERS",
                            headers1)

    # CM.set_card_permissions(BASE_URL, allowedusers, str(cardID), body['BusinessTag'], "OPERATOR", headers1)
    s_arr_reversed_list = list(reversed(s_arr))
    result = CM.create_form_elements(BASE_URL, headers1, body['BusinessTag'], cardID, form, s_arr_reversed_list)
    fields = {}
    result1 = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, str(cardID), fields)
    newtag = topname + ":WFID_" + str(tagName) + "," + form
    resp = CM.add_tags_future (str(result1), newtag, BASE_URL, body['BusinessTag'], headers1,body['WorkflowID'])

def user_addition_using_Form(body, BASE_URL, headers1):
    # file_name = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/add_user_to_group.csv"
    # file_name = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
    file_name = "/var/www/cgi-bin/workflow/Haldiram_UserAdditionMapping.csv"
    hasHeader = "Y"
    name = body['FormData']['Name']
    # department = body['FormData']['Team']
    role = body['FormData']['Role']
    email_ID = body['FormData']['Email']

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


    result = CM.create_user_group(BASE_URL, headers1, name, body['BusinessTag'])
    result = result['reply']
    result_1 = json.loads(result)
    g_ID = result_1['output']['groupdetails']['groupid']
    result = CM.add_user_to_group(g_ID,user_id,body['BusinessTag'], headers1, BASE_URL)
    logging.warning(result)

    with open(file_name, 'r') as rf:
        # user_id = "8RQ53HA67RFHP"
        data = csv.reader(rf, delimiter=',')
        if hasHeader == "Y":
            row1 = data.next()
        for row in data:
            if role.strip() in row[0].strip():
                grp_name = row[1]
                usergroups = CM.getAllUserGroups(headers1, body['BusinessTag'],BASE_URL,grp_name)
                grpvals = json.loads(usergroups)
                grps = grpvals['output']
                grpname = grps['usergroup']
                dict1 = grpname
                grpID = dict1[grp_name]
                g_ID = str(grpID)
                result = CM.add_user_to_group(g_ID,user_id,body['BusinessTag'], headers1, BASE_URL)
                logging.warning(result)
            else:logging.warning("we are not able to find role and manager")


def add_single_user_to_givenGroups(body, BASE_URL, headers1):
    # file_name = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/single_user_to_GROUP_form.csv"
    file_name = "/var/www/cgi-bin/workflow/single_user_to_GROUP_form.csv"
    hasHeader = "Y"
    user_id = body['FormData']['User Name']
    group_name = body['FormData']['User Group Name']
    with open(file_name, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        if hasHeader == "Y":
            row1 = data.next()
        for row in data:
            if group_name.strip() in row[0].strip():
                grp_name = row[1]
                usergroups = CM.getAllUserGroups(headers1, body['BusinessTag'], BASE_URL,grp_name)
                grpvals = json.loads(usergroups)
                grps = grpvals['output']
                grpname = grps['usergroup']
                dict1 = grpname
                grpID = dict1[grp_name]
                g_ID = str(grpID)
                result = CM.add_user_to_group(g_ID, user_id, body['BusinessTag'], headers1, BASE_URL)
                logging.warning(result)
            else:logging.warning("Not able to find user group")

def add_SPINNER_elements_IN_FORM(body, BASE_URL, headers1):
    try:
        brand_name = body['FormData']['Brand Name']
        field_name = body['FormData']
    except:
        brand_name = body['FormData']['New Product Category Name']
        field_name = body['FormData']

    if "Brand Name" in field_name:
        f_title = "Brand"
    else:
        f_title = "Product Category"

    b = {}
    url = BASE_URL + "all_actions/" + body['BusinessTag'] + "/form/94847"
    method = "GET"
    jsonresponse = CM.hit_url_method(b, headers1, method, url)

    result = CM.edit_form_spinner_element(BASE_URL,body['BusinessTag'],headers1,jsonresponse,f_title,brand_name)
    logging.warning("Spinner updated successfully")
    logging.warning(result)

def assign_task_to_user(body, BASE_URL, headers1):
    form_ID = 95600
    input_data = {}
    sub_id = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID, input_data)
    task_name = body['FormData']['Title']
    task_desc = body['FormData']['Description']
    end_date = body['FormData']['Due Date']
    grp = body['FormData']['Assign to']
    grp_id = json.loads(grp)
    grp_id_1 = grp_id['GroupIDs']
    for g_id in grp_id_1:
        method = "POST"
        url = BASE_URL + "tasks/add/" + body['BusinessTag']
        body1 = {}
        startdate = datetime.datetime.utcnow()
        sd = startdate.strftime('%Y-%m-%d %H:%M:%S')
        end_date = end_date + " " + "00:00:00"
        body1['CardID'] = str(sub_id)
        body1['Title'] = task_name
        body1['Description'] = task_desc
        body1['UserGroupIDLevel1'] = int(g_id)
        body1['StartDate'] = sd
        body1['EndDate'] = end_date
        body1['Status'] = "Active"
        response = CM.hit_url_method(body1, headers1, method, url)
        logging.warning(response)

def complete_Adhoc_TASK(body, BASE_URL, headers1):
    t_flag = body['FormData']['Completed']
    if t_flag == "true":
        result = CM.get_all_tasks_on_cardID(BASE_URL, body['BusinessTag'], headers1, body['FormSubmissionID'])
        for task_id in json.loads(result)['data']['elements']:
            t_ID = task_id['cardID']
            task_status = "Completed"
            result = CM.edit_task_forOnlyFor_changeStatus(BASE_URL,body['BusinessTag'],headers1,t_ID,task_status)
            logging.warning("Task is completed")
            logging.warning(result)
    else:logging.warning("Task is not ready to COMPLETE")


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

                #************************* code for Debug********************************
                # if "Carton" in body['FormData']['Packaging Type?']:
                #     masterFileName = "WFE_subflow_PKG1.csv"
                #     create_wfes(body, masterFileName, headers1, BASE_URL)
                # #**************************************************************************

                logging.warning("packaging form is resubmitted")
            else:
                logging.error("something is wrong in the packaging form submission")

        except:
            CM.add_val_in_table(BASE_URL, headers1, formkey, 112, body['BusinessTag'],int(wfid))
            if "Carton" in body['FormData']['Packaging Type?']:
                masterFileName = "WFE_subflow_PKG1.csv"
                create_wfes(body, masterFileName, headers1, BASE_URL)
            elif "Flexible" in body['FormData']['Packaging Type?']:
                logging.warning("PKG creation is start")
                masterFileName = "WFE_subflow_PKG2.csv"
                create_wfes(body, masterFileName, headers1, BASE_URL)
                logging.warning("PKG creation is done")
            elif "Rigid" in body['FormData']['Packaging Type?']:
                masterFileName = "WFE_subflow_PKG3.csv"
                create_wfes(body, masterFileName, headers1, BASE_URL)
            else:
                logging.warning("packaging form is blank")

            grpname = "PKGmgr" + str(wfid)

            tag = "TOP:WFID_" + str(wfid)
            result = json.loads(CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'], headers1))
            for f_name in result['data']['elements']:
                if "Project Management" in f_name['title']:
                    data = json.loads(f_name['content'])
                    for e1 in data['Elements'][0]['Elements']:
                        if "Project Title" in e1['FieldLabel']:
                            workFlow_Name = e1['Value']

            # workFlow_Name = workFlow_Name
            logging.warning(workFlow_Name)
            mail = {}
            mail['title'] = "Packaging workflow for " + '"' + workFlow_Name + '"' + " is successfully created"
            mail['msg'] = "Based on your inputs packaging workflow for " + workFlow_Name + " is successfully created. Please assign team members to the tasks."
            mail['commtype'] = ["MAIL"]
            mail['groupname'] = [grpname]
            method = "POST"
            url = BASE_URL + "usergroups/message/" + body['BusinessTag']
            resp = CM.hit_url_method(mail, headers1, method, url)
            logging.warning(resp)
            logging.warning("MAIL for PKG")


            mail = {}
            mail['title'] = "Packaging workflow for " + '"' + workFlow_Name + '"' + " is successfully created"
            mail['msg'] = "Based on your inputs packaging workflow for " + workFlow_Name + " is successfully created. Please assign team members to the tasks."
            mail['commtype'] = ["NOTIFY"]
            mail['groupname'] = [grpname]
            method = "POST"
            url = BASE_URL + "usergroups/message/" + body['BusinessTag']
            resp = CM.hit_url_method(mail, headers1, method, url)
            logging.warning(resp)
            logging.warning("Notification for PKG")


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
    formkey = "created1_" + body['FormData']['wid']
    tagNamesub = "WFID_" + body['FormData']['wid']
    wid = body['FormData']['wid']

    if body['FormData']['Applicant Name'] is None:
        logging.warning("Blank form submission")
    else:

        try:
            # try:
            #     logging.warning("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
            #     logging.warning(body['FormData'])
            #     grpname = "TOPp_" + str(body['FormData']['wid'])
            #     logging.warning(grpname)
            #
            #
            #
            #     # newgrpID = CM.create_groups(grpname, "TOP group for project : " + body['FormData']['Project Title'],
            #     #                             headers1, body['BusinessTag'], BASE_URL)
            #     # logging.warning(newgrpID)
            #
            #     lead = []
            #     lia_lead = body['FormData']['Liaisoning Lead']
            #     lead.append(lia_lead)
            #     civil_lead = body['FormData']['Civil Lead']
            #     lead.append(civil_lead)
            #     contractor_lead = body['FormData']['Electrical Contractor Lead']
            #     lead.append(contractor_lead)
            #     trans_lead = body['FormData']['Electrical Transformer Lead']
            #     lead.append(trans_lead)
            #     cable_lead = body['FormData']['Electrical Cable Lead']
            #     lead.append(cable_lead)
            #     mech_lead = body['FormData']['Mechanical Lead']
            #     lead.append(mech_lead)
            #     logging.warning(lead)
            #
            #
            #     # grpname = "TOPp_" + str(body['FormData']['wid'])
            #     # g_ID = CM.find_out_grp_ID(grpname,headers1,body['BusinessTag'],BASE_URL)
            #
            # except:
            #     # logging.exception("error")
            #     logging.error("adding users to group fails")


            createdvalue = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], formkey)
            createdvalue = json.loads(createdvalue)
            createdvalue = createdvalue['data']['value']['_value']
            if createdvalue == "113":
                logging.warning("resubmit")
                #
                # masterFileName = "WFE_subflow_NPD1.csv"
                # create_wfes(body, masterFileName, headers1, BASE_URL)
                # print "execution is done"
                #

                tag1 = "DOCSEARCH::" + tagNamesub
                result = json.loads(CM.get_all_tagIds(tag1, BASE_URL, body['BusinessTag'], headers1))
                cards = {}
                allresults = []
                # allresults = result['data']['elements']
                allresults = CM.unpaginate(result['data']['elements'], allresults, headers1)
                cardsarray = []
                #
                for card in allresults:
                    try:
                        cont = json.loads(card['content'])
                        formID = cont['FormID']
                        subID = cont['FormSubmissionID']
                        if str(formID) != workflowTopFormID:
                            cardsarray.append(str(subID))
                        else:
                            continue
                        cards[formID] = subID
                    except:
                        continue
                # print result
                method = "PUT"
                url = BASE_URL + "bulk/" + body['BusinessTag'] + "/formsubmissions/"
                try:
                    if "Active" in body['FormData']['Status']:
                        fieldsmeta = json.dumps({"HideEditAction": False})
                        # for k,v in cards.items():
                        b = {}
                        b['FormSubmissionID'] = cardsarray
                        b['MetaData'] = fieldsmeta
                        b['OverrideMetaData'] = False
                        resp = CM.hit_url_method(b, headers1, method, url)
                        logging.warning(resp)
                        # print resp
                            #
                            # *{
                            #     *"FormSubmissionID": [1, 2, 3, ...]
                            #                          * "MetaData": "<JSON ENCODED MetaData>"
                            # CM.EDIT_submission_metadata(BASE_URL, body['BusinessTag'], headers1, k, fieldsmeta, v)
                    else:
                        fieldsmeta = json.dumps({"HideEditAction": True})
                        b = {}
                        b['FormSubmissionID'] = cardsarray
                        b['MetaData'] = fieldsmeta
                        b['OverrideMetaData'] = False
                        resp = CM.hit_url_method(b, headers1, method, url)

                except:
                    fieldsmeta = json.dumps({"HideEditAction": True})
                    # for k, v in cards.items():
                    #     CM.EDIT_submission_metadata(BASE_URL, body['BusinessTag'], headers1, k, fieldsmeta, v)

                ##below section is for debug only

                #
                # if body['FormData']['Project Type?'] == "New Brand/Product" or body['FormData'][
                #     'Project Type?'] == "Product Variant" or body['FormData'][
                #     'Project Type?'] == "New SKU/Pack":
                #     # masterFileName = "WFE_subflow_NPD1.csv"
                #     masterFileName = "WFE_subflow_try.csv"
                #     create_wfes(body, masterFileName, headers1, BASE_URL)

                ######################




            else:
                CM.add_val_in_table(BASE_URL, headers1, formkey, 113, body['BusinessTag'],int(wid))
                if body['FormData']['Student Type'] == "Under Graduate" or body['FormData']['Student Type'] == "Graduate" or body['FormData']['Student Type'] == "Post Graduate":
                    # logging.warning("creation is start")
                    masterFileName = "admin_list.csv"
                    create_wfes(body, masterFileName, headers1, BASE_URL)
                    # logging.warning("Creation is done")
                # elif body['FormData']['Project Type'] == "New SKU" or body['FormData']['Project Type'] == "New Pack":
                #     masterFileName = "WFE_subflow_NPD2.csv"
                #     create_wfes(body, masterFileName, headers1, BASE_URL)
                else:
                    logging.error("Project type not specified. Doing Nothing")

                # logging.warning("Trying to add users in user groups")

                # try:
                #     for person in lead:
                #         if person == '':
                #             logging.warning("empty field")
                #         else:
                #             logging.warning(person)
                #             result = CM.add_user_to_group(g_ID, person, body['BusinessTag'], headers1, BASE_URL)
                #             logging.warning(result)
                #             ### Send emails
                #
                #             # ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
                #             # ************    This Code is for sending MAIL  **********************************
                #     mail = {}
                #     mail['title'] = body['FormData']['Project Title'] + " is successfully created"
                #     # mail['title'] = "Workflow step complete"
                #     mail['msg'] = body['FormData']['Project Title']  + " has been succesfully created"
                #     mail['commtype'] = ["MAIL"]
                #     mail['groupname'] = [grpname]
                #     # mail['CardID'] = t_cardID
                #     method = "POST"
                #     url = BASE_URL + "usergroups/message/" + body['BusinessTag']
                #     resp = CM.hit_url_method(mail, headers1, method, url)
                #     logging.warning(resp)
                # except:
                #     logging.error("Add to groups failed")
        except:
            # logging.exception("error")
            CM.add_val_in_table(BASE_URL, headers1, formkey, 113, body['BusinessTag'],int(wid))
            if body['FormData']['Student Type'] == "Under Graduate" or body['FormData']['Student Type'] == "Graduate" or body['FormData']['Student Type'] == "Post Graduate":
                logging.warning("creation is start")
                masterFileName = "admin_list.csv"
                create_wfes(body, masterFileName, headers1, BASE_URL)
                logging.warning("Creation is done")
                # create_wfes(body, masterFileName, headers1, BASE_URL)
            # elif body['FormData']['Project Type'] == "New SKU" or body['FormData']['Project Type'] == "New Pack":
            #     logging.warning("creation is start")
            #     masterFileName = "WFE_subflow_NPD2.csv"
            #     create_wfes(body, masterFileName, headers1, BASE_URL)
            #     logging.warning("Creation is done")
            else:
                logging.error("Project type not specified. Doing Nothing")


                # ************    This Code is for sending MAIL  **********************************
            try:
                grpname = "TOPp_" + str(body['FormData']['wid'])
                g_ID = CM.find_out_grp_ID(grpname, headers1, body['BusinessTag'], BASE_URL)
                lead = ["Manasi"]
                for inside_group in lead:
                    grp_in_grp_ID = CM.find_out_grp_ID(inside_group, headers1, body['BusinessTag'], BASE_URL)
                    by = {'grpUserGroupID': str(grp_in_grp_ID)}
                    result = CM.add_usergrps_grps(BASE_URL, json.dumps(by), headers1, body['BusinessTag'], g_ID)
                    logging.warning("Adding group to group")
                    logging.warning(result)

            except:logging.warning("adding fail in leads to TOP grp")
            #
            # mail = {}
            # mail['title'] = "Project " + '"' + body['FormData']['Project Name'] + '"' + " is successfully created"
            # mail['msg'] = "Project " + '"' + body['FormData']['Project Name'] + '"' + " is successfully created.<br> Please assign team members to the tasks."
            # mail['commtype'] = ["MAIL"]
            # mail['groupname'] = [grpname]
            # # mail['CardID'] = t_cardID
            # method = "POST"
            # url = BASE_URL + "usergroups/message/" + body['BusinessTag']
            # resp = CM.hit_url_method(mail, headers1, method, url)
            # logging.warning("sending proj completion Mail")
            # logging.warning(resp)
            #
            # mail = {}
            # mail['title'] = "Project " + '"' + body['FormData']['Project Name'] + '"' + " is successfully created"
            # mail['msg'] = "Project " + '"' + body['FormData'][
            #     'Project Name'] + '"' + " is successfully created.<br> Please assign team members to the tasks."
            # mail['commtype'] = ["NOTIFY"]
            # mail['groupname'] = [grpname]
            # # mail['CardID'] = t_cardID
            # method = "POST"
            # url = BASE_URL + "usergroups/message/" + body['BusinessTag']
            # resp = CM.hit_url_method(mail, headers1, method, url)
            # logging.warning("sending proj completion Notification")
            # logging.warning(resp)

        # try:

            # if lia_lead == '':
            #     logging.warning("LIA is empty field")
            # else:
            #     logging.warning("LIA lead present")
            #     m_gname = "LIAmgr_" + str(body['FormData']['wid'])
            #     g_id = CM.find_out_grp_ID(m_gname, headers1, body['BusinessTag'], BASE_URL)
            #     result = CM.add_user_to_group(g_id, lia_lead, body['BusinessTag'], headers1, BASE_URL)
            #     logging.warning(result)
            #
            # if civil_lead == '':
            #     logging.warning("CIVIL is empty field")
            # else:
            #     logging.warning("CIVIL lead present")
            #     m_gname = "CVLmgr_" + str(body['FormData']['wid'])
            #     g_id = CM.find_out_grp_ID(m_gname, headers1, body['BusinessTag'], BASE_URL)
            #     result = CM.add_user_to_group(g_id, civil_lead, body['BusinessTag'], headers1, BASE_URL)
            #     logging.warning(result)
            #
            # if contractor_lead == '':
            #     logging.warning("Contractor is empty field")
            # else:
            #     logging.warning("Contractor lead present")
            #     m_gname = "ECNTmgr_" + str(body['FormData']['wid'])
            #     g_id = CM.find_out_grp_ID(m_gname, headers1, body['BusinessTag'], BASE_URL)
            #     result = CM.add_user_to_group(g_id, contractor_lead, body['BusinessTag'], headers1, BASE_URL)
            #     logging.warning(result)
            #
            # if trans_lead == '':
            #     logging.warning("Transformer is empty field")
            # else:
            #     logging.warning("Transformer lead present")
            #     m_gname = "ETRFmgr_" + str(body['FormData']['wid'])
            #     g_id = CM.find_out_grp_ID(m_gname, headers1, body['BusinessTag'], BASE_URL)
            #     result = CM.add_user_to_group(g_id, trans_lead, body['BusinessTag'], headers1, BASE_URL)
            #     logging.warning(result)
            #
            # if cable_lead == '':
            #     logging.warning("Cable is empty field")
            # else:
            #     logging.warning("Cable lead present")
            #     m_gname = "ECBLmgr_" + str(body['FormData']['wid'])
            #     g_id = CM.find_out_grp_ID(m_gname, headers1, body['BusinessTag'], BASE_URL)
            #     result = CM.add_user_to_group(g_id, cable_lead, body['BusinessTag'], headers1, BASE_URL)
            #     logging.warning(result)
            #
            # if mech_lead == '':
            #     logging.warning("Mechanical is empty field")
            # else:
            #     logging.warning("Mechanical lead present")
            #     m_gname = "MECmgr_" + str(body['FormData']['wid'])
            #     g_id = CM.find_out_grp_ID(m_gname, headers1, body['BusinessTag'], BASE_URL)
            #     result = CM.add_user_to_group(g_id, mech_lead, body['BusinessTag'], headers1, BASE_URL)
            #     logging.warning(result)

            #
            # grpname = "TOPp_" + str(body['FormData']['wid'])
            # g_ID = CM.find_out_grp_ID(grpname, headers1, body['BusinessTag'], BASE_URL)
            # for person in lead:
            #     if person == '':
            #         logging.warning("empty field")
            #     else:
            #         logging.warning(person)
            #         result = CM.add_user_to_group(g_ID, person, body['BusinessTag'], headers1, BASE_URL)
            #         logging.warning(result)

            # grpname = "TOPp_" + str(body['FormData']['wid'])
            # g_ID = CM.find_out_grp_ID(grpname, headers1, body['BusinessTag'], BASE_URL)
            # lead = ["SMGT", "MGR", "HOD", "TEAM"]
            # for inside_group in lead:
            #     grp_in_grp_ID = CM.find_out_grp_ID(inside_group, headers1, body['BusinessTag'], BASE_URL)
            #     by = {'grpUserGroupID': str(grp_in_grp_ID)}
            #     result = CM.add_usergrps_grps(BASE_URL, json.dumps(by), headers1, body['BusinessTag'], g_ID)
            #     logging.warning("Adding group to group")
            #     logging.warning(result)

                        # group = ["SeniorManagement","StrategyOffice","HOD"]
            # for inside_group in group:
            #     grp_in_grp_ID = CM.find_out_grp_ID(inside_group, headers1, body['BusinessTag'], BASE_URL)
            #     by = {'grpUserGroupID': str(grp_in_grp_ID)}
            #     result = CM.add_usergrps_grps(BASE_URL, json.dumps(by), headers1, body['BusinessTag'], g_ID)
            #     logging.warning("Adding group to group")
            #     logging.warning(result)


        # except:
        #     logging.error("Add to groups failed")


    logging.warning("@@@@@@@@@@@@@@@@@@@@@@@@@")
    logging.warning(datetime.datetime.now())
    logging.warning("@@@@@@@@@@@@@@@@@@@@@@@@@")


def mainworkflow(body, h1, B_URL):


    global filepath
    global filepath_server
    global logFilePath
    global logFilePath_server

    global BASE_URL
    global headers1

    BASE_URL = B_URL
    headers1 = h1

    # filepath = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/6DEC_data_FG/"

    filepath_server = "/var/www/cgi-bin/workflow/Calpoly/"
    filepath = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/Prod_Server_WORKFLOW/Calpoly/wfe/"
    # filepath_server = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/Test_Server_workflow/Haldiram/wfe/"

    workflowTopFormID = "27"     ## Top Project management form TEST SERVER form ID
    # create_user_formID = "5849"  #### user addition
    # packagingform = "117"

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
        #
        # elif body['FormID'] == create_user_formID:
        #     user_addition_using_Form(body, BASE_URL, headers1)


        elif len(body['tags']) > 0:

            try:
                tagsoncard = body['tags']
            except:
                try:
                    tags = CM.get_tags_by_cardID(body['FormSubmissionID'], BASE_URL, body['BusinessTag'], headers1 )
                    tagsoncard = json.loads(tags)['data']['elements'][0]['allTags']
                except:
                    logging.warning("Nothing to do here")

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

                if "_CONFIG" in decisionname:
                    # logging.warning(decisionname)
                    result = json.loads(CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1))
                    for alltag in result['data']['elements']:
                        if "Task Assignment Form" in alltag['allTags'] and "Task Assignment Form" in formname:
                            data = json.loads(alltag['content'])
                            elem = {}
                            statusd = {}
                            applyALLv = []
                            field_label = {}
                            field_label_1 = {}
                            flag = 0
                            for subelm in data['Elements'][0]['Elements']:
                                label = subelm['ElementID']
                                field_label[label] = subelm['Value']
                            for k,v in field_label.items():
                                if k == "Apply to all tasks in this form (adding a name in other task will override that particular task assignment)":
                                    try:
                                        applyALL = v
                                        applyALL = json.loads(applyALL)
                                        applyALLv = applyALL['GroupIDs']

                                    except:
                                        flag = 1
                                        logging.warning("No apply to all field ")
                            if flag is not 1:
                                for k,v in field_label.items():
                                    label = k
                                    try:
                                        assigned = json.loads(v)
                                        assignedv = assigned['GroupIDs']
                                        field_label_1[label] = assigned
                                    except:
                                        field_label_1[label] = applyALL
                                field_label_1[
                            'Apply to all tasks in this form (adding a name in other task will override that particular task assignment)'] = ""
                                result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1,body['FormID'], field_label_1, body['FormSubmissionID'])
                                result = json.loads(CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1))
                                for alltag in result['data']['elements']:
                                    if "Task Assignment Form" in alltag['allTags'] and "Task Assignment Form" in formname:
                                        data = json.loads(alltag['content'])
                                        for subelm_1 in data['Elements'][0]['Elements']:
                                            try:
                                                g_ID = subelm_1['Value']
                                                g_ID = json.loads(g_ID)
                                                g_ID = g_ID['GroupIDs']
                                                c_id = subelm_1['MetaData']['PYTHON']
                                                elem[c_id] = g_ID
                                            except:
                                                logging.warning("no user grp assigned")
                            else:
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

                        elif "Update estimated Time Form" in alltag['allTags'] and "Update estimated Time Form" in formname:
                            data = json.loads(alltag['content'])
                            for subelm in data['Elements'][0]['Elements']:
                                s_id = subelm['MetaData']['PYTHON']
                                estimate_value = subelm['Value']
                                form_ID = 26
                                input_data = {"Estimated Time": estimate_value}
                                result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID,input_data, s_id)

                        if "Skip workflow stages form" in alltag['allTags'] and "Skip workflow stages form" in formname:
                            data = json.loads(alltag['content'])
                            for subelm in data['Elements'][0]['Elements']:
                                s_id = subelm['MetaData']['PYTHON']
                                skip_flag = subelm['Value']
                                form_ID = 20
                                input_data = {"SKIP": skip_flag}
                                result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1,form_ID, input_data, s_id)
                                # combine_tag = "MKT_WFE1_4:WFID_420,Status Form F5"
                                # result = CM.combine_tag_gives_cardID(BASE_URL, body['BusinessTag'], headers1, combine_tag)
                                # print result
                                # form_ID = 13
                                # input_data = {"Status": "Skipped"}
                                # result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1,form_ID, input_data, s_id)


                elif "Status" in formname:
                    status = body['FormData']['Status']
                    estimateTag = "estimate::" + tagName
                    tasktag = "task:" + decisionname + ":" + st + ":" + wfidtag
                    estimateTag = "estimate::" + tagName

                    result = CM.get_all_tagIds(estimateTag, BASE_URL, body['BusinessTag'], headers1)
                    # value = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], "Estimate")
                    # value = json.loads(value)
                    # form_ID = value['data']['value']['_value']
                    try:
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
                            logging.warning("Status is ready to ACTIVE")
                            logging.warning(response)

                        if startExists == False:
                            input_data = {"Start Date": sd}
                            result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID, input_data, s_id)
                        else:
                            logging.warning("Start already exists")

                else:
                    try:
                #*********************  We are not putting thiscode on prod. so we are commenting this code  ***************************
                        # flag = "s"
                        # if "donotcall" in body['url_params']:
                        #     logging.warning("we are inside DONOTCALL")
                        #     check_flag = body['url_params']['donotcall']
                        #     flag = check_flag
                        #
                        # if flag == "t":
                        #     logging.warning("do not proceed for Linked submission")
                        #
                        # else:
                        #     logging.warning("WE are going inside METADATA")
                        #     result = CM.get_form_submission(body['FormSubmissionID'], body['BusinessTag'], BASE_URL, headers1)
                        #     for elm in json.loads(result)['data']['ondemand_action']:
                        #         if elm['MetaData'] != None:
                        #             logging.warning("metadata is not NONE")
                        #             link_proj = json.loads(elm['MetaData'])
                        #             for sub_link_proj in link_proj:
                        #                 if "LinkedProjects" in sub_link_proj:
                        #                     logging.warning("we are inside LINKED PROJECTS")
                        #                     wf_array = link_proj['LinkedProjects']
                        #
                        #                     if len(wf_array) != 0:
                        #                         logging.warning("array is not empty")
                        #                         for work_id in wf_array:
                        #                             form = formname
                        #                             tag = decisionname + ":WFID_" +str(work_id)
                        #                             combine_tag = form + "," + tag
                        #                             form_ID = body['FormID']
                        #                             input_data = body['FormData']
                        #                             result = CM.combine_tag_gives_cardID(BASE_URL, body['BusinessTag'], headers1, combine_tag)
                        #                             for sub_cardID in json.loads(result)['data']['elements']:
                        #                                 if form in sub_cardID['Tags']:
                        #                                     submission_cardID = sub_cardID['CardID']
                        #                                     result = CM.EDIT_submission_using_NEW_API_using_ChangeIn_URL(BASE_URL,body['BusinessTag'],
                        #                                                                                                  headers1,form_ID,input_data,submission_cardID)
                        #                                 else:logging.warning("Form name is not found")
                        #                     else:logging.warning("Multiselect workflow array is empty")
                        #                 else:logging.warning("not able to find Linked Project")
                        #         else:logging.warning("Meta data is NULL dont do anything")
                #******************************************************************************************************************************************************************
                        checkreq = {}
                        checkboxes = {}
                        c_tag = tagName
                        # hasHeader = "Y"
                        # mapping_Dossier = "/var/www/cgi-bin/workflow/dossier_wfe_files_mapping.csv"
                        # mapping_Dossier = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/dossier_wfe_files_mapping.csv"
                        result = json.loads(CM.get_all_tagIds(c_tag, BASE_URL, body['BusinessTag'], headers1))
                        for alltag in result['data']['elements']:
                            if formname in alltag['allTags']:
                                data = json.loads(alltag['content'])
                                for subelm in data['Elements'][0]['Elements']:
                                #************************ Minal code ** Code for attachment********************************
                                    # if "UPLOAD_FILE_IMAGE" in subelm['ElementType']:
                                    #     if subelm['Value'] is not None:
                                    #         f_url = subelm['Value']
                                    #         media_name = subelm['MetaData']['media_name']
                                    #         media_size = subelm['MetaData']['media_size']
                                    #         with open(mapping_Dossier, 'r') as rf:
                                    #             data = csv.reader(rf, delimiter=',')
                                    #             if hasHeader == "Y":
                                    #                 row1 = data.next()
                                    #             for row in data:
                                    #
                                    #                 if row[2] == formname:
                                    #                     tag = "DOSSIER:WFID_" + str(wfid)
                                    #                     result = CM.get_all_tagIds(tag,BASE_URL,body['BusinessTag'],headers1)
                                    #                     for f_name in json.loads(result)['data']['elements']:
                                    #                         if row[0] in f_name['title']:
                                    #                             sub_ID = f_name['cardID']
                                    #                             result = CM.attachment_API(BASE_URL,body['BusinessTag'],headers1, sub_ID, f_url,media_name, media_size)
                                    #                         else:
                                    #                             logging.warning("Name not found")
                                    #                 else:logging.warning("Form name is not found in file")
                                    #     else:logging.warning("File is not attached")
                                 #**********************************************************
                                    if "CHECK_BOX" in subelm['ElementType']:
                                        key = subelm['ElementID']
                                        req = subelm['MetaData']['PYTHON']
                                        # key = req
                                        value = subelm['Value']
                                        # print req
                                        # if req == "Mandatory":
                                        #     key = subelm['ElementID']
                                        #     value = subelm['Value']
                                    checkboxes[key] = value
                                    checkreq[key] = req


                    #     result = CM.get_form_submission(body['FormSubmissionID'], body['BusinessTag'], BASE_URL, headers1)
                    #     checkboxes = {}
                    #     for ele in result:
                    #         if "CheckBox" in ele['widget']:
                    #             for prop in ele['properties']:
                    #                 if prop['name'] == "text":
                    #                     key = prop['value']
                    #                 elif prop['name'] == "default":
                    #                     value = prop['value']
                    #             checkboxes[key] = value
                    except:
                        logging.warning("No checkboxes found")
                    flag = False
                    try:
                        for (k, v), (k2, v2) in zip(checkboxes.items(), checkreq.items()):
                        # for k,v in checkboxes.items():
                            if v2 == "Mandatory" and v == "false":
                                flag = True
                        if flag == False:
                            st = decisionname.split('_')
                            st = st[0]
                            tag = "task:" + decisionname + ":" + st + ":WFID_" + wfid  #### this is worong
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
                                if "Exit Checklist" in formname:
                                    logging.warning("This is Exit Checklist please dont send notification")
                                else:
                                    logging.warning("These are only tasks please send notification")
                                    tasktag = "task:" + decisionname + ":" + st + ":" + wfidtag
                                    completeFlag = check_alltasks_complete(tasktag, body, BASE_URL, headers1)
                                    if completeFlag:
                                        tag = "TOP:WFID_" + str(wfid)
                                        result = json.loads(CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'], headers1))
                                        for f_name in result['data']['elements']:
                                            if "Application" in f_name['title']:
                                                data = json.loads(f_name['content'])
                                                for e1 in data['Elements'][0]['Elements']:
                                                    if "Applicant Name" in e1['FieldLabel']:
                                                        workFlow_Name = e1['Value']

                                        filename = filepath + decisionname + ".csv"
                                        filename_server = filepath_server + decisionname + ".csv"
                                        val1 = {}
                                        try:
                                            val1 = WP.parse_wfe(filename)
                                        except:
                                            val1 = WP.parse_wfe(filename_server)

                                        grpname = st + "mgr_" + str(wfid)
                                        b = {}
                                        b['title'] = workFlow_Name + " : " + val1['desc'] + "is awaiting your approval"
                                        b['msg'] = workFlow_Name + " : " + val1['desc'] + "is awaiting your approval, please complete the exit checklist."
                                        b['commtype'] = ["NOTIFY"]
                                        b['groupname'] = [grpname]
                                        # b['CardID'] = t_cardID
                                        method = "POST"
                                        url = BASE_URL + "usergroups/message/" + body['BusinessTag']
                                        resp = CM.hit_url_method(b, headers1, method, url)
                                        logging.warning("This Notificatiob befor exit complets")
                                        logging.warning(resp)

                                    else:logging.warning("Stages are not complete")



                            else:
                                tasktag = "task:" + decisionname + ":" + st + ":" + wfidtag
                                completeFlag = check_alltasks_complete(tasktag, body, BASE_URL, headers1)
                                if completeFlag:
                                    set_wfe_status(decisionname + ":" + wfidtag, "Completed", body, BASE_URL, headers1)
                                    # complete_wfe((decisionname + ":" + wfidtag), wfid, BASE_URL, body, headers1)  # as per sujoy instruction

                            if "Exit Checklist" in formname:
                                logging.warning("HERE we found EXIT Checklist")
                                tagName1 = decisionname + ":WFID_" + wfid
                                set_wfe_status(tagName1, "Completed", body, BASE_URL, headers1)
                                # complete_wfe(tagName1, wfid, BASE_URL, body, headers1)    # as per sujoy instruction

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

