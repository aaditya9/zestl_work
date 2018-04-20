import common as CM
import logon as LL
import json
import logging
import requests
import wfe_parser as WP
import time
import csv
import datetime


SERVER = "http://twig-me.com/" #Dev
version = "v13/"
BASE_URL = SERVER + version
zviceID = "WHGJ7HTVTDFH3" # Future group
email = "admin@zestl.com"
pwd = "TwigMeNow"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)


# {"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"72675","FormSubmissionID":"73784","FormData":{"Supply Chain strategy":"Cycu"," Supply and Demand Planning Rational (how has the number been forecasted)":"Cjvj"},"tags":["TOP:WFID_451","wfe:DOSSIER_WFFE","DOCSEARCH::WFID_451"]}

# WARNING:root:{u'tags': [u'Execution_WFE1_5:WFID_18', u'Status', u'DOCSEARCH::WFID_18'], u'FormData': {u'Status': u'Completed'}, u'Cmd': u'form-submit', u'FormID': u'134', u'FormSubmissionID': u'2967', u'BusinessTag': u'AQSYFC5AQY7X8'}
# {"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"69659","FormSubmissionID":"73675","FormData":{"Volume Forecasting Done?":"false"," Volume Forecast Plan":null},"tags":["COE_WFE1_4:WFID_451","VOLUME FORECASTING FORM","DOCSEARCH::WFID_451"]}


# inp = {"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"69552","FormSubmissionID":"74372","FormData":{"Design Route Study done":"false"," Design Route File":"[{\"media_name\":\"temporary_holder.jpg\",\"media_ext\":\"jpg\",\"media_size\":194047,\"media_type\":\"image\\\/jpeg\",\"media\":\"https:\\\/\\\/s3-ap-south-1.amazonaws.com\\\/dev-zestl-4\\\/TM_S3_TEMP_FILES_209521151.jpg\",\"media_compressed\":true}]"},"tags":["MKT_WFE1_1:WFID_453","DESIGN ROUTE FINALIZATION FORM","DOCSEARCH::WFID_453"]}
# {\"media_name\":\"temporary_holder.jpg\",\"media_ext\":\"jpg\",\"media_size\":194047,\"media_type\":\"image\\\/jpeg\",\"media\":\"https:\\\/\\\/s3-ap-south-1.amazonaws.com\\\/dev-zestl-4\\\/TM_S3_TEMP_FILES_209521151.jpg\",\"media_compressed\":true}
# body = json.loads(inp)
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"69552","FormSubmissionID":"74372","FormData":{"Design Route Study done":"false"," Design Route File":"[{\"media_name\":\"temporary_holder.jpg\",\"media_ext\":\"jpg\",\"media_size\":194047,\"media_type\":\"image\\\/jpeg\",\"media\":\"https:\\\/\\\/s3-ap-south-1.amazonaws.com\\\/dev-zestl-4\\\/TM_S3_TEMP_FILES_209521151.jpg\",\"media_compressed\":true}]"},"tags":["MKT_WFE1_1:WFID_453","DESIGN ROUTE FINALIZATION FORM","DOCSEARCH::WFID_453"]}')
abc = body['FormData'][' Design Route File']
print abc

tom = json.loads(abc)
print tom

for eee in tom:
    jerry = eee['media_name']
    jerry_1 = eee['media']
    jerry_2 = eee['media_size']
    print jerry
    print jerry_1
    print jerry_2
    # print eee
# cardID = 73784
body = {}
method = "POST"
url = BASE_URL + "cards/" + str(cardID) + "/attachment/s3/" + zviceID
body['S3URL'] = "https://s3-ap-south-1.amazonaws.com/dev-zestl-4/TM_S3_TEMP_FILES_209521151.jpg"
body['fileName'] = "temporary_holder.jpg"
body['fileSize'] = 194047
jasub = CM.hit_url_method(body, headers1, method, url)
# print jasub