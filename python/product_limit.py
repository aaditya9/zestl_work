import requests

import logon as LL
import common as CM
import password as PP
SERVER = "http://35.154.64.119/"  # test
#SERVER = "https://twig.me/" #Production
version = "v13/"
BASE_URL = SERVER + version

#zviceID = "8LS8752NB6U5Y"
zviceID="63YXHNUGXDX5T"

email = "shripad@zestl.com"
# pwd = "TwigMeNow"
pwd = "Zestl123"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
# jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

#
# gallery

# body = {}
# method = "PUT"
# # url = "http://35.154.64.11/v6/products/876MD568TAUH2/maxproducts/15"
# url = "https://twig.me/v8/products/8LS8752NB6U5Y/maxproducts/30"
# jasub = CM.hit_url_method(body, headers1, method, url)
# print jasub

#body={}
#
# body['Title']="Gallery_FIRST"
# body['Description']="Gallery_one_description"
# body['flag']=True
#
# method="POST"
#
# url=BASE_URL + zviceID + "/gallery"
# jaction = CM.hit_url_method(body,headers1, method, url)
#
# print jaction


# text card
# body={}
# body['cardData'] = {"title": "my_text_card", "desc": "my_text_desc", "Flags": True}
# body['cardType'] = "TEXT"
# body['opType'] = 1
# body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
# method = "POST"
# url = BASE_URL + "zvice/interaction/" + zviceID
# jaction = CM.hit_url_method(body, headers1, method, url)
# print jaction

#formcard
#
# body={}
# r = requests.get("http://twig.me/v1/push/dectest/" + zviceID)
# tagnum = r.json()['decTagID']
# user_tag = r.json()['decTagID']
#
# body["FormID"]=""
# body['FormTitle"']="my_first_from"
# body['FormDescription']="my_form_desc"
# body['LinkType']="Form"
# body['ZviceID']=tagnum
# body["ZbotID"]= user_tag
# body["LinkID"]=""
#
# method = "POST"
# url = BASE_URL+ zviceID +"/forms"
# print url
# jaction = CM.hit_url_method(body, headers1, method, url)
# print jaction


########## forum ###########
#
# body = {}
# body['Text'] = "my_forum"
# body['Flags'] = True
# body['FlagsInside'] = False
# method = "POST"
#
# url = BASE_URL + "forum/" + zviceID
# jaction = CM.hit_url_method(body, headers1, method, url)
# print  jaction


##### attendence


# body={}
# body["Title"]="my_Attendence"
# body["Description"]="my_attendence_desc"
# body["ScanType"]="FAST"
#
# method="POST"
#
# url = BASE_URL + "fastscan/attendance/" +zviceID
#
# jaction = CM.hit_url_method(body, headers1, method, url)
# print jaction

## department
#
# body ={}
# body['title'] = "my_dpt"
# body['zviceinfo'] = "my_dpt_desc"
# body['zviceid'] =zviceID
#
# body['zvicetype'] = "ZTAG"
# body['zvicelink'] = "NEW"
# body['lat'] = "-"
# body['long'] = "-"
# body['zviceloc'] = "---"
#
# method="POST"
# url = BASE_URL + "fastscan/attendance/" +zviceID
#
# jaction = CM.hit_url_method(body, headers1, method, url)
# print jaction

#{"error":true,"message":"Required field(s) Title is missing or empty"}

# body={}
# body['Title'] = "my_product"
# body['Description'] = "my_desc"
# method = "POST"
# url = BASE_URL + "carousel/products/add/" + zviceID
# jaction = CM.hit_url_method(body, headers1, method, url)
# print jaction