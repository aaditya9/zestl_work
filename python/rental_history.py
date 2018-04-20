
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
from fuzzywuzzy import fuzz
import hashlib\

import lib.login1 as LL



def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']



headers, headers1 = LL.req_headers(passkey)

zbotID = LL.ZbotID

url = LL.BASE_URL + "library/rental/" + zbotID + "/report"
method = POST

body = {"StartDate" : "2016-07-14" }
jsonreply = hit_url_method(body, headers1, method, url)

print jsonreply

