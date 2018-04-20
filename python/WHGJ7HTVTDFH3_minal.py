
import common as CM
import wfe_parser as WP
import logon as LL
import json
import sys
import logging
import re

import datetime
from datetime import timedelta
import threading

from time import sleep

from subprocess import Popen

# elif body['BusinessTag'] == "3QVRRWHHJX3D9" and body['Cmd'] == "form-submit":
# body['FormID'] == '16'

threadLock = threading.Lock()
threads = []

class usualThread(threading.Thread):
    def __init__(self, threadID, val1, ele, body, BASE_URL, headers1):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.body = body
        self.val1 = val1
        self.BASE_URL = BASE_URL
        self.headers1 = headers1
        self.ele = ele

    def run(self):
        logging.warning( "Starting " + str(self.threadID) + " " + str(self.ele))
        threadLock.acquire()
        create_usual_forms(self.val1, self.ele, self.body, self.BASE_URL, self.headers1)
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
        logging.warning( cardIDs)
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


def create_worflow_elements(wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1, threadID, threads):

    filename = filepath + wfe + ".csv"
    filename_server = filepath_server + wfe + ".csv"
    ###### one wfe only below :::
    val1 = {}
    try:
        val1 = WP.parse_wfe(filename)
    except:
        val1 = WP.parse_wfe(filename_server)

    result = CM.create_txt_card(val1['desc'], "", body['BusinessTag'], headers1, wfesparentID, BASE_URL, "false",
                                "true")
    CardIds = str(result)
    tagName = body['WorkflowID']
    # tagNameTop = wfe + ":WFID_" + str(tagName)
    newtag = val1['subFlow'] + ":WFID_" + str(tagName) + ", wfe:" + val1['name']
    # tagnames = tagNameTop + "," + "wfe:" + wfe
    result = CM.add_tags_future(CardIds, newtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
    CM.create_txt_card("dummy", "dummy", body['BusinessTag'], headers1, CardIds, BASE_URL, "true", "false")

    # tagName = body['WorkflowID']

    #### speed bedug comment
    threadID = threadID + 1000
    threads = []

    usualForms = ["Estimate", "Form F4", "Form F6", "Status Form F5"]
    # usualForms = ["Estimate", "Skip this workflow step", "Dependencies", "Status"]
    for ele in usualForms:
        threadID = threadID + 1
        threadname = "thread" + ele + val1['name']
        threadname = usualThread(threadID, val1, ele, body, BASE_URL, headers1)
        threadname.start()
        threads.append(threadname)


        # ************** WFE specibody['BusinessTag']fic forms  submission ******#
    for k, v in val1['forms'].items():
        try:
            grp_name = v['AdminsR']
        except:
            grp_name = "N"
        form_key = val1['name'] + ":" + k
        # form_key = "WFE:Ideation:Form 1"
        result = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'],
                                                   form_key)  # gettings key value pair
        result = json.loads(result)
        form_id = result['data']['value']['_value']

        if grp_name is not "N":
            grpname = grp_name
        else:
            grpname = val1['subFlow'] + str(body['WorkflowID'])
        result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_id,
                                                  val1['forms'][k]['fields'])  # submitting form
        s_id = str(result)
        logging.warning(s_id)

        tagName = body['WorkflowID']
        cardtag = val1['name'] + ":WFID_" + str(tagName) + "," + k
        tagName = val1['name'] + ":" + val1['subFlow'] + ":WFID_" + str(tagName) + "," + k
        taskTagname = "task:" + tagName
        CM.add_tags_future(s_id, cardtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
        result = CM.set_card_permissions(BASE_URL, grpname, form_id, body['BusinessTag'], "OPERATOR",
                                         headers1)
        logging.warning(result)# setting operator permission
        for task in v['taskList']:
            threadID = threadID + 10000
            threadname = "thread" + s_id + str(task)
            threadname = taskThread(threadID, s_id, val1, task, body, BASE_URL, headers1, taskTagname)
            threadname.start()
            threads.append(threadname)

    return threads

        # result = CM.create_user_group(BASE_URL,headers1,grpname,body['BusinessTag'])    # creating new user group



def create_and_tag_task(s_id, val1, task, body, BASE_URL, headers1, taskTagname):
    response = CM.create_task_for_workflow(BASE_URL, body['BusinessTag'], headers1, s_id, task, val1['subFlow'])
    logging.warning(taskTagname)
    if response['error'] == False:
        t_id = str(response['taskID'])
        #### add this task ID to the taskOfsubmissionID  on key,val table
        keyname = "tasksOf" + s_id
        wfekeyname = "tasksOf" + val1['name']
        try:
            writeVal = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], keyname)
            result = json.loads(writeVal)
            form_id = result['data']['value']['_value']
            writeVal = form_id + "," + t_id

            writeVal1 = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], wfekeyname)
            result1 = json.loads(writeVal1)
            form_id1 = result1['data']['value']['_value']
            writeVal1 = form_id1 + "," + t_id

            CM.add_val_in_table(BASE_URL, headers1, keyname, writeVal, body['BusinessTag'])
            CM.add_val_in_table(BASE_URL, headers1, wfekeyname, writeVal1, body['BusinessTag'])

        except:
            writeVal = t_id
            CM.add_val_in_table(BASE_URL, headers1, keyname, writeVal, body['BusinessTag'])
            writeVal = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], keyname)
            result = json.loads(writeVal)
            form_id = result['data']['value']['_value']
            logging.warning("The task ID written in table was " + form_id)

            writeVal1 = t_id
            CM.add_val_in_table(BASE_URL, headers1, wfekeyname, writeVal1, body['BusinessTag'])
            writeVal1 = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], wfekeyname)
            result1 = json.loads(writeVal1)
            form_id1 = result1['data']['value']['_value']
            logging.warning("The task ID written in table was " + form_id1)

        CM.add_tags(t_id, taskTagname, BASE_URL, body['BusinessTag'], headers1)

def create_user_grps(body, flow, BASE_URL, headers1, parentID):
    tagName = body['WorkflowID']
    tagNameTop = "WFID_" + str(tagName)
    grpname = flow + "p_" + str(tagName)
    try:
        CM.create_groups(grpname, headers1, body['BusinessTag'], BASE_URL)
    except:
        logging.error("could not create user group " + flow + str(body['WorkflowID']))
    result = CM.create_txt_card(flow, "", body['BusinessTag'], headers1, parentID, BASE_URL, "false", "true")
    CardIds = str(result)

    tagnames = tagNameTop + "," + "subflow:" + flow
    CM.add_tags_future(CardIds, tagnames, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
    CM.create_txt_card("dummy", "dummy", body['BusinessTag'], headers1, CardIds, BASE_URL, "true", "false")
    return CardIds

def create_usual_forms(val1, ele, body, BASE_URL, headers1):
    tagName1 = val1['name'] + ":WFID_" + str(body['WorkflowID']) + "," + ele
    form_key = ele
    try:
        result = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'],
                                                   form_key)  # gettings key value pair
        result = json.loads(result)
        form_id = result['data']['value']['_value']
    except:
        logging.error("such a form does not exist" + ele)

    if ele == "Estimate":
        try:
            fields = val1['estimates']
        except:
            fields = []
        # depTagname = "estimate::" + tagName1 ### enable this one for prod
        depTagname = "estimate::" + tagName1 + "," + tagName1
        result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_id, fields)
        CM.add_tags_future(str(result), depTagname, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

    if ele == "Form F4":
        fieldname = {}
        try:
            fieldname['SKIP'] = val1['Skip']
        except:
            fieldname['SKIP'] = "false"
        fields = fieldname
        result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_id, fields)
        CM.add_tags_future(str(result), tagName1, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

    if ele == "Status Form F5":
        fieldname = {}
        try:
            fieldname['Status'] = val1['status']
        except:
            fieldname['Status'] = "Select"
        fields = fieldname
        result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_id, fields)
        CM.add_tags_future(str(result), tagName1, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])

    if ele == "Form F6":
        try:
            fields = val1['dependencies']
        except:
            fields = []
        depTagname = "backend::" + tagName1
        result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_id, fields)
        CM.add_tags_future(str(result), depTagname, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])



def create_wfes(body, masterfileName, headers1, BASE_URL):
    threads = []

    body['WorkflowID'] = body['FormData']['wid']

    filepath = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/wfes/"
    filepath_server = "/var/www/cgi-bin/workflow/wfes/"
    masterFile = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/" + masterfileName
    masterFile_server = "/var/www/cgi-bin/workflow/" + masterfileName

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
        threadID = threadID + 10000

        threads = create_worflow_elements(wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1, threadID, threads)

        # threadname = "thread" + wfe
        # threadname = wfeThread(threadID, wfe, body, wfesparentID, filepath, filepath_server, BASE_URL, headers1)
        # threadname.start()
        # threads.append(threadname)

    for t in threads:
        t.join()


    for wfe in lisval['deptwfes']:
        topname = wfe + "_CONFIG"
        result = CM.create_txt_card(topname, "Configure the workflow here", body['BusinessTag'], headers1, wfesparentID,
                                    BASE_URL, "false", "true")
        CardIds = str(result)
        tagName = body['WorkflowID']
        tagNameTop = wfe + ":WFID_" + str(tagName)
        # tagNameTop = wfe + ":WFID:" + str(tagName)

        allowedusers = wfe + "mgr"

        CM.set_card_permissions(BASE_URL, allowedusers, CardIds, body['BusinessTag'], "OPERATOR", headers1)

        tagnames = tagNameTop + "," + "wfe:" + topname
        result = CM.add_tags_future(CardIds, tagnames, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
        CM.create_txt_card("dummy", "dummy", body['BusinessTag'], headers1, CardIds, BASE_URL, "true", "false")

        tag = ""
        for ele in lisval['wfes']:
            if wfe in ele:

                # newtag = "task:" + ele + ":WFID:" + str(body['WorkflowID'])
                newtag = "task:" + ele + ":" + wfe + ":WFID_" + str(body['WorkflowID'])
                if tag == "":
                    tag = newtag
                else:
                    tag = tag + "," + newtag
        result = json.loads(CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'], headers1))

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
            try:
                val1 = WP.parse_wfe(filename)
            except:
                val1 = WP.parse_wfe(filename_server)

            elem['label'] = val1['desc'] + " : " + deptTasks['title']
            elem['type'] = "AUTO_COMPLETE"
            elem['required'] = 0
            elem['placeholder'] = ""
            elem['editable'] = "true"
            elem['values'] = grp_ID
            elem['python'] = subid
            form_element.append(elem)

        form = "Task Assignment Form"
        cardID = CM.form_card(BASE_URL, headers1, form, body['BusinessTag'], parentID)
        CM.set_card_permissions(BASE_URL, "All Org Users", str(cardID), body['BusinessTag'], "ALLLOWED_USERS", headers1)
        # form = "Web Tasks"
        result = CM.create_form_elements(BASE_URL, headers1, body['BusinessTag'], cardID, form, form_element)
        fields = {}
        result1 = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, str(cardID), fields)
        newtag = topname + ":WFID_" + str(tagName) + "," + form
        resp = CM.add_tags(str(result1), newtag, BASE_URL, body['BusinessTag'], headers1)

        #####
        e_arr = []
        for ele in lisval['wfes']:
            elem = {}
            tag = "estimate::" + ele + ":WFID_" + str(body['WorkflowID'])
            if wfe in ele:
                filename = filepath + ele + ".csv"
                filename_server = filepath_server + ele + ".csv"
                ###### one wfe only below :::
                val1 = {}
                try:
                    val1 = WP.parse_wfe(filename)
                except:
                    val1 = WP.parse_wfe(filename_server)
                result = json.loads(CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'], headers1))
                for alltag in result['data']['elements']:
                    if "Estimate" in alltag['allTags']:
                        sid = str(alltag['cardID'])
                        elem['label'] = val1['desc'] + " : Estimated Time"
                        elem['type'] = "EDIT_TEXT"
                        elem['required'] = 0
                        elem['placeholder'] = ""
                        elem['editable'] = "true"
                        elem['python'] = sid
                        e_arr.append(elem)
        # print e_arr
        form = "Update estimated Time Form"
        cardID = CM.form_card(BASE_URL, headers1, form, body['BusinessTag'], parentID)
        CM.set_card_permissions(BASE_URL, "All Org Users", str(cardID), body['BusinessTag'], "ALLLOWED_USERS", headers1)
        # CM.set_card_permissions(BASE_URL, allowedusers, str(cardID), body['BusinessTag'], "OPERATOR", headers1)
        result = CM.create_form_elements(BASE_URL, headers1, body['BusinessTag'], cardID, form, e_arr)
        fields = {}
        result1 = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, str(cardID), fields)
        newtag = topname + ":WFID_" + str(tagName) + "," + form
        resp = CM.add_tags(str(result1), newtag, BASE_URL, body['BusinessTag'], headers1)


def mainworkflow(body, headers1, BASE_URL):

    workflowTopFormID = "7395"
    workflowdummyform = "7404"
    congratsCardID = "7402"
    packagingform = "15150"

    try:
        w_ID = body['FormData']['WorkflowID']
        w_ID = str(w_ID)
    except:
        w_ID = 0
#***************************  Testing STARTS  ***************************************#

    if body['Cmd'] == "form-submit" and body['FormID'] == packagingform:
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
                # masterFileName = "WFE_subflow_PKG1.csv"
                # create_wfes(body, masterFileName, headers1, BASE_URL)
            else:
                logging.error("something is wrong in the packaging form submission")

        except:
            CM.add_val_in_table(BASE_URL, headers1, formkey, 112, body['BusinessTag'])
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
                    CM.add_val_in_table(BASE_URL, headers1, formkey, 112, body['BusinessTag'])
                    result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1,
                                                              workflowdummyform, input_data)
            except:
                CM.add_val_in_table(BASE_URL, headers1, formkey, 112, body['BusinessTag'])
                result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, workflowdummyform,
                                                          input_data)

    if body['Cmd'] == "workflow-create":
        outdict = {}
        input_data = {"wid" : str(body['WorkflowID'])}
        result = CM.form_submission_using_NEW_API(BASE_URL,body['BusinessTag'],headers1,workflowTopFormID,input_data)   #form submission
        CardIds = str(result)
        tagName = "projform:::WFID_" + str(body['WorkflowID'])
        CM.add_tags(CardIds, tagName, BASE_URL, body['BusinessTag'], headers1)
        #submit a project config form with the correct workflowID
        tagArray = [tagName]
        outdict['tags'] = tagArray
        logging.warning(outdict)
        print json.dumps(outdict)
        ## open up the workflowTopFormID for submission


    if body['Cmd'] == "form-submit" and body['FormID'] == workflowTopFormID:
        input_data = body['FormData']
        formkey = "created_" + body['FormData']['wid']
        tagNamesub = "WFID_" + body['FormData']['wid']
        if body['FormData']['Project Title'] is None:
            logging.warning("Blank form submission")
        else:
            try:
                createdvalue = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1,  body['BusinessTag'],formkey)
                createdvalue = json.loads(createdvalue)
                createdvalue = createdvalue['data']['value']['_value']
                if createdvalue == "112":
                    logging.warning("resubmit")
                else:
                    CM.add_val_in_table(BASE_URL, headers1, formkey, 112, body['BusinessTag'])
                    result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, workflowdummyform, input_data)
                    CardIds = str(result)
                    tagNamesub = "TOP:WFID_" + body['FormData']['wid']
                    CM.add_tags_future(CardIds, tagNamesub, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
            except:
                CM.add_val_in_table(BASE_URL, headers1, formkey, 112, body['BusinessTag'])
                result = CM.form_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, workflowdummyform,input_data)
                CardIds = str(result)
                tagNamesub = "TOP:WFID_" + body['FormData']['wid']
                CM.add_tags_future(CardIds, tagNamesub, BASE_URL, body['BusinessTag'], headers1, body['FormData']['wid'])
#**********************************   Testing  END ****************************************#

    if body['Cmd'] == "form-submit":
        tags = CM.get_tags_by_cardID(body['FormSubmissionID'], BASE_URL, body['BusinessTag'], headers1 )
        try:
            tagsoncard = json.loads(tags)['data']['elements'][0]['allTags']
            if len(tagsoncard) < 1:
                try:
                    here = body['junk']
                except:
                    logging.warning("not a tagged card")
            for tag in tagsoncard:
                tags = tag.split(":")
                if len(tags) == 2:
                    tagName = tag
                    decisionname = tags[0]
                    wfid = re.search("WFID_(\d+)", tags[1])
                    wfid = wfid.group(1)
                if len(tags) == 1:
                    formname = tag
            # if "ABC" in decisionname:
            if "_CONFIG" in decisionname:
                logging.warning(decisionname)
                result = json.loads(CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1))

#**********************   Testing STARTS *********************************************#
                for alltag in result['data']['elements']:
                    if "Task Assignment Form" in alltag['allTags'] and "Task Assignment Form" in formname:
                        data = json.loads(alltag['content'])
                        elem = {}
                        for subelm in data['Elements'][0]['Elements']:
                            try:
                                g_ID = subelm['Value']
                                g_ID = json.loads(g_ID)
                                g_ID = g_ID['GroupIDs']
                                c_id = subelm['MetaData']['PYTHON']
                                elem[c_id] = g_ID
                            except:
                                logging.warning("no user grp assigned")
                        logging.warning(elem)
                        for k, v in elem.items():
                            for gid in v:
                                task_Id = int(k)
                                g_Id = gid
                                result = CM.edit_task_for_workflow(BASE_URL, body['BusinessTag'], headers1, task_Id, g_Id)
                    if "Update estimated Time Form" in alltag['allTags'] and "Update estimated Time Form" in formname:
                        data = json.loads(alltag['content'])
                        for subelm in data['Elements'][0]['Elements']:
                            s_id = subelm['MetaData']['PYTHON']
                            estimate_value = subelm['Value']
                            form_ID = 10
                            input_data = {"Estimated Time": estimate_value}
                            result = CM.EDIT_submission_using_NEW_API(BASE_URL, body['BusinessTag'], headers1, form_ID,
                                                                      input_data, s_id)
#*************************************   Testing ENDS *******************************************#




            else:
                try:
                    result = CM.get_form_submission(body['FormSubmissionID'], body['BusinessTag'], BASE_URL, headers1)
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
                            flag == True
                    if flag == False:

                        key = "tasksOf" + body['FormSubmissionID']
                        value = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'],key)
                        value = json.loads(value)
                        value = value['data']['value']['_value']
                        values = value.split(',')
                        url = BASE_URL + "tasks/edit/" + body['BusinessTag']
                        method = "POST"
                        rb = {}
                        rb['Status'] = "Completed"
                        for taskno in values:
                            rb['TaskID'] = taskno
                            response = json.loads(CM.hit_url_method(rb, headers1, method, url))
                        if "Exit Checklist" in formname:
                        # if "exit" in formname:
                            tagName1 = decisionname + ":WFID_" + wfid
                            depTagname = "backend::" + tagName1
                            cards = CM.get_all_tagIds(depTagname, BASE_URL, body['BusinessTag'], headers1)
                            try:
                                cards = json.loads(cards)
                                contents = cards['data']['elements'][0]['content']
                                contents = json.loads(contents)
                                for a in contents['Elements'][0]['Elements']:
                                    if "Next stage" in a['ElementID']:
                                        nextstage = a['Value']
                                        nextstages = nextstage.split(",")
                                        for stage in nextstages:
                                            # k = "tasksOf" + stage
                                            st = stage.split('_')
                                            st = st[0]
                                            tag = "task:" + stage + ":" + st + ":WFID_" + wfid
                                            value = CM.get_all_tagIds(tag, BASE_URL, body['BusinessTag'], headers1)
                                            # print value
                                            taskID_array = []
                                            for t_val in json.loads(value)['data']['elements']:
                                                t_id = t_val['taskID']
                                                taskID_array.append(t_id)
                                            # print taskID_array
                                            # value = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1,
                                            #                                           body['BusinessTag'], k)
                                            # tag = "task:" +val1['name'] + val1['subflow'] + :wfid_1
                                            # value = json.loads(value)
                                            # value = value['data']['value']['_value']
                                            # values = value.split(',')

                                            url = BASE_URL + "tasks/edit/" + body['BusinessTag']
                                            method = "POST"
                                            rb = {}
                                            rb['Status'] = "Active"
                                            now = datetime.datetime.now()
                                            startdate = datetime.datetime.utcnow()
                                            sd = startdate.strftime('%Y-%m-%d %H:%M:%S')
                                            rb['StartDate'] = sd
                                            for taskno in taskID_array:
                                                rb['TaskID'] = taskno
                                                response = json.loads(CM.hit_url_method(rb, headers1, method, url))
                                            ### these are the tasks that need to be 'activated and start date added

                            except:
                                logging.warning("no contents found")
                            print cards

                            ## update the estimate form to complete
                            ## find the next WFE
                            ## make all tasks in next WFE active and set their start date as today


                except:
                    logging.warning("Nothing to do in this form")
        except:
            logging.warning("Not a tagged form")


    if body['Cmd'] == "form-submit" and body['FormID'] == workflowdummyform:
        input_data = body['FormData']
        formkey = "created1_" + body['FormData']['wid']
        tagNamesub = "WFID_" + body['FormData']['wid']

        try:
            createdvalue = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], formkey)
            createdvalue = json.loads(createdvalue)
            createdvalue = createdvalue['data']['value']['_value']
            if createdvalue == "113":
                logging.warning("resubmit")

                ###below section is for debug only


                # if body['FormData']['Project Type?'] == "New Brand/Product" or body['FormData'][
                #     'Project Type?'] == "Product Variant":
                #     masterFileName = "WFE_subflow_NPD1.csv"
                #     # masterFileName = "WFE_subflow_try.csv"
                #     create_wfes(body, masterFileName, headers1, BASE_URL)

                ######################




            else:
                CM.add_val_in_table(BASE_URL, headers1, formkey, 113, body['BusinessTag'])
                if body['FormData']['Project Type?'] == "New Brand/Product" or body['FormData'][
                    'Project Type?'] == "Product Variant":
                    masterFileName = "WFE_subflow_NPD1.csv"
                    # masterFileName = "WFE_subflow_try.csv"
                    create_wfes(body, masterFileName, headers1, BASE_URL)
                elif body['FormData']['Project Type?'] == "New SKU/Pack":
                    masterFileName = "WFE_subflow_NPD2.csv"
                    create_wfes(body, masterFileName, headers1, BASE_URL)
                else:
                    logging.error("Project type not specified. Doing Nothing")
        except:
            CM.add_val_in_table(BASE_URL, headers1, formkey, 113, body['BusinessTag'])
            if body['FormData']['Project Type?'] == "New Brand/Product" or body['FormData'][
                'Project Type?'] == "Product Variant":
                masterFileName = "WFE_subflow_NPD1.csv"
                # masterFileName = "WFE_subflow_try.csv"
                create_wfes(body, masterFileName, headers1, BASE_URL)
            elif body['FormData']['Project Type?'] == "New SKU/Pack":
                masterFileName = "WFE_subflow_NPD2.csv"
                create_wfes(body, masterFileName, headers1, BASE_URL)
            else:
                logging.error("Project type not specified. Doing Nothing")


        # outdict = {}
        # tagNameTop = "WFID_" + str(body['WorkflowID'])
        # tagArray = [tagNameTop]
        # outdict['tags'] = tagArray
        # logging.warning(outdict)
        # print json.dumps(outdict)



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

