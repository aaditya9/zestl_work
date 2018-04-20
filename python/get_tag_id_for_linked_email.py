#!/usr/local/bin/python

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
import hashlib\

import argparse
import lib.login_prod as LL

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-server', nargs=1, type=str, required=True, dest='server', help = 'Provide server url')
    parser.add_argument('-loginID', nargs=1, type=str, required=True, dest='loginID', help = 'Provide login email')
    parser.add_argument('-pwd', nargs=1, type=str, required=True, dest='pwd', help = 'Provide login pwd')
    args = parser.parse_args()

    URL = args.server[0]
    BASE_URL =str(URL + "/v1/")
    email = args.loginID[0]
    pwd = args.pwd[0]
    
    # login
    headers, headers1, userIdentity = LL.req_headers(BASE_URL, email, pwd)
    
    print userIdentity
    #tagID = userIdentity.strip(URL) right usage
    tagID = userIdentity.strip("http://www.twig.me/")
    print "server: ", URL, "\nemail: ", email, "\ntagID: ", tagID 
    
