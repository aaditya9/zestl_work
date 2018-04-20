import sys
import json
import logon as LL
import logging
import os
import csv
import re

def parse_wfe_list(filename):
    subflowStart = False
    wfe_start = False
    deptWFEStart = False
    speWFEStart = False
    spewfes = []
    subflows = []
    wfes = []
    deptwfes =[]
    out = {}
    with open(filename, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        for row in data:
            if re.match("Sub Flows", row[0], re.IGNORECASE):
                subflowStart = True
                wfe_start = False
                deptWFEStart = False
                speWFEStart = False
            elif re.match("WFEs", row[0], re.IGNORECASE):
                subflowStart = False
                wfe_start = True
                deptWFEStart = False
                speWFEStart = False

            elif re.match("Dept WFEs", row[0], re.IGNORECASE):
                deptWFEStart = True
                subflowStart = False
                wfe_start = False
                speWFEStart = False

            elif re.match("Special WFEs", row[0], re.IGNORECASE):
                speWFEStart = True
                deptWFEStart = False
                subflowStart = False
                wfe_start = False
            elif subflowStart:
                subflows.append(row[0])
            elif wfe_start:
                wfes.append(row[0])
            elif deptWFEStart:
                deptwfes.append(row[0])
            elif speWFEStart:
                spewfes.append(row[0])


    out['subflows'] = subflows
    out['wfes'] = wfes
    out['deptwfes'] = deptwfes
    out['spewfes'] = spewfes
    out['error'] = False
    return out


def parse_wfe(filename):
    nameFound = False
    subFound = False
    entryStart = False
    exitStart = False
    formStart = False

    val = {}
    estimates = {}
    forms = {}
    formelems = {}
    formelems['fields'] = {}
    dependencies = {}

    val['error'] = False
    # logging.error("arrived here with filename " + filename)



    with open (filename, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        for row in data:
            if re.match("name", row[0], re.IGNORECASE):
                nameFound = True
                val['name'] = row[1]
                val['desc'] = row[2]
            if re.match("Sub Workflow", row[0], re.IGNORECASE):
                subFound = True
                val['subFlow'] = row[1]
            if re.match("Standard Time", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Standard Resource", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Standard Cost", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Estimated Time", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Estimated Resource", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Estimated Cost", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Actual Time", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Actual Resource", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Actual Cost", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]

            if re.match("Next WFE", row[0], re.IGNORECASE):
                dependencies["Next stage"] = row[1]

            if re.match("Previous WFE", row[0], re.IGNORECASE):
                dependencies["Previous stage"] = row[1]

            if re.match("Communication pref", row[0], re.IGNORECASE):
                val['Comm'] = row[1]
            if re.match("Skip", row[0], re.IGNORECASE):
                val['Skip'] = row[1]

            if re.match("status", row[0], re.IGNORECASE):
                val['status'] = row[1]

            if formStart:
                if re.match(r".* form end", row[0], re.IGNORECASE):
                    formelems['taskList'] = taskList
                    forms[formname] = formelems
                    formStart = False
                    formelems = {}
                    formelems['fields'] = {}
                elif re.match("task", row[0], re.IGNORECASE):
                    logging.debug("task found")
                    task = {}
                    try:
                        tsplits = row[0].split(":::")
                        tasksplit = re.match(r"TASK:(.*)", tsplits[0], re.IGNORECASE)
                        task['title'] = tasksplit.group(1)
                        task['duration'] = tsplits[1]
                        taskList.append(task)
                    except:
                        logging.error("Illegal task definition " + row[0])

                elif re.match("Admin Only", row[0], re.IGNORECASE):
                    formelems['AdminsR'] = row[1]
                else:
                    if row[0] is not "":
                        formelems['fields'][row[0]] = row[1]

            if re.match(r".* form start", row[0], re.IGNORECASE):
                m = re.match(r"(.*) form start", row[0], re.IGNORECASE)
                formname = m.group(1)
                formStart = True
                taskList = []
                formelems['AdminsR'] = "N"

            if re.match("WFE end", row[0], re.IGNORECASE):
                val['estimates'] = estimates
                val['forms'] = forms
                val['dependencies'] = dependencies
                return val

    # val['estimates'] = estimates
    # val['forms'] = forms
    val['error'] = True
    val['message'] = "No WFE end statement found"
    return val



def parse_wfe_ordered(filename, optional = None):
    nameFound = False
    subFound = False
    entryStart = False
    exitStart = False
    formStart = False

    val = {}
    estimates = {}
    forms = {}
    formelems = {}
    formelems['fields'] = {}
    dependencies = {}

    val['error'] = False
    val['Optinal_Tag'] = optional
    # logging.error("arrived here with filename " + filename)



    with open (filename, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        allforms = []
        for row in data:
            if re.match("name", row[0], re.IGNORECASE):
                nameFound = True
                # if optional == None:
                val['name'] = row[1]
                # else:
                #     elm = row[1].split("_")
                #     val['name'] = elm[0] + "_" + optional + "_" + elm[2] + "_" + elm[3]

                val['desc'] = row[2]
            if re.match("Sub Workflow", row[0], re.IGNORECASE):
                subFound = True
                if optional == None:
                    val['subFlow'] = row[1]
                else:
                    elm = row[1].split("_")
                    val['subFlow'] = elm[0] + "_" + optional

            if re.match("Standard Time", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Standard Resource", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Standard Cost", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Estimated Time", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Estimated Resource", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Estimated Cost", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Actual Time", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Actual Resource", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]
            if re.match("Actual Cost", row[0], re.IGNORECASE):
                estimates[row[0]] = row[1]

            if re.match("Next WFE", row[0], re.IGNORECASE):
                dependencies["Next stage"] = row[1]

            if re.match("Previous WFE", row[0], re.IGNORECASE):
                dependencies["Previous stage"] = row[1]

            if re.match("Communication pref", row[0], re.IGNORECASE):
                val['Comm'] = row[1]
            if re.match("Skip", row[0], re.IGNORECASE):
                val['Skip'] = row[1]

            if re.match("status", row[0], re.IGNORECASE):
                val['status'] = row[1]

            if formStart:
                if re.match(r".* form end", row[0], re.IGNORECASE):
                    formelems['taskList'] = taskList
                    forms = {}
                    forms[formname] = formelems
                    allforms.append(forms)
                    formStart = False
                    formelems = {}
                    formelems['fields'] = {}
                elif re.match("task", row[0], re.IGNORECASE):
                    logging.debug("task found")
                    task = {}
                    try:
                        tsplits = row[0].split(":::")
                        tasksplit = re.match(r"TASK:(.*)", tsplits[0], re.IGNORECASE)
                        task['title'] = tasksplit.group(1)
                        task['duration'] = tsplits[1]
                        taskList.append(task)
                    except:
                        logging.error("Illegal task definition " + row[0])

                elif re.match("Admin Only", row[0], re.IGNORECASE):
                    formelems['AdminsR'] = row[1]
                else:
                    if row[0] is not "":
                        formelems['fields'][row[0]] = row[1]

            if re.match(r".* form start", row[0], re.IGNORECASE):
                m = re.match(r"(.*) form start", row[0], re.IGNORECASE)
                formname = m.group(1)
                formStart = True
                taskList = []
                formelems['AdminsR'] = "N"

            if re.match("WFE end", row[0], re.IGNORECASE):
                val['estimates'] = estimates
                val['forms'] = allforms
                val['dependencies'] = dependencies
                return val

    # val['estimates'] = estimates
    # val['forms'] = forms
    val['error'] = True
    val['message'] = "No WFE end statement found"
    return val

def parse_formcreate(filename):

    with open (filename, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        forms = {}
        formsinform = {}
        indform = []
        formstart = False
        formend = True
        formsection = False
        error = False
        for row in data:
            if re.match("Forms body end", row[0], re.IGNORECASE):
                forms['error'] = False
                forms['forms'] = formsinform
                return forms
            if re.match("Forms body", row[0], re.IGNORECASE):
                formsection = True
            if formsection:
                if re.match(r"(.*) Form body end", row[0], re.IGNORECASE):
                    m = re.match(r"(.*) Form body end", row[0], re.IGNORECASE)
                    if formstart == False:
                        logging.error("Form end before form start defined for form " + m.group(1))
                        forms['error'] = True
                        return forms
                    else:
                        formend = True
                        formsinform[formname] = indform
                        indform = []
                        formstart = False
                elif re.match(r"(.*) Form body start", row[0], re.IGNORECASE):
                    if formstart:
                        logging.error("Form body not ended for " + formname)
                        forms['error'] = True
                        return forms
                    else:
                        m = re.match(r"(.*) Form body start", row[0], re.IGNORECASE)
                        formstart = True
                        formname = m.group(1)
                        formend = False
                    # indform = []
                elif formstart:
                    if row[0] is not "":
                        ele = row[0].split(":")
                        try:
                            line = {}
                            line['type'] = ele[0]
                            line['label'] = ele[3]
                            if re.match(r"M", ele[1], re.IGNORECASE):
                                line['required'] = 1
                                line['python'] = "Mandatory"
                            else:
                                line['required'] = 0
                                line['python'] = "Optional"
                            if re.match(r"I", ele[2], re.IGNORECASE):
                                line['editable'] = True
                            else:
                                line['editable'] = False
                            try:
                                line['values'] = ele[4]
                            except:
                                logging.info("No 4th element supplied")
                            line['placeholder'] = row[1]
                            indform.append(line)
                        except:
                            logging.error("illegal form structure")
                            forms['error'] = True
                            return forms


filename="/home/adi/Downloads/Mechanical_WFE1_1.csv"
val1=parse_formcreate(filename)
print val1
#
#
# logfile = "./parserlogs.log"
# logging.basicConfig(filename=logfile)
#
# #
# filename = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/Test_Server_workflow/New_Haldiram_27_FEB/wfe/Cable_WFE1_1.csv"
# val1 = {}
# val1 = parse_wfe_ordered(filename, optional="minal")
# print val1
# print val1['forms']
# abc = list(reversed(val1['forms']))
# print abc

# val1 = parse_wfe(filename)
# print val1
# val1 = parse_formcreate(filename)
#
# print "done"
