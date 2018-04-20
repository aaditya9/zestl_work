
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
import hashlib\

#import lib.login1 as LL
import lib.login1 as LL
import common as CM



if __name__ == '__main__':

    BASE_URL = "https://twig.me/v7/"
    zbotID = "A4CJ2VHTTJS9Y"
    outfile = "utsrentals.csv"

    headers, headers1 = LL.req_headers()

    # body = {"bookname": "", "pagenum": 0, "pagesize": 3000,
    #         "interactionID": "LibraryInteraction_INTERACTION_TYPE_SEARCH_BOOKS"}
    body = {"bookname": "", "pagenum": 0, "pagesize": 3000,
            "interactionID": "LibraryInteraction_INTERACTION_TYPE_SEARCH_BOOKS"}

    method = "POST"
    url = BASE_URL + "zvice/interaction/" + zbotID
    jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
    books = []

    for element in jsondata['data']['elements']:
        if element['cardtype'] == "basecard":
            books.append(element['tagId'])
    with open(outfile, "w") as of:
        for book in books:
            url = BASE_URL + "zvice/detailscard/" + book
            body = {}
            jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
            if "The book is in library" in jsondata['data']['elements'][2]['subtitle']:
                print "library book"
            else:
                print jsondata['data']['elements'][2]['subtitle']
                date = re.search(r'(\d+\-\d+\-\d+)', jsondata['data']['elements'][2]['subtitle'])
                date = date.group(0)
                renter = re.search(r'The book is rented by (.*)', jsondata['data']['elements'][2]['content'])
                renter = renter.group(1)
                of.write(book + "," + "\"" + jsondata['subtitle'] + "\"" + "," + renter + "," + date + "\n")
                print book + "," + "\"" + jsondata['subtitle'] + "\"" + "," + renter + "," + date
            # print "stop"

    print "stop"
