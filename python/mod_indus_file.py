import json
from fuzzywuzzy import fuzz

import csv

import logon as LL
import common as CM



def unpaginate(inp, elements):
    for element in inp:
        if element['cardtype'] == "nextcard":
            url = element['url']
            method = element['method']
            body = json.loads(element['content'])
            jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
            elements = unpaginate(jsondata['data']['elements'], elements)
        else:
            elements.append(element)
    return elements



SERVER = "https://twig.me/"

version = "v11/"

BASE_URL = SERVER + version


zviceID = "B969YSR37AT7G"

urlAdd = "genericcards/" + zviceID


email = "admin@zestl.com"
pwd = "zsplADMIN999"


method = "POST"


url = u'https://twig.me/v11/org/B969YSR37AT7G/user/search'

body = {"username":"","expired":"false", "pagesize" : 250 }


headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.hit_url_method(body, headers1, method, url)
jsondata = json.loads(jsondata)
elements = []
elements = unpaginate(jsondata['data']['elements'], elements)
allusers = {}
for ele in elements:
    try:
        allusers[ele['title']] = ele['tagId']
    except:
        print "bad field"

infile = "/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/millennium/script_inputs/31stAug.csv"
outfile = "/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/millennium/script_inputs/31stAug_updated.csv"

# with open(outfile, 'w') as wf:
#     for k, v in allusers.items():
#         wf.write(k + "," + v + "," + "\n")

otherfile = "/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/millennium/script_inputs/New_Names.csv"
CM.parse_files(infile)
CM.parse_files(otherfile)
with open(otherfile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    for row in data:
        count = 0
        for k,v in allusers.items():
            if fuzz.ratio(k, row[0]) > 85:
                # print row[0]
                count = count + 1
                # print k
        if count < 2:
            print row[0]
            print count


with open  (outfile, 'w') as wf:

    with open("./tmp.csv", 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        for row in data:
            printline = ""
            matched = False
            for i in range(0, len(row) - 1):
                printline = printline + "," + "\"" + row[i] + "\""
                if i == 3:
                    for k, v in allusers.items():
                        if (fuzz.ratio(row[3], k) > 95):
                            printline = printline + "," + v
                            matched = True
                    if matched:
                        print "match"
                    else:
                        printline = printline + "," + ""
            printline = printline + "\n"
            wf.write(printline)

