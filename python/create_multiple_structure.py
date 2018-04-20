import base64
import time
import urllib2
from urllib2 import URLError
from urllib2 import HTTPError
import requests
import urllib
import json
import time
import os
import re
import sys
import csv
import StringIO
import itertools
import hashlib \

# import lib.login1 as LL
import logon as LL
import common as CM
import structure_builder_vka as struct


if __name__ == '__main__':
    # sys.('utf8')

    infile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/MINAL_test_struct.csv"

    email = 'admin@zestl.com'
    pwd = 'Zspladmin99'
    SERVER = "https://www.twig.me/"
    version = "v5/"
    BASE_URL = SERVER + version

    zbotFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/Golds_Gym_spare_users.csv"

    hasHeaders = True
    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)


    with open(zbotFile, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        if hasHeaders:
            row1 = data.next()
        for row in data:
            zbotID = row[0]
            try:
                struct.createStructure(infile, BASE_URL, headers1, zbotID)
            except:
                print " ****************************** "
                print "Something went wrong while creating + " + zbotID
                print " ****************************** "


    # zbotID = "FZJQSLZKA27T9" we are using test serer urllll. ok. i thought these tags were for test server. these are prod?
    ### do you think this will work? row[0] is header. minal?................  yes it will work . good. lets trywaittttt. you know what is wrong?
            ### was all this working? here it is saying error...........  it is working. i tried it on test server
    # i login
            ## tey arent doing anything with the server i hope

    # headers, headers1 = LL.req_headers()
