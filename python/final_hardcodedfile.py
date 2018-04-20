import json
import sys
import logging
import re
import csv
import common as CM
# import pandas as PD
# import xlrd


def convert():
        wfes=[]
        filename = "/home/adi/Downloads/TwigMeScripts-master/newfire/WFE_Lead_Tender.xlsx - WorkFlow.csv"

        with open(filename, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            # data = csv.reader(rf)
            #wfe = {}
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
            filename = '/home/adi/Downloads/TwigMeScripts-master/newfire/' + wfe['id'] + ".csv"
            #cfile.write(wfe['id'] + ".csv\n")
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
                            if re.match(r"(.*) start", line, re.IGNORECASE):
                                formname = re.match(r"(.*) form start", line, re.IGNORECASE)
                                wf.write(formname.group(1) + " form start,,\n")
                            elif re.match(r"TASK:.*", line, re.IGNORECASE):
                                wf.write(line.strip() + ",,\n")
                            elif re.match(r"ADMIN:.*", line, re.IGNORECASE):
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



if __name__ == "__main__":
    convert()

