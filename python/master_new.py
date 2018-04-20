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
import wfe_parser as WP
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
pwd = os.path.dirname(__file__)
logfile = pwd + "/pythonlogs.log"
logging.basicConfig(filename=logfile)
logging.warning(inp)

# body = json.loads(inp)



# body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"99490","FormSubmissionID":99492,"FormData":{"coe Lead":"{\"GroupIDs\":[\"2804\",\"2514\"]}","mkt lead ":"{\"GroupIDs\":[\"1064\",\"2632\"]}","pkg lead":"{\"GroupIDs\":[\"2632\"]}","npd lead":"{\"GroupIDs\":[\"2504\"]}"},"SubmittedBy":"33PQMYD4N77DP","tags":[],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"5322","FormSubmissionID":"6692","FormData":{"GPDx ID":null,"Patient Name (If Existing Patient)":"C6B3UFKTV27J9","Patient Name (If New Patient)":"Tom cat","Patient Email":null,"Patient Phone No":null,"Date of Birth":"2018-01-01","Age":null,"Sex":"Male","Priority":"3","Test Requested":" Achondroplasia common mutation study (FGFR3 G380R)","Patient Initiation Details":null,"Relatives Name (if secondary samples)":"","Staff Only: Create new patient entry":"false","wid":"100"},"SubmittedBy":null,"tags":["TOP:WFID_100","DOCSEARCH::WFID_100"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"5322","FormSubmissionID":"6692","FormData":{"GPDx ID":null,"Patient Name (If Existing Patient)":null,"Patient Name (If New Patient)":"GenePath 8 Feb","Patient Email":"Minal@zestl.con","Patient Phone No":"764335","Date of Birth":"2018-01-01","Age":null,"Sex":"Male","Priority":"3","Test Requested":" Achondroplasia common mutation study (FGFR3 G380R)","Patient Initiation Details":null,"Relatives Name (if secondary samples)":"","Staff Only: Create new patient entry":"true","wid":"100"},"SubmittedBy":null,"tags":["TOP:WFID_100","DOCSEARCH::WFID_100"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"5313","FormSubmissionID":"6973","FormData":{"Test Performed":"Y chromosome microdeletion"},"SubmittedBy":null,"tags":["TOP:WFID_103","Test Selection Form","DOCSEARCH::WFID_103"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"5322","FormSubmissionID":"7225","FormData":{"GPDx ID":"2","Patient Name (If Existing Patient)":"","Patient Name (If New Patient)":"Pallavi zestl","Patient Email":"Pallavi@zestl.com","Patient Phone No":"7038701663","Date of Birth":"1992-03-04","Age":"25","Sex":"Female","Priority":"1(Highest)","Test Requested":"Y chromosome microdeletion","Patient Initiation Details":null,"Relatives Name (if secondary samples)":"","Staff Only: Create new patient entry":"false","wid":"108"},"SubmittedBy":null,"tags":["TOP:WFID_108","DOCSEARCH::WFID_108"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"12","FormSubmissionID":"799","FormData":{"Resource Name":"{\"GroupIDs\":[\"4\"]}","Comments":null},"SubmittedBy":null,"tags":["SER_WFE1_1:WFID_22","Assign Resource","DOCSEARCH::WFID_22"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"12","FormSubmissionID":"915","FormData":{"Resource Name":"{\"GroupIDs\":[\"4\"]}","Comments":null},"SubmittedBy":null,"tags":["SER_WFE1_1:WFID_24","Technician","DOCSEARCH::WFID_24"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
# body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"5313","FormSubmissionID":"13082","FormData":{"Test Performed ":"Y chromosome microdeletion"},"SubmittedBy":null,"tags":["TOP:WFID_174","Test Selection Form","DOCSEARCH::WFID_174"],"url_params":[]}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"83H6LVUBRXWZ5","FormID":"268","FormSubmissionID":282,"FormData":{"File Name":"one"},"SubmittedBy":null,"tags":[],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
# body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"9SEUR88JAVLN6","FormID":"120","FormSubmissionID":"1187","FormData":{"Make Identified":"true","Comments":null},"SubmittedBy":null,"tags":["MEC_WFE1_1:WFID_6","Identifying Makes","DOCSEARCH::WFID_6"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"98","FormSubmissionID":"14912","FormData":{"Sample Prep -DNA Done":"true","Comments":"Sample Prep -DNA NOTES"},"SubmittedBy":null,"tags":["WFE1_2:WFID_198","SAMPLE PREP -DNA FORM","DOCSEARCH::WFID_198"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
# body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"9SEUR88JAVLN6","FormID":"120","FormSubmissionID":"3114","FormData":{"Make Identified":"true","Comments":null},"SubmittedBy":null,"tags":["MEC_WFE1_1:WFID_17","Identifying Makes","DOCSEARCH::WFID_17"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
# body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"XAJVCAMQQQD4D","FormID":"177","FormSubmissionID":"225","FormData":{"Test No.":"RPDSEQ391"},"SubmittedBy":null,"tags":["TOP_WFE:WFID_8","Test Selection","DOCSEARCH::WFID_8"],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"9SEUR88JAVLN6","FormID":"117","FormSubmissionID":"2694","FormData":{"Make Finalised?":"true","Comments":null},"SubmittedBy":null,"tags":["MEC_WFE1_1:WFID_14","Finalise Make","DOCSEARCH::WFID_14"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"9SEUR88JAVLN6","FormID":"132","FormSubmissionID":"2692","FormData":{"Status":"Completed"},"SubmittedBy":null,"tags":["MEC_WFE1_1:WFID_14","Status","DOCSEARCH::WFID_14"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"57J947VG9CCSK","FormID":"197","FormSubmissionID":"666","FormData":{"1 Crate":"Blue Small","1 Article":null,"1 Quantity":"10","2 Crate":null,"2 Article":null,"2 Quantity":null,"3 Crate":null,"3 Article":null,"3 Quantity":null,"4 Crate":null,"4 Article":null,"4 Quantity":null,"5 Crate":null,"5 Article":null,"5 Quantity":null},"SubmittedBy":null,"tags":["TRIP_WFE1_1:WFID_18","Indent Dispatch","DOCSEARCH::WFID_18"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"57J947VG9CCSK","FormID":"200","FormSubmissionID":"707","FormData":{"1 Crate":null,"1 Article":null,"1 Quantity":null,"2 Crate":null,"2 Article":null,"2 Quantity":null,"3 Crate":null,"3 Article":null,"3 Quantity":null,"4 Crate":null,"4 Article":null,"4 Quantity":null,"5 Crate":null,"5 Article":null,"5 Quantity":null,"Trip Complete":"true"},"SubmittedBy":null,"tags":["TRIP_WFE1_4:WFID_26","Reception at Store","DOCSEARCH::WFID_26"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"17","FormSubmissionID":"2308","FormData":{"Arrieved at Client Location on Time":"true","Comments":null},"SubmittedBy":null,"tags":["SER_WFE1_3:WFID_59","Check In","DOCSEARCH::WFID_59"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"18","FormSubmissionID":"2306","FormData":{"Customer Satisfied with the Service Provided?":"true","Product Consumed":"Office 365","Comments":"creat one more user","Replacement Parts":null},"SubmittedBy":null,"tags":["SER_WFE1_3:WFID_59","Check Out","DOCSEARCH::WFID_59"],"url_params":{"users":"{\"selected\":\"DWUL75YCZN4JS\"}"}}')
# body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"741","FormSubmissionID":"2327","FormData":{"Available Credit (In Minutes)":"500","Credit Consumed (In Minutes)":"240","Comments":null},"SubmittedBy":null,"tags":["TOP:WFID_59","wfe:TOP_WFE1","DOCSEARCH::WFID_59"],"url_params":{"users":"{\"selected\":\"DWUL75YCZN4JS\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"XAJVCAMQQQD4D","FormID":"1081","FormSubmissionID":3862,"FormData":{"Employee Name":"15 feb","Employee Email":"minal@zestl.com","Employee Phone 1":null,"Employee Phone 2":null,"Department":null,"Role":null},"SubmittedBy":"6NA569EEKU3TV","tags":[],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"15683","FormSubmissionID":"15684","FormData":{"Sample Accession":"true","Sample Prep -DNA":"false","PCR -PCR step 1":"false","PCR -PCR step 2":"false","Post Seq - SANGER - FA":"false","Data Analysis":"false","Reporting":"false","Review":"false","Release":"false"},"SubmittedBy":null,"tags":["LAB_CONFIG:WFID_207","Skip workflow stages form","DOCSEARCH::WFID_207"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"XAJVCAMQQQD4D","FormID":"4255","FormSubmissionID":6030,"FormData":{"Patient Name (If Existing Patient)":"","Patient Name (If New Patient)":"shinchan","Patient Email":null,"Patient Phone No":null,"Date of Birth":"2018-02-11","Age":null,"Sex":null,"Priority":null,"Test Requested":null,"Sales Lead":"","Patient Initiation Details":null,"Relatives Name (If secondary samples)":"","Staff Only - Create new patient entry":"true","wid":"71","Patient ID":null,"GPDx ID":null},"SubmittedBy":"6NA569EEKU3TV","tags":[],"url_params":[]}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"XAJVCAMQQQD4D","FormID":"4255","FormSubmissionID":"6031","FormData":{"Patient Name (If Existing Patient)":"","Patient Name (If New Patient)":"Shinchan","Patient Email":null,"Patient Phone No":null,"Date of Birth":"2018-02-01","Age":null,"Sex":null,"Priority":null,"Test Requested":null,"Sales Lead":"","Patient Initiation Details":null,"Relatives Name (If secondary samples)":"","Staff Only - Create new patient entry":"true","wid":"72","Patient ID":null,"GPDx ID":null},"SubmittedBy":null,"tags":["TOP:WFID_72","DOCSEARCH::WFID_72"],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')
# body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"XAJVCAMQQQD4D","FormID":"153","FormSubmissionID":"6066","FormData":{"Patient Name (If Existing Patient)":"","Patient Name (If New Patient)":"Shinchan","Patient Email":"minal@zestl.com","Patient Phone No":"9890662293","Date of Birth":"2018-02-01","Age":null,"Sex":"Male","Priority":"3","Test Requested":"Y chromosome microdeletion","Sales Lead":"","Patient Initiation Details":null,"Relatives Name (if secondary samples)":"","Staff Only - Create new patient entry":"true","wid":"74","Patient ID":null,"GPDx ID":"G000050"},"SubmittedBy":null,"tags":["TOP:WFID_74","DOCSEARCH::WFID_74"],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')
# body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"10","FormSubmissionID":"2423","FormData":{"Client Name":"BUVSL8DN7ASC6","Service Request For":"Cloud","Description":"ABC","Upload Image":"[{\"media_name\":\"new-piktochart_28032681 (1).png\",\"media_size\":733652,\"media_type\":\"image\\\/png\",\"media\":\"https:\\\/\\\/s3-ap-south-1.amazonaws.com\\\/test-zestl-4\\\/1519018513newpiktochart280326811.png\",\"media_compressed\":false}]","Prefered Date":"2018-02-20","Priority":"Normal","Status":"Active","Token Number":"Token No: 66","wid":"66"},"SubmittedBy":null,"tags":["TOP:WFID_66","DOCSEARCH::WFID_66"],"url_params":{"users":"{\"selected\":\"DWUL75YCZN4JS\"}"}}')
# body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"XAJVCAMQQQD4D","FormID":"6594","FormSubmissionID":"8504","FormData":{"Patient Name (If Existing Patient)":"5FSHG72ZBGCX5","Patient Name (If New Patient)":null,"Patient Email":"xyz@gmail.com","Patient Phone No":"9898565656","Date of Birth":"2018-02-06","Age":"5","Sex":"Female","Priority":"2","Test Requested":"4p16.3 microdeletion (Wolf-Hirschhorn syndrome)","Sales Lead":"2238HKWNN4J57","Patient Initiation Details":null,"Relatives Name (If secondary samples)":"","Staff Only - Create new patient entry":"false","wid":"97","GPDx ID":"G000071"},"SubmittedBy":null,"tags":["TOP:WFID_97","DOCSEARCH::WFID_97"],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')
# body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"16989","FormSubmissionID":"16990","FormData":{"Sample Accession":"false","Sample Prep -DNA":"false","PCR -PCR step 1":"false","PCR -PCR step 2":"true","Post Seq - SANGER - FA":"false","Data Analysis":"false","Reporting":"false","Review":"false","Release":"false"},"SubmittedBy":null,"tags":["LAB_CONFIG:WFID_228","Skip workflow stages form","DOCSEARCH::WFID_228"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"18","FormSubmissionID":"2616","FormData":{"Customer Satisfied with the Service Provided?":"true","Product Consumed":"Outlook 2013","Comments":null,"Replacement Parts":null},"SubmittedBy":null,"tags":["SER_WFE1_3:WFID_70","Check Out","DOCSEARCH::WFID_70"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"740","FormSubmissionID":2683,"FormData":{"Client Name":null,"Business Address":null,"Phone Number":null,"Email":null,"Service Plan":null,"Available Credits (In Minutes)":null,"Pricing for Remote Service":null,"Pricing for On-Premise Service":null,"User ID":null},"SubmittedBy":null,"tags":[],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"740","FormSubmissionID":2687,"FormData":{"Client Name":"Chin min lu","Business Address":null,"Phone Number":"7878787878","Email":"minal@zestl.com","Service Plan":"Plan 2","Available Credits (In Minutes)":"700","Pricing for Remote Service":null,"Pricing for On-Premise Service":null,"User ID":null},"SubmittedBy":null,"tags":[],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"10","FormSubmissionID":"2594","FormData":{"Client Name":"7HPWCS3ERDC7T","Service Request For":"Email","Description":"Email","Upload Image":"[{\"media_name\":\"new-piktochart_28032681 (1).png\",\"media_size\":733652,\"media_type\":\"image\\\/png\",\"media\":\"https:\\\/\\\/s3-ap-south-1.amazonaws.com\\\/test-zestl-4\\\/1519119259newpiktochart280326811.png\",\"media_compressed\":false}]","Prefered Date":"2018-02-21","Priority":"FastTrack ","Status":"Active","Token Number":"Token No: 70","wid":"70"},"SubmittedBy":null,"tags":["TOP:WFID_70","DOCSEARCH::WFID_70"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"10","FormSubmissionID":"2594","FormData":{"Client Name":"2R666UDZHVV3K","Service Request For":"Email","Description":"Email","Upload Image":"[{\"media_name\":\"new-piktochart_28032681 (1).png\",\"media_size\":733652,\"media_type\":\"image\\\/png\",\"media\":\"https:\\\/\\\/s3-ap-south-1.amazonaws.com\\\/test-zestl-4\\\/1519119259newpiktochart280326811.png\",\"media_compressed\":false}]","Prefered Date":"2018-02-21","Priority":"FastTrack ","Status":"Active","Token Number":"Token No: 70","wid":"70"},"SubmittedBy":null,"tags":["TOP:WFID_70","DOCSEARCH::WFID_70"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"82","FormSubmissionID":"17113","FormData":{"SKIP":"true"},"SubmittedBy":null,"tags":["WFE1_16:WFID_229","Skip","DOCSEARCH::WFID_229"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"136","FormSubmissionID":"17264","FormData":{"Post Seq - SANGER - FA Done":"true","Post Seq - SANGER - FA Quantitative Results":null," Post Seq - SANGER - FA Image File 1":null," Post Seq - SANGER - FA Image File 2":null," Post Seq - SANGER - FA Image File 3":null,"Comments":"Post Seq - SANGER - FA NOTES"},"SubmittedBy":null,"tags":["WFE1_21:WFID_230","Post Seq - SANGER - FA FORM","DOCSEARCH::WFID_230"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"17344","FormSubmissionID":17345,"FormData":{"Patient age":"3","Patient weight":"3","Patient Height":"3","Patient salary":"3"},"SubmittedBy":"543X3UQ4ALWVK","tags":[],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"XAJVCAMQQQD4D","FormID":"156","FormSubmissionID":"8515","FormData":{"Item Shipped":"true","Shipping Date":null,"Expected Delivery Date":null,"Shipping Details":null},"SubmittedBy":null,"tags":["TOP:WFID_97","Shipping","DOCSEARCH::WFID_97"],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"XAJVCAMQQQD4D","FormID":"177","FormSubmissionID":"8279","FormData":{"Test No.":"ONCQPC141"},"SubmittedBy":null,"tags":["TOP:WFID_95","Test Selection","DOCSEARCH::WFID_95"],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"XAJVCAMQQQD4D","FormID":"6594","FormSubmissionID":"9151","FormData":{"Patient Name (If Existing Patient)":"8PN7GMQXK5NUM","Patient Name (If New Patient)":null,"Patient Email":"zestlapk123@gmail.com","Patient Phone No":"8484659595","Date of Birth":"2018-01-28","Age":"5","Sex":"Male","Priority":"1(Highest)","Test Requested":"Factor V Leiden (FVL R506Q\/ G1691A) mutation analysis","Sales Lead":"CZGQSEN4PFG3N","Patient Initiation Details":null,"Relatives Name (If secondary samples)":"","Staff Only - Create new patient entry":"false","wid":"101","GPDx ID":"G000075"},"SubmittedBy":null,"tags":["TOP:WFID_101","DOCSEARCH::WFID_101"],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"18527" ,"FormSubmissionID":"18882","FormData":{"Sample ready for processing":"true"},"S ubmittedBy":null,"tags":["WFE1_1:WFID_246","Entry Checklist","DOCSEARCH::WFID_24 6"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
# body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"77860","FormSubmissionID":"101469","FormData":{"Project Initiated by higher management":"true","Comments":null},"SubmittedBy":null,"tags":["COE_WFE1_1:WFID_639","Entry Checklist","DOCSEARCH::WFID_639"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"5322","FormSubmissionID":"19038","FormData":{"Patient Name (If Existing Patient)":"","Patient Name (If New Patient)":"shinchan","Patient Email":"abc@gmail.com","Patient Phone No":"8888888888","Date of Birth":"2018-02-07","Age":null,"Sex":null,"Priority ":null,"Test Requested ":null,"Sales Lead":"","Patient Initiation Details":null,"Relatives Name (if secondary samples)":"","Staff only":null,"Staff Only: Create new patient entry":"true","wid":"248","GPDx ID":"G000080"},"SubmittedBy":null,"tags":["TOP:WFID_248","DOCSEARCH::WFID_248"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WHGJ7HTVTDFH3","FormID":"77860","FormSubmissionID":"101469","FormData":{"Project Initiated by higher management":"true","Comments":null},"SubmittedBy":null,"tags":["COE_WFE1_1:WFID_639","Entry Checklist","DOCSEARCH::WFID_639"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')

body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"WKMUYXELA9LCC","FormID":"18527","FormSubmissionID":"19102","FormData":{"Sample ready for processing":"true"},"SubmittedBy":null,"tags":["WFE1_1:WFID_248","Entry Checklist","DOCSEARCH::WFID_248"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"742","FormSubmissionID":2759,"FormData":{"Product Name":"26FEB","Product Description":null,"Purchase Date":null,"Warranty Expiration":null,"Purchase Cost (Before Tax)":null,"Customer Price (Before Tax)":null,"Profit Percentage":null,"Profit (Purchase Cost - Customer Price) ":null,"Quantity":null,"Supplier (Vendor)":null,"Comments":null},"SubmittedBy":null,"tags":[],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"18","FormSubmissionID":"2716","FormData":{"Customer Satisfied with the Service Provided?":"false","Product Consumed":"Outlook 2013","Comments":null,"Replacement Parts":null},"SubmittedBy":null,"tags":["SER_WFE1_3:WFID_73","Check Out","DOCSEARCH::WFID_73"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"XAJVCAMQQQD4D","FormID":"171","FormSubmissionID":"10700","FormData":{"Status":"Completed"},"SubmittedBy":null,"tags":["WFE1_17:WFID_122","Status","DOCSEARCH::WFID_122"],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"18","FormSubmissionID":"2838","FormData":{"Customer Satisfied with the Service Provided?":"true","Product Consumed":"Outlook 2013","Comments":null,"Replacement Parts":null},"SubmittedBy":null,"tags":["SER_WFE1_3:WFID_76","Check Out","DOCSEARCH::WFID_76"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"XAJVCAMQQQD4D","FormID":"1077","FormSubmissionID":11249,"FormData":{"Customer Name":"Bhagali hospital","Address":null,"State":null,"City":null,"Key Contact 1 Name":null,"Key Contact 1 Phone":null,"Key Contact 1 Email":null,"Key Contact 2 Name":null,"Key Contact 2 Phone":null,"Key Contact 2 Email":null,"Finance Contact 1 Name":null,"Finance Contact 1 Phone":null,"Finance Contact 1 Email":null,"Purchase Contact 1 Name":null,"Purchase Contact 1 Phone":null,"Purchase Contact 1 Email":null,"Sales Person":"","MoU Done":null,"MoU Date":null,"MoU File":null},"SubmittedBy":"6NA569EEKU3TV","tags":[],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"F6BPR2VWXPWQJ","FormID":"100","FormSubmissionID":"9913","FormData":{"Project Initiated by higher management":"true","Comments":null},"SubmittedBy":null,"tags":["COE_WFE1_1:WFID_37","Entry Checklist","DOCSEARCH::WFID_37"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"workflow-click","BusinessTag":"F6BPR2VWXPWQJ","WorkflowID":38}')
# body = json.loads(r'{"Cmd":"workflow-click","BusinessTag":"9SEUR88JAVLN6","WorkflowID":40}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"3JZVHP4PSV4HP","FormID":"133","FormSubmissionID":862,"FormData":{"Name":null,"Email":null,"Phone Number (Just the 10 digit number)":"9889899889","Role":null,"Tag ID":null},"SubmittedBy":null,"tags":[],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"3JZVHP4PSV4HP","FormID":"131","FormSubmissionID":"1301","FormData":{"Project Name":"March","Project Description":"March","Project Plan":null,"Estimeated Launch Date":null,"Priority":"Normal","Status":"Not Started","Start Project?":"Yes","wid":"5"},"SubmittedBy":null,"tags":["TOP:WFID_5","DOCSEARCH::WFID_5"],"url_params":{"users":"{\"selected\":\"5QJGA7PJX3F36\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"A3S7NY7KCKLRC","FormID":"18","FormSubmissionID":"3243","FormData":{"Customer Satisfied with the Service Provided?":"true","Product Consumed":"Office 365 Pro Plus","Comments":null,"Replacement Parts":"[{\"media_name\":\"Screenshot_20171124_172117.png\",\"media_size\":36856,\"media_type\":\"image\\\/png\",\"media\":\"https:\\\/\\\/s3-ap-south-1.amazonaws.com\\\/test-zestl-4\\\/1520599738Screenshot20171124172117.png\",\"media_compressed\":false}]"},"SubmittedBy":null,"tags":["SER_WFE1_3:WFID_89","Check Out","DOCSEARCH::WFID_89"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"9SEUR88JAVLN6","FormID":"7519","FormSubmissionID":"7738","FormData":{"Subflow Name":"Sujoy","Type":"Type A"},"SubmittedBy":null,"tags":["Electrical_NEW:WFID_48","Subflow Selector","DOCSEARCH::WFID_48"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"9SEUR88JAVLN6","FormID":"7519","FormSubmissionID":"7805","FormData":{"Subflow Name":"Akshay","Type":"Type A"},"SubmittedBy":null,"tags":["Electrical_NEW:WFID_49","Subflow Selector","DOCSEARCH::WFID_49"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"9SEUR88JAVLN6","FormID":"7519","FormSubmissionID":"8798","FormData":{"Subflow Name":"SACHIN","Type":"Type A"},"SubmittedBy":null,"tags":["Electrical_NEW:WFID_56","Subflow Selector","DOCSEARCH::WFID_56"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"9SEUR88JAVLN6","FormID":"7519","FormSubmissionID":"10857","FormData":{"Subflow Name":"Kitkat","Type":"Type A"},"SubmittedBy":null,"tags":["Electrical_NEW:WFID_66","Subflow Selector","DOCSEARCH::WFID_66"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"9SEUR88JAVLN6","FormID":"7519","FormSubmissionID":"11433","FormData":{"Subflow Name":"Water234","Type":"Type A"},"SubmittedBy":null,"tags":["Electrical_NEW:WFID_69","Subflow Selector","DOCSEARCH::WFID_69"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
# body = json.loads(r'{"Cmd":"form-submit","BusinessTag":"9SEUR88JAVLN6","FormID":"2","FormSubmissionID":"9007","FormData":{"Project Name":"Minal","Project Description":null,"Project Plan":null,"Estimated Launch Date":"2018-03-01","Priority":"Normal","Status":"Active","wid":"59","Start Project?":"Yes"},"SubmittedBy":null,"tags":["TOP:WFID_59","DOCSEARCH::WFID_59"],"url_params":{"users":"{\"selected\":\"FJBSBPYQMRZZN\"}"}}')
# body = json.loads(r'{"Cmd":"textcard-click","BusinessTag":"9SEUR88JAVLN6","Tags":["Electrical_First:WFID_68","wfe:Electrical_Cable_WFE1_4","parallelWFE_true","DOCSEARCH::WFID_68"]}')
# body = json.loads(r'{"Cmd":"textcard-click","BusinessTag":"9SEUR88JAVLN6","Tags":["Mechanical:WFID_68","wfe:Mechanical_WFE1_1","DOCSEARCH::WFID_68"]}')
# body = json.loads(r'{"Cmd":"textcard-click","BusinessTag":"9SEUR88JAVLN6","Tags":["Electrical_Kitkat:WFID_66","wfe:Electrical_Cable_WFE1_1","DOCSEARCH::WFID_66"]}')
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