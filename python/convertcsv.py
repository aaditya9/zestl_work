
import json
import sys
import logging
import re
import csv
import common as CM
import pandas as PD
import xlrd

#
# filename = '/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/Workflow_Specs_Template1.csv'
# filename = '/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/Workflow_Specs_MKT.csv'
# pathxls = '/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/'
pathxls = 'C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/DEC_6_DEV_FG/'
# pathxls = 'C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/Test_Server_workflow/farmfresh/'
# pathxls = 'C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/future_retail/'
# pathxls = 'C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/'
# filenamecsv = '/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/Workflow_Specs_MKTxls.csv'
# csvfileList = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/wfe_list.csv"
# csvfileList = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/all_wfes/wfe_list.csv"
# csvfileList = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/DEC_6_DEV_FG/wfe_list.csv"
csvfileList = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/Test_Server_workflow/Haldiram/wfe_list_1.csv"
# csvfileList = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/future_retail/wfe_list.csv"


inpufiles = ["Workflow_Specs_MKT", "Workflow_Specs_NPD", "Workflow_Specs_COM","Workflow_Specs_COE","Workflow_Specs_PKG"]
# inpufiles = ["Commercial_workflow","CPC_workflow","Design_workflow","Execution_workflow","Property_workflow"]
# inpufiles = ["Workflow_Specs_MKT"]

with open(csvfileList, "w") as cfile:

    for fn in inpufiles:
        filenamexls = pathxls + fn + ".xlsx"
        filename = pathxls + fn + "xls.csv"
        # filename = pathxls + "Workflow_Specs_NPD_2.csv"

        wfes = []

        data_xls = PD.read_excel(filenamexls, 'Main', index_col=None, skiprows=3)
        # data_xls = data_xls[3:]
        data_xls.to_csv(filename, encoding='utf-8', index=False)
        # filename = filenamecsv
        # filename = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/Workflow_Lab.csv"
        # filename = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/farmfresh_Workflow_Specs.csv"
        # filename = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/PROD_Gene_Path/Masters.csv"
        filename = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/PROD_Gene_Path/12_march_new_Test_selectionForm/LAB_wfes.csv"
        # filename = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/Test_Server_workflow/Services Demo/WFServicesDemo.csv"

        with open(filename, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            # data = csv.reader(rf)
            wfe = {}
            for row in data:
                wfe = {}
                # wfe['subflow'] = ""
                # wfe['id'] = ""
                # wfe['desc'] = ""
                # wfe['entry'] = ""
                # wfe['forms'] = ""
                # wfe['exit'] = ""
                # wfe['comm'] = ""
                # wfe['skip'] = ""
                # wfe['status'] = ""
                # wfe['prev'] = ""
                # wfe['next'] = ""
                if row[0] is not "" or row[0] != "Dept" or row[0] != 'MKT\nPKG\nLGL\nPKG\nMFG\nCOE\nCOM\nOPS':
                    wfe['subflow'] = CM.force_decode(row[0])
                    wfe['id'] = CM.force_decode(row[1])
                    wfe['desc'] = CM.force_decode(row[2])
                    if "Unnamed" in row[3]:
                        wfe['entry'] = ""
                    else:
                        wfe['entry'] = CM.force_decode(row[3])

                    wfe['forms'] = CM.force_decode(row[4])
                    wfe['exit'] = CM.force_decode(row[5])
                    if "Unnamed" in row[5]:
                        wfe['exit'] = ""
                    else:
                        wfe['exit'] = CM.force_decode(row[5])

                    if "Unnamed" in row[6]:
                        wfe['comm'] = ""
                    else:
                        wfe['comm'] = CM.force_decode(row[6])

                    wfe['skip'] = CM.force_decode(row[7])
                    wfe['status'] = CM.force_decode(row[8])
                    wfe['prev'] = CM.force_decode(row[9])
                    wfe['next'] = CM.force_decode(row[10])
                    wfes.append(wfe)


        for wfe in wfes:
            # filename = 'C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/DEC6_WFES/' + wfe['id'] + ".csv"
            # filename = 'C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/future_retail/all_files/' + wfe['id'] + ".csv"
             # filename = 'C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/' + wfe['id'] + ".csv"
            # filename = 'C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/PROD_Gene_Path/' + wfe['id'] + ".csv"
            filename = 'C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/PROD_Gene_Path/12_march_new_Test_selectionForm/wfe/' + wfe['id'] + ".csv"
            cfile.write(wfe['id'] + ".csv\n")
            with open(filename, 'w') as wf:
                wf.write("WFE,,comments\n")
                wf.write("Name," + wfe['id'] + "," + wfe['desc'] + ",\n")
                wf.write("Sub Workflow," + wfe['subflow'] + ",\n")
                wf.write("Communication pref," + wfe['comm'] + ",\n")
                wf.write("Skip," + wfe['skip'] + ",\n")
                wf.write("Status," + wfe['status'] + ",\n")
                wf.write("Next WFE," + wfe['next'] + ",\n")
                wf.write("previous WFE," + wfe['prev'] + ",\n")
                try:
                    flag = wfe['entry']
                    if flag is not "":
                        formrows = flag.split("\n")
                        wf.write("Entry Checklist form start,,\n")
                        for line in formrows:
                            line = CM.force_decode(line)
                            if re.match(r"TASK:.*", line, re.IGNORECASE):
                                wf.write(line.strip() + ",,\n")
                            elif re.match(r"ADMIN:.*", line, re.IGNORECASE):
                                linesplit = line.split(":")
                                wf.write("Admin only," + linesplit[1] + ",\n")
                        wf.write("Entry Checklist form end,,\n")
                except:
                    flag = ""
                try:
                    flag = wfe['exit']
                    if flag is not "":
                        formrows = flag.split("\n")
                        wf.write("Exit Checklist form start,,\n")
                        for line in formrows:
                            line = CM.force_decode(line)
                            if re.match(r"TASK:.*", line, re.IGNORECASE):
                                wf.write(line.strip() + ",,\n")
                            elif re.match(r"ADMIN:.*", line, re.IGNORECASE):
                                linesplit = line.split(":")
                                wf.write("Admin only," + linesplit[1] + ",\n")
                        wf.write("Exit Checklist form end,,\n")
                except:
                    flag = ""
                try:
                    flag = wfe['forms']
                    if flag is not "":
                        formrows = flag.split("\n")
                        for line in formrows:
                            line = CM.force_decode(line)
                            if re.match(r"(.*) start", line, re.IGNORECASE ):
                                formname = re.match(r"(.*) form start", line, re.IGNORECASE )
                                wf.write(formname.group(1) + " form start,,\n")
                            elif re.match(r"TASK:.*", line, re.IGNORECASE ):
                                wf.write(line.strip() + ",,\n")
                            elif re.match(r"ADMIN:.*", line, re.IGNORECASE ):
                                linesplit = line.split(":")
                                wf.write("Admin only," + linesplit[1] + ",\n")
                            if re.match(r"(.*) end", line, re.IGNORECASE):
                                formname = re.match(r"(.*) form end", line, re.IGNORECASE)
                                wf.write(formname.group(1) + " form end,,\n")
                except:
                    flag = ""
                wf.write("WFE end,,\n")

            with open(filename, 'a') as wf:
                wf.write(",,\n")
                wf.write("Forms body,,\n")
                try:
                    flag = wfe['entry']
                    if flag is not "":
                        formrows = flag.split("\n")
                        wf.write("Entry Checklist form body start,,\n")
                        for line in formrows:
                            line = CM.force_decode(line)
                            line = line.strip()
                            if re.match(r"TASK:.*", line, re.IGNORECASE):
                                flag1 = 1
                            elif re.match(r"ADMIN:.*", line, re.IGNORECASE):
                                flag1 = 1
                            else:
                                linesplit = line.split(":::")
                                if linesplit[0] == '':
                                    logging.info("who likes unicodes")
                                else:
                                    try:
                                        default = linesplit[1]
                                    except:
                                        default = ""
                                    wf.write(linesplit[0].strip() + "," + default.strip() + ",\n")
                        wf.write("Entry Checklist form body end,,\n")
                except:
                    logging.warn("no entry form defined")
                try:
                    flag = wfe['exit']
                    if flag is not "":
                        formrows = flag.split("\n")
                        wf.write("Exit Checklist form body start,,\n")
                        for line in formrows:
                            line = line.strip()
                            if re.match(r"TASK:.*", line, re.IGNORECASE):
                                flag1 = 1
                            elif re.match(r"ADMIN:.*", line, re.IGNORECASE):
                                flag1 = 1
                            else:
                                linesplit = line.split(":::")
                                if linesplit[0] == '':
                                    logging.info("who likes unicodes")
                                else:
                                    try:
                                        default = linesplit[1]
                                    except:
                                        default = ""
                                    wf.write(linesplit[0].strip() + "," + default.strip() + ",\n")
                        wf.write("Exit Checklist form body end,,\n")
                except:
                    logging.warn("no exit form defined")
                try:
                    flag = wfe['forms']
                    if flag is not "":
                        formrows = flag.split("\n")
                        for line in formrows:
                            line = line.strip()
                            if re.match(r"(.*) start", line, re.IGNORECASE):
                                formname = re.match(r"(.*) form start", line, re.IGNORECASE)
                                wf.write(formname.group(1) + " form body start,,\n")
                            elif re.match(r"TASK:.*", line, re.IGNORECASE):
                                flag1 = 1
                            elif re.match(r"ADMIN:.*", line, re.IGNORECASE):
                                flag1 = 1
                            elif re.match(r"(.*) end", line, re.IGNORECASE):
                                formname = re.match(r"(.*) form end", line, re.IGNORECASE)
                                wf.write(formname.group(1) + " form body end,,\n")
                            else:
                                linesplit = line.split(":::")
                                if linesplit[0] == '':
                                    logging.info("who likes unicodes")
                                else:
                                    try:
                                        default = linesplit[1]
                                    except:
                                        default = ""
                                    wf.write(linesplit[0].strip() + "," + default.strip() + ",\n")
                except:
                    flag = ""
                wf.write("Forms body end,,\n")