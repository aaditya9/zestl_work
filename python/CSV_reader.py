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

import csv
import pprint

if __name__ == '__main__':

    filename = "./../../Millennium/MNS_AdminData_TwigMe_CSV.csv"
    with open (filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print row
            pprint.pprint(row)
    
