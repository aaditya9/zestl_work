import sys
import json
import logon as LL
import re
import logging
import os
import common as CM
import csv
import json
import pandas as PD





BASE_URL = "https://twig.me/v13/"  ### dev server
email = "admin@zestl.com"
pwd = "zsplADMIN999"
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
inputFile = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/python/TwigMeScripts/python/hopemills.csv"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
zviceID = "FWSMGL6USVKDW"
hasHeader = "Y"

#*******************************    Upload   Data*****************

# with open(inputFile, 'r') as rf:
#     data = csv.reader(rf, delimiter=',')
#     if hasHeader == "Y":
#         row1 = data.next()
#     counter = 0
#     for row in data:
#         counter += 1
#         print counter
#         body = {}
#         url = BASE_URL + "kidzcare/" + zviceID + "/content/upload"
#         method = "POST"
#         body['Content'] = CM.force_decode(row[0].strip())
#         body['Flag'] = CM.force_decode(row[1].strip())
#         b = []
#         b.append(body)
#         resp = CM.hit_url_method(b, headers1, method, url)
#         print resp
#***************************************************************

url = BASE_URL + "kidzcare/" + zviceID + "/reports/upload"
method = "POST"

# body = {}
# body['OrgZviceID'] = 3000012597
# body['CenterName'] = "YADKIN"
# # body['CenterName'] = "YADKIN"
# body['Date'] = "2017-11-10"
# topbody = []

monthdecode = {
    "January" : "01",
    "Januray" : "01",
    "February": "02",
    "Feburary": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "Jaune": "06",
    "July": "07",
    "August": "08",
    "Auguast": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12",
    "Marh" : "03"
}


pathxls = "/Users/sujoychakravarty/PycharmProjects/TwigMeScripts/inputs/KidzCare/"
pathxls = "/Users/sujoychakravarty/Downloads/131117Updated/"

# inpufiles = ["Workflow_Specs_MKT", "Workflow_Specs_NPD", "Workflow_Specs_COM","Workflow_Specs_COE","Workflow_Specs_PKG"]

inputfiles = ["011117_KidzCare_HopeMills_ProvidersData__copy.xlsx","011117_KidzCare_AllAmerica_ProvidersData_.xlsx","011117_KidzCare_Northside_ProvidersData_.xlsx","011117_KidzCare_Yadkin_ProvidersData_.xlsx","021117_KidzCare_Burlington_ProvidersData_.xlsx","021117_KidzCare_Franklin_ProvidersData_.xlsx","021117_KidzCare_Sanford_ProvidersData.xlsx","031117_KidzCare_CapeFare_ProvidersData_.xlsx","031117_KidzCare_Charlotte_ProvidersData_.xlsx","031117_KidzCare_Greensboro_ProvidersData_.xlsx","031117_KidzCare_Leland_ProvidersData_.xlsx","031117_KidzCare_Lillington_ProvidersData_.xlsx","031117_KidzCare_StPauls_ProvidersData_.xlsx","041117_KidzCare_CharlotteEastover_ProvidersData_.xlsx","041117_KidzCare_Dunn_ProvidersData_.xlsx","041117_KidzCare_FuquayVarina_ProvidersData_.xlsx","041117_KidzCare_Morrisville_ProvidersData_.xlsx","041117_KidzCare_OwenPark_ProvidersData_.xlsx","061117_KidzCare_Clayton_ProvidersData_.xlsx","061117_KidzCare_Hampstead_ProvidersData_.xlsx"]
inputfiles = ["021117_KidzCare_SpringLake_ProvidersData.xlsx","021117_KidzCare_Wilmington_ProvidersData.xlsx"]

# inputfiles = ["041117_KidzCare_FuquayVarina_ProvidersData_.xlsx","041117_KidzCare_Morrisville_ProvidersData_.xlsx","041117_KidzCare_OwenPark_ProvidersData_.xlsx","061117_KidzCare_Clayton_ProvidersData_.xlsx","061117_KidzCare_Hampstead_ProvidersData_.xlsx"]
# inputfiles = ["061117_KidzCare_Hampstead_ProvidersData.xlsx"]


for fn in inputfiles:
    filenamexls = pathxls + fn
    filename = pathxls + fn + ".csv"
    # filename = pathxls + "Workflow_Specs_NPD_2.csv"

    wfes = []

    data_xls = PD.read_excel(filenamexls, 'Sheet1', index_col=None)
    # data_xls = data_xls[3:]
    data_xls.to_csv(filename, encoding='utf-8', index=False)

for fn in inputfiles:
    inputFile = pathxls + fn + ".csv"
    with open(inputFile, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        if hasHeader == "Y":
            row1 = data.next()
            centre = row1[0]
            print centre
        counter = 0
        daydata = {}
        topbody = []
        for row in data:
            if "Month" in row[0]:
                month = row[1].strip()
                print month
            if "Providers" in row[0]:
                providers = []
                for i in range(1,len(row)):
                    if row[i] != "":
                        providers.append(row[i].strip())
                print providers
            if re.match(r'\d+', row[0]):
                m = re.match(r'\d+', row[0])
                day = m.group(0)
                TotalPatientSeen = 0

                for i in range(0, len(providers)):
                    providerdata = {}
                    j = i * 6 + 1
                    if re.search("FALSE", row[j+4], re.IGNORECASE):
                        abse = False
                    else:
                        abse = True
                    if re.search("FALSE", row[j+5], re.IGNORECASE):
                        half = False
                    else:
                        half = True
                    daydata[providers[i]] = {
                        "Hosp": row[j+3],
                        "Absent": abse,
                        "HalfDay": half,
                        "Onsite": {
                            "PatientsScheduled": row[j],
                            "PatientsSeen": row[j+1],
                            "Noshow": row[j+2]
                    }}
                    TotalPatientSeen = TotalPatientSeen + int(row[j+3]) + int(row[j+1])

                date = "2017-" + monthdecode[month] + "-" + str(day).zfill(2)
                body = {}

                body['OrgZviceID'] = "95YTMAVLYEE7D"
                body['CenterName'] = centre
                body['Date'] = date
                body['TotalPatientsSeen'] = TotalPatientSeen
                body['Doctors'] = json.dumps(daydata)
                topbody.append(body)
        print topbody



    #
    #     st = []
    #     final_array = []
    #         st.append((row[0],row[1]))
    #         final_array.append(row)
    #     dict = {}
    #     mylist = []
    #     unique = []
    #     for sub in st:
    #         dict.setdefault(sub[1],[]).append(sub[0])
    #         if sub[1] not in unique: unique.append(sub[1])
    #     mylist = [(dict[sub][0], sub) for sub in unique]
    #     # print mylist
    #     # rf.seek(0)
    #     for sub_1 in mylist:
    #         center =  sub_1[0]
    #         date =  sub_1[1]
    #         body = {}
    #         req = {}
    #         for row in final_array:
    #             body['OrgZviceID'] = 3000012597
    #             body['CenterName'] = center
    #             body['Date'] = date
    #             if row[0] == center and row[1] == date:
    #                 print "coming"
    #
    #
    #                 req[row[2]] = {
    #                                 "Hosp" : row[3] ,
    #                                 "Absent" : row[4] ,
    #                                 "HalfDay" : row[5] ,
    #                                 "Onsite" : {
    #                                     "PatientsScheduled" : row[6] ,
    #                                     "PatientsSeen" : row[7] ,
    #                                     "Noshow" : row[8]
    #                                 }}
    #
    # #
    #
    #                 body['Doctors'] = json.dumps(req)
    #         topbody = []
    #         topbody.append(body)
    #         print topbody
        resp = CM.hit_url_method(topbody, headers1, method, url)
        print resp
        print "Done" + fn
    #
