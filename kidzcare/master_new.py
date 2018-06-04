import sys
import json
import logon as LL
import logging
import os
import traceback
import signal
from datetime import datetime
# import datetime
import csv
#import wfe_parser as WP
import urllib2
# import wfe_parser_pandas as WP
import common as CM
import password as PD


# sudo tailf /var/log/httpd/error_log
# sudo pip install "module name"
def debug(sig, frame):
    d={'_frame':frame}         # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)
    message = "Signal received : " + str(sig) + "\n"
    message += ''.join(traceback.format_stack(frame))
    logging.error(message)

def listen():
    signal.signal(signal.SIGTERM, debug)  # Register handler
    # signal.signal(signal.SIGKILL, debug)  # Register handler
    signal.signal(signal.SIGSEGV, debug)  # Register handler
    signal.signal(signal.SIGFPE, debug)  # Register handler
    signal.signal(signal.SIGABRT, debug)  # Register handler
    # signal.signal(signal.SIGBUS, debug)  # Register handler
    signal.signal(signal.SIGILL, debug)  # Register handler

try:
    inp = sys.argv[1]
except:
    # logging.error("json decode error")
    inp = '{"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"77390","FormSubmissionID":"92235","FormData":{"Project Title":"Web 001","Product Description":"New Web 001","Product Brief":"[{\"media_name\":\"httpd.conf\",\"media_size\":15531,\"media_type\":\"\",\"media\":\"https:\\\/\\\/s3-ap-south-1.amazonaws.com\\\/dev-zestl-4\\\/TM_S3_TEMP_FILES_httpd.conf\",\"media_compressed\":false}]","Launch Date":"2017-11-28"," Included In ABP":"No","ABP Launch Date":"2017-12-21","ABP Revenue (INR in Lakhs)":null,"Project Type":"New Pack","Product Category":"Nilgiris","Brand":null,"Project Priority":"FastTrack","Brand Entrepreneur Lead":"35W23AX5F4ECA","NPD Lead":"AFCAF85STGDED","PKG Lead":"CU65L54L9U5T6","COM Lead":"AFCAF85STGDED","MKT Lead":"AFCAF85STGDED","LGL Lead":"AFCAF85STGDED","MFG Lead":"AFCAF85STGDED","Status":"Ideation","wid":"589"},"SubmittedBy":null,"tags":["TOP:WFID_589","DOCSEARCH::WFID_589"]}'
    inp = '{"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"77861","FormSubmissionID":"90591","FormData":{"Commercial Feasibility Done?":"true","Comments":null},"SubmittedBy":null,"tags":["COE_WFE1_1:WFID_579","COMMERCIAL FEASIBILITY STUDY","DOCSEARCH::WFID_579"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}'
    inp = '{"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"63881","FormSubmissionID":93302,"FormData":{"User Name":null,"Department":"New Product Development","Role":"Manager","Email ID":null,"Mobile number":null,"Link User?":"false"},"SubmittedBy":"33PQMYD4N77DP","tags":[],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}'
 #   inp=  '{"Cmd":"form-submit","BusinessTag":"WH4ULS9BHSAKZ","FormID":"24204","FormTitle":"Doctor Master","FormSubmissionID":24207,"FormData":{"Doctors":"D6","Center":"Burlington,NC","Start Date":"2018-05-16","End Date":"2018-05-16","Start Time":"16:30:00","End Time":"17:00:00","Monday":"false","Tuesday":"false","Wednesday":"false","Thursday":"false","Friday":"false"},"SubmittedBy":"FX5283PU679LC","tags":[],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}'
pwd = os.path.dirname(__file__)
logfile = pwd + "/pythonlogs.log"
logging.basicConfig(filename=logfile)
logging.warning(inp)

# body = json.loads(inp)



#body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"9SEUR88JAVLN6","FormID":"7519","FormSubmissionID":"11433","FormData":{"Subflow Name":"Water234","Type":"Type A"},"SubmittedBy":null,"tags":["Electrical_NEW:WFID_69","Subflow Selector","DOCSEARCH::WFID_69"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body=json.loads(r'{"Cmd":"form-submit","BusinessTag":"WH4ULS9BHSAKZ","FormID":"24204","FormTitle":"Doctor Master","FormSubmissionID":24207,"FormData":{"Doctors":"D5s","Center":"Hope Mills,NC","Start Date":"2018-06-15","End Date":"2018-06-15","Start Time":"09:00:00","End Time":"18:00:00","Monday":"false","Tuesday":"false","Wednesday":"false","Thursday":"false","Friday":"false"},"SubmittedBy":"FX5283PU679LC","tags":[],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
impName = body['BusinessTag']

# "tags":["skip::COE_WFE1_2:WFID_639","Form F4","COE_WFE1_2:WFID_639","DOCSEARCH::WFID_639"]
# "tags":["WFE1_33:WFID_229","Skip","DOCSEARCH::WFID_229"]


start=datetime.now()
# logging.warning(start)

try:
    X = __import__(impName)
    # BASE_URL = "http://twig-me.com/v13/"  ### dev server
    BASE_URL = "http://35.154.64.119/v13/"  # test server
    # BASE_URL = "https://future.twig.me/v13/"
    # BASE_URL = "http://twig-me.com/lankesh/v13/"  ### dev server
    # BASE_URL = "http://13.126.76.186/v13/"
    # BASE_URL = "https://twig.me/v13/"   # prod
    email = "admin@zestl.com"
    # pwd = PD.pwd
    pwd = "TwigMeNow"
    # zviceID = "WHGJ7HTVTDFH3"       #future group dev
    # zviceID = "WKMUYXELA9LCC"   #Genepath DEV
    # zviceID = "A3S7NY7KCKLRC"   #service demo test server
    # zviceID = "F6BPR2VWXPWQJ"
    # zviceID = "9SEUR88JAVLN6"   # Haldiram
    # zviceID = "XAJVCAMQQQD4D"   # PROD genepath
    # zviceID = "57J947VG9CCSK"
    # zviceID = "83H6LVUBRXWZ5"# minal dev
    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

    logging.warning(impName)
    listen()

    # cardID = "283"
    # metaDATA = '{"Name" : "akshay"}'
    # result = CM.textCard_metadata(cardID,metaDATA,BASE_URL,zviceID,headers1)
    # print result
    # result = CM.get_textcard_metadata(cardID,BASE_URL,zviceID,headers1)
    # print result

    # tag = "TOP:WFID_52"
    # # combine_tag = "Status,DOCSEARCH::WFID_52"
    # # result = CM.combine_tag_gives_cardID(BASE_URL,zviceID, headers1,combine_tag)
    # # print result
    # combine_tag = "Skip,DOCSEARCH::WFID_52"
    # result = CM.combine_tag_gives_cardID(BASE_URL, zviceID, headers1, combine_tag)
    # # print result
    # elm_array = []
    # completeStatus = True
    # for ctg in json.loads(result)['data']['elements']:
    #     # sub_ID = ctg['CardID']
    #     arr = ctg['Tags']
    #     arr1 = arr.split(",")
    #     print arr1
    #     for elm in arr1:
    #         if "DOCSEARCH" in elm or "Skip" in elm or "skip" in elm or "Skip workflow stages form" in elm:
    #             logging.warning("ignore")
    #         else:
    #             elm_1 = elm
    #             print elm_1
    #             sub_ID = ctg['CardID']
    #
    #             result_1 = CM.get_form_submission(str(sub_ID),zviceID, BASE_URL, headers1)
    #             # print result_1
    #             for ele in json.loads(result_1)['data']['ondemand_action'][0]['inputs']:
    #                 if "CheckBox" in ele['widget']:
    #                     for prop in ele['properties']:
    #                         if prop['name'] == "default":
    #                             value = prop['value']
    #                             print value
    #                             if value == "true":
    #                                 print "ignore stage"
    #                             else:elm_array.append(elm_1)
    #                         else:elm_array.append(elm_1)
    #
    # print elm_array
    #
    #     #                 if value == "Completed":
    #     #                     continue
    #     #                 else:
    #     #                     completeStatus = False


    X.mainworkflow(body, headers1, BASE_URL)
except:
    logging.exception("Exception hit - quitting")
logging.warning(datetime.now()-start)