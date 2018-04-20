#
# import json
# import sys
# import logging
# import re
import csv
import common as CM
# import pandas as PD
# import xlrd
#

wfes=[]

with open("Haldiram_Mechanical(Updated).csv","r") as rf:
        data=csv.reader(rf, delimiter=',')
        wfe={}

        for row in data:
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
                        with open("sample.csv","w") as wf :
                            print (wfe['id'])
                            print ("Name,"+ wfe['id']+ "," +wfe['desc'])
                            wf.write("WFE,,comments\n")
                            wf.write("Name,"+ wfe['id']+ "," +wfe['desc'] + ",\n")
                            wf.write("Sub Workflow," + wfe['subflow'] + ",\n")
                            wf.write("Communication pref," + wfe['comm'] + ",\n")
                            wf.write("Skip," + wfe['skip'] + ",\n")
                            wf.write("Status," + wfe['status'] + ",\n")
                            wf.write("Next WFE," + wfe['next'] + ",\n")
                            wf.write("previous WFE," + wfe['prev'] + ",\n")









