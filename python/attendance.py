import json
import logon as LL
import common as CM
import sys
import re



if __name__ == "__main__":
    BASE_URL = "https://twig.me/v7/"  ### dev server
    zviceID = "2HRKLHBPPYXSN"  # Work flow demo department
    # zviceID = "5AGURR84SUC2K"
    email = "sujoy@zestl.com"
    pwd = "zestl123"
    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

    jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
    # print jsondata
    jddict = {}
    for ele in jsondata['data']['elements']:
        if ele['title'] == "Inscan":
            jddict['Inscan'] = ele
        if ele['title'] == "Outscan":
            jddict['Outscan'] = ele
    # print jddict
    method = "POST"
    body = {}
    body['numdays'] = 7
    url = 'https://twig.me/v7/2HRKLHBPPYXSN/fastscan/attendance/1660' ##inscan


    url = 'https://twig.me/v7/2HRKLHBPPYXSN/fastscan/attendance/1661/report' ## outscan
    jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
    checkouts = {}
    for day in jsondata['data']['elements']:
        dt = re.search("(\d{4}-\d{2}-\d{2})", day['title'])
        lines = day['content'].split("\n")
        ppl = {}
        for line in lines:
            if "Check Out" in line:
                rname = str(line).split("|")
                ppl[rname[0].strip()] = rname[1].strip()
        checkouts[dt.group(0)] = ppl

    url = 'https://twig.me/v7/2HRKLHBPPYXSN/fastscan/attendance/1660/report'  ## inscan
    jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
    checkins = {}
    for day in jsondata['data']['elements']:
        dt = re.search("(\d{4}-\d{2}-\d{2})", day['title'])
        lines = day['content'].split("\n")
        ppl = {}
        for line in lines:
            if "Check In" in line:
                rname = str(line).split("|")
                ppl[rname[0].strip()] = rname[1].strip()
        checkins[dt.group(0)] = ppl

    people = {'Minal Thorat', 'Sachin Tanpure', 'Manasi Karanjkar', 'Sayali Deshpande', 'Akshay Jadhav', 'Pallavi Agarwal', 'Lankesh Zade', 'Nitin Mhaske', 'Pushkar Prasad', 'Shripad Gadam', 'Hardik Gandhi',  'Sujoy Chakravarty',  'Siddharth Munot'}
    filename = "/Users/sujoychakravarty/Desktop/scratchpad/attendance.csv"
    with open(filename, 'w') as wf:
        for date in checkins:
            wf.write(date)
            wf.write("\n")
            for person in people:
                wf.write(person)
                wf.write(" , ")
                try:
                    wf.write(checkins[date][person])
                except:
                    wf.write("0")
                wf.write(" , ")
                try:
                    wf.write(checkouts[date][person])
                except:
                    wf.write("0")
                wf.write("\n")
            wf.write("\n")
    print ""

