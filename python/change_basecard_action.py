
import base64
import time
import urllib2
from urllib2 import URLError
from urllib2 import HTTPError
import requests
import urllib
import json
# import time
import os
import re
import sys
import csv
import StringIO
import itertools
import copy
import logon as LL
import common as CM
import hashlib




# inputLoginFile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/login.csv"

# hasHeader = 'N'

# "https://twig.me/v4/usergroups/2HRKLHBPPYXSN"

# SERVER = "http://52.8.240.85/"
# SERVER = "https://twig.me/"
SERVER = "http://52.53.164.140/"
version = "v4/"
BASE_URL = SERVER + version

zviceID = "EMZK4CWXHF54V"
# urlAdd = "zvice/interaction/" + zviceID
urlAdd = "customize/actions/" + zviceID
# "https://twig.me/v4/2HRKLHBPPYXSN"
# "https://twig.me/v4/membership/user/23KBNM7BUFTYR"


email = "admin@zestl.com"
pwd = "TwigMeNow"
# pwd = "Zspladmin99"
body = {}
# body = {'groupName' : "EA Executive Assistant", 'groupDesc' : "" }
# method = "PUT"
# body = {"interactionID":"INTERACTION_TYPE_GET_CONFIG_CARDS"}

body = {"bc.com.sms" : False}
method = "POST"

url = BASE_URL + urlAdd

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.hit_url_method(body, headers1, method, url)

print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
print jsondata