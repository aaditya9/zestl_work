
import common as CM
import json
import logging
import re
import csv
import datetime
import workFLOW_functions as WF
import settings as s

def user_addition_using_Form(body, BASE_URL, headers1):

    name = body['FormData'][s.field_dict['name']]
    email_ID = body['FormData'][s.field_dict['email']]

    result = CM.add_user_InBusiness(body['BusinessTag'],name,email_ID, headers1, BASE_URL)
    jsonreply = json.loads(result)
    user_id = jsonreply['data']['usertagid']
    logging.warning("addition is done " + str(user_id))

    WF.hide_user_card(headers1, BASE_URL, user_id)
    if s.selfgroup == "true":
        result_3 = WF.create_self_grp_and_ADDuser(name, user_id,BASE_URL, headers1,body)
    if s.usexlsmap == "true":
        department = body['FormData'][s.field_dict['department']]
        role = body['FormData'][s.field_dict['role']]
        file_name = s.xlsmapfile
        result_4 = WF.add_user_in_GivenInExcel(file_name,department,role,user_id,headers1,BASE_URL,body)

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


def topformSubmit(body, workflowTopFormID, headers1, BASE_URL):


    logging.warning("@@@@@@@@@@@@@@@@@@@@@@@@@")
    logging.warning(datetime.datetime.now())
    logging.warning("@@@@@@@@@@@@@@@@@@@@@@@@@")


    input_data = body['FormData']
    formkey = "created1_" + body['FormData']['wid']
    tagNamesub = "WFID_" + body['FormData']['wid']
    wid = body['FormData']['wid']

    if body['FormData']['Project Title'] is None:
        logging.warning("Blank form submission")
    else:

        try:
            try:
                logging.warning("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
                logging.warning(body['FormData'])
                grpname = "TOPp_" + str(body['FormData']['wid'])
                logging.warning(grpname)

                lead = []
                coe_lead = body['FormData']['Brand Entrepreneur Lead']
                lead.append(coe_lead)
                npd_lead = body['FormData']['NPD Lead']
                lead.append(npd_lead)
                p_lead = body['FormData']['LGL Lead']
                lead.append(p_lead)
                mkt_lead = body['FormData']['MKT Lead']
                lead.append(mkt_lead)
                pkg_lead = body['FormData']['PKG Lead']
                lead.append(pkg_lead)
                com_lead = body['FormData']['COM Lead']
                lead.append(com_lead)
                p_lead = body['FormData']['MFG Lead']
                lead.append(p_lead)

                logging.warning(lead)



            except:
                logging.error("adding users to group fails")


            createdvalue = CM.get_formID_using_KEY_Value_API(BASE_URL, headers1, body['BusinessTag'], formkey)
            createdvalue = json.loads(createdvalue)
            createdvalue = createdvalue['data']['value']['_value']
            if createdvalue == "113":
                logging.warning("resubmit")
                #
                masterFileName = "WFE_subflow_NPD1.csv"
                WF.create_wfes(body, masterFileName, headers1, BASE_URL,filepath,filepath_server)
                # print "execution is done"
                #

                tag1 = "DOCSEARCH::" + tagNamesub
                result = json.loads(CM.get_all_tagIds(tag1, BASE_URL, body['BusinessTag'], headers1))
                cards = {}
                allresults = []
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
                method = "PUT"
                url = BASE_URL + "bulk/" + body['BusinessTag'] + "/formsubmissions/"
                try:
                    if "Active" in body['FormData']['Status']:
                        fieldsmeta = json.dumps({"HideEditAction": False})
                        b = {}
                        b['FormSubmissionID'] = cardsarray
                        b['MetaData'] = fieldsmeta
                        b['OverrideMetaData'] = False
                        resp = CM.hit_url_method(b, headers1, method, url)
                        logging.warning(resp)

                    else:
                        fieldsmeta = json.dumps({"HideEditAction": True})
                        b = {}
                        b['FormSubmissionID'] = cardsarray
                        b['MetaData'] = fieldsmeta
                        b['OverrideMetaData'] = False
                        resp = CM.hit_url_method(b, headers1, method, url)

                except:
                    fieldsmeta = json.dumps({"HideEditAction": True})

            else:
                CM.add_val_in_table(BASE_URL, headers1, formkey, 113, body['BusinessTag'],int(wid))
                master_dict = s.master_dict
                for k,v in master_dict.items():
                    if body['FormData'][s.Top_Projet_Type] == k:
                        masterFileName = v
                        logging.warning("creation is Start")
                        WF.create_wfes(body, masterFileName, headers1, BASE_URL, filepath, filepath_server)
                        logging.warning("creation is Ensd")
                    else:
                        logging.error("Project type not specified. Doing Nothing")
        except:
            CM.add_val_in_table(BASE_URL, headers1, formkey, 113, body['BusinessTag'],int(wid))
            master_dict = s.master_dict
            for k, v in master_dict.items():
                if body['FormData'][s.Top_Projet_Type] == k:
                    masterFileName = v
                    logging.warning("creation is Start")
                    WF.create_wfes(body, masterFileName, headers1, BASE_URL, filepath, filepath_server)
                    logging.warning("creation is End")
                else:
                    logging.error("Project type not specified. Doing Nothing")


                # ************    This Code is for sending MAIL  **********************************
            try:
                grpname = "TOPp_" + str(body['FormData']['wid'])
                g_ID = CM.find_out_grp_ID(grpname, headers1, body['BusinessTag'], BASE_URL)
                for person in lead:
                    if person == '':
                        logging.warning("empty field")
                    else:
                        logging.warning(person)
                        result = CM.add_user_to_group(g_ID, person, body['BusinessTag'], headers1, BASE_URL)
                        logging.warning(result)
            except:logging.warning("adding fail in leads to TOP grp")

            result_1 = WF.send_mail_notification("MAIL",body,grpname,BASE_URL,headers1)

            result_1 = WF.send_mail_notification("NOTIFY",body,grpname,BASE_URL,headers1)

        try:

            if mkt_lead == '':
                logging.warning("MKT is empty field")
            else:
                logging.warning("MKT lead present")
                m_gname = "MKTmgr_" + str(body['FormData']['wid'])
                g_id = CM.find_out_grp_ID(m_gname, headers1, body['BusinessTag'], BASE_URL)
                result = CM.add_user_to_group(g_id, mkt_lead, body['BusinessTag'], headers1, BASE_URL)
                logging.warning(result)

            if coe_lead == '':
                logging.warning("COE is empty field")
            else:
                logging.warning("COE lead present")
                m_gname = "COEmgr_" + str(body['FormData']['wid'])
                g_id = CM.find_out_grp_ID(m_gname, headers1, body['BusinessTag'], BASE_URL)
                result = CM.add_user_to_group(g_id, coe_lead, body['BusinessTag'], headers1, BASE_URL)
                logging.warning(result)

            if com_lead == '':
                logging.warning("COM is empty field")
            else:
                logging.warning("COM lead present")
                m_gname = "COMmgr_" + str(body['FormData']['wid'])
                g_id = CM.find_out_grp_ID(m_gname, headers1, body['BusinessTag'], BASE_URL)
                result = CM.add_user_to_group(g_id, com_lead, body['BusinessTag'], headers1, BASE_URL)
                logging.warning(result)

            if npd_lead == '':
                logging.warning("NPD is empty field")
            else:
                logging.warning("NPD lead present")
                m_gname = "NPDmgr_" + str(body['FormData']['wid'])
                g_id = CM.find_out_grp_ID(m_gname, headers1, body['BusinessTag'], BASE_URL)
                result = CM.add_user_to_group(g_id, npd_lead, body['BusinessTag'], headers1, BASE_URL)
                logging.warning(result)

            if pkg_lead == '':
                logging.warning("PKG is empty field")
            else:
                logging.warning("PKG lead present")
                m_gname = "PKGmgr_" + str(body['FormData']['wid'])
                g_id = CM.find_out_grp_ID(m_gname, headers1, body['BusinessTag'], BASE_URL)
                result = CM.add_user_to_group(g_id, pkg_lead, body['BusinessTag'], headers1, BASE_URL)
                logging.warning(result)

            grpname = "TOPp_" + str(body['FormData']['wid'])
            g_ID = CM.find_out_grp_ID(grpname, headers1, body['BusinessTag'], BASE_URL)
            for person in lead:
                if person == '':
                    logging.warning("empty field")
                else:
                    logging.warning(person)
                    result = CM.add_user_to_group(g_ID, person, body['BusinessTag'], headers1, BASE_URL)
                    logging.warning(result)
            group = ["SeniorManagement","StrategyOffice","HOD"]
            for inside_group in group:
                grp_in_grp_ID = CM.find_out_grp_ID(inside_group, headers1, body['BusinessTag'], BASE_URL)
                by = {'grpUserGroupID': str(grp_in_grp_ID)}
                result = CM.add_usergrps_grps(BASE_URL, json.dumps(by), headers1, body['BusinessTag'], g_ID)
                logging.warning("Adding group to group")
                logging.warning(result)


        except:
            logging.error("Add to groups failed")


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


    # filepath_server = s.filepath_server
    filepath_server = "/var/www/cgi-bin/workflow/wfes/"

    filepath = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/Test_Server_workflow/Product demo/"
    # filepath = s.filepath

    workflowTopFormID = s.workflowTopFormID     ## Top Project management form TEST SERVER form ID
    packagingform = s.packagingform

    usuallistFile = filepath + str(body['BusinessTag']) + s.usualForm
    usuallistFile_server = filepath_server + str(body['BusinessTag']) + s.usualForm

    global cardList

    cardList = WF.read_usual_file(usuallistFile,usuallistFile_server)

    if body['Cmd'] == "workflow-create":
        print json.dumps(WF.start_workflow(workflowTopFormID, body, BASE_URL, headers1))

    if body['Cmd'] == "form-submit":

        if body['FormID'] == packagingform:
            WF.packagingSubmit(body, BASE_URL, headers1, packagingform, filepath,filepath_server)

        elif body['FormID'] == workflowTopFormID:
            topformSubmit(body, workflowTopFormID, headers1, BASE_URL)


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
                    result = json.loads(CM.get_all_tagIds(tagName, BASE_URL, body['BusinessTag'], headers1))
                    for alltag in result['data']['elements']:
                        if "Task Assignment Form" in alltag['allTags'] and "Task Assignment Form" in formname:
                        #*********************** one line function for Task Assignment form  ******************************#
                            WF.task_assignment_form(alltag,body,tagName,st,wfid,formname,headers1,BASE_URL)

                        elif "Update estimated Time Form" in alltag['allTags'] and "Update estimated Time Form" in formname:
                            #**********************  New Code **********************************
                            KEY = "Estimated Time"
                            form_ID = cardList['Estimate']
                            WF.update_skip_estimated(alltag,body,KEY,form_ID,BASE_URL,headers1)

                        if "Skip workflow stages form" in alltag['allTags'] and "Skip workflow stages form" in formname:
                            #**************************** New code *****************************
                            KEY = "SKIP"
                            form_ID = cardList['Skip']
                            WF.updateEstimated_SkipWorkflow(alltag, body, KEY, form_ID, BASE_URL, headers1)

                elif "Status" in formname:
                    WF.Status_In_Formname(decisionname,body,st,wfidtag,tagName,cardList,BASE_URL,headers1,wfid,filepath,filepath_server)
                else:
                    try:
                #*********************  We are not putting thiscode on prod. so we are commenting this code  ***************************
                        # result_1 = WF.link_WFES(body,BASE_URL,headers1,formname,decisionname)
                #******************************************************************************************************************************************************************

                        checkreq, checkboxes = WF.check_CHECK_BOX_true(tagName,formname,BASE_URL,body,headers1)
                    except:
                        logging.warning("No checkboxes found")
                    try:
                        WF.check_Mandatory_checkBOX(checkboxes,checkreq,decisionname,wfidtag,formname,wfid,filepath,filepath_server,cardList,body,BASE_URL,headers1)
                    except:
                        logging.warning("Nothing to do in this form")
            except:
                logging.warning("Not a tagged form")
#****************** New Code ****************************************
    WF.click_workflow(body)
#**********************************************************
#************************* New Code *************************
    WF.click_textcard(body)
#**********************************************************