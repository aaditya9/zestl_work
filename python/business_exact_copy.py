import json
import csv
import logon as LL
import common as CM
import re
import requests



SERVER = "http://35.154.64.11/"  # test
# SERVER = "https://twig.me/" #Production
version = "v7/"
BASE_URL = SERVER + version


# zviceID = "2PNNBUMU6KFFM"    ####  Business ID
# zviceID = "3HF549KHNFQ3N"   #### shipad Test

email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
# jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

body = {}
method = "POST"
url = "http://35.154.64.11/v7/customers/copy/customer"
# url = "https://twig.me/v6/products/BQMVDWRGWH7TA/maxproducts/50"
body = {}
body['DisplayName'] = "Du"
body['ToCopyBusinessTagID'] = "CVEPKDHYA2FCS"
jasub = CM.hit_url_method(body, headers1, method, url)
print jasub
