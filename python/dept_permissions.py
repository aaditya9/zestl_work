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
import csv
import getopt
import StringIO
import hashlib\

import lib.login1 as LL


def getUsersInGroup(headers, grpID, zbotID):
    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + grpID + '/' + zbotID, None, headers)
    # jsd = json.loads(jsondata)
    return jsondata
    
def getAllUserGroups(headers, zbotID):
    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + zbotID, None, headers)
    # 
    # print "User Group API response : Code : " + str(jsondata['code'])
    # print "======================="
    # print jsondata['reply']
    # print "======================="
    return jsondata['reply']

def add_user(body, headers, zbotID, grpID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/' + grpID + '/user/add/' + zbotID, body, headers)
    
    # print "User Group API response : Code : " + str(jsondata['code'])
    # print "======================="
    # print jsondata['reply']
    # print "======================="
    return jsondata['reply']

def get_details(body, headers, hit_url):
    jsondata = LL.invoke_rest('POST', hit_url, body, headers)
    
    # print "User Group API response : Code : " + str(jsondata['code'])
    # print "======================="
    # print jsondata['reply']
    # print "======================="
    return jsondata['reply']   
   
def add_usergrps_grps(body, headers, zbotID, grpID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/' + grpID + '/usergroup/add/' + zbotID, body, headers)
    print "User Group API response : Code : " + str(jsondata['code'])
    print "======================="
    print jsondata['reply']
    print "======================="
    return jsondata['reply']

def change_view_permissions(body, headers, zbotID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'zvice/interaction/' + zbotID, json.dumps(body), headers)
    return jsondata['reply']

def change_view_permissions_fullurl(body, headers, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL , json.dumps(body), headers)
    return jsondata['reply']


def create_text_card_dept(body, headers, zbotID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'zvice/interaction/' + zbotID, json.dumps(body), headers)
    return jsondata['reply']

def expand(std):
        if std == "1" or std == "2" or std == "3" or std == "4":
            vals = [std+'A', std+'B', std+'C', std+'D', std+'E', std+'F']
        if std == "5" or std == "6" or std == "7" or std == "8" or std == "9":
            vals = [std+'A', std+'B', std+'C', std+'D', std+'E']
        if std == "10":
            vals = [std+'A', std+'B', std+'C']
        # "2": "green",
        # "3": "blue",
        # "4": "yellow",
        # 
        return vals # if the house is not assigned - then use "not assigned" as value.

def create_gallery(body, headers, zbotID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + zbotID + "/gallery", json.dumps(body), headers)
    return jsondata['reply']

def create_nested_cards(body, headers, zbotID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + "zvice/interaction/" + zbotID, json.dumps(body), headers)
    return jsondata['reply']

def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']

def getArgs(argv):
    loginfile = ''
    # outputfile = ''
    print argv
    try:
       opts, args = getopt.getopt(argv[1:],"hi:ol:")
       print opts
       print args
    except getopt.GetoptError:
       print argv[0] + ' -l <loginfile>'
       sys.exit(2)
    for opt, arg in opts:
        if opt in ("-l"):
            loginfile = arg    
            print loginfile
   #          print 'test.py -i <inputfile> -o <outputfile>'
   #          sys.exit()
   #      elif opt in ("-i", "--ifile"):
   #        inputfile = arg
   #      elif opt in ("-o", "--ofile"):
   #       outputfile = arg
   # print 'Input file is "', inputfile
   
    return loginfile, args
   
   # print 'Output file is "', outputfile

if __name__ == '__main__':
        
        # i must login
        print sys.argv
        args, loginfile = getArgs(sys.argv)
        print loginfile
        print args
        # headers, headers1 = LL.req_headers()
        
        # usergroups = getAllUserGroups(headers1, LL.zbotID)
        # 
        # # ## the response is ugly - so i'll housekeep it
        # 
        # grpvals = json.loads(usergroups)
        # print "=======================****"
        # grps = grpvals['output']
        # grpname = grps['usergroup']
        # # for k, v in grpname.items():
        # #     print (k, "   ::::   ", v)
        # # 
        # # 
        # # ###### change the permissions of a department based on a tsv file of format
        # # ##### <dept_tag_id> \t <group name> \t <permission_type>
        # with open(sys.argv[1], 'r') as f:
        #     for line in f:
        #         args = line.split('\t')
        #         zbotID = args[0].strip()
        #         if  args[2].strip() == 'V':
        #             actionType = 'VIEW'
        #         if args[2].strip() == 'A':
        #             actionType = 'ADMIN'
        #         std=args[1].strip()
        #         if '*' in std:
        #             std = std.replace('*', '')
        #             std = std.replace('Teachers', '')
        #             std = expand(std.strip())
        #             for x in std:
        #                 grpID = grpname[("Teachers " + x)]
        #                 # print zbotID + '\t' + str(grpID) + '\t' + actionType
        #                 RequestBody = { "interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN",
        #                                 "opType": "1",
        #                                 "actionType": actionType,
        #                                 "groupID": str(grpID),
        #                                 "cardID": "",
        #                                 "cardType": ""
        #                             }
        #                 response = change_view_permissions(RequestBody, headers1, zbotID)                    
        #                 print response
        #                                                 
        #         else:
        #             grpID = grpname[args[1].strip()]
        #             # print zbotID + '\t' + str(grpID) + '\t' + actionType
        #             RequestBody = { "interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN",
        #                              "opType": "1",
        #                              "actionType": actionType,
        #                              "groupID": str(grpID),
        #                              "cardID": "",
        #                              "cardType": ""
        #                          }
        #             response = change_view_permissions(RequestBody, headers1, zbotID)                    
        #             print response
        # 
        # 
        ###### try comm preferences

        # 
        # title = "Communication Preferences"
        # hit_url = "https://twig.me/v1/zvice/interaction/3P5LAQ9J7DQ7Z"
        # body  = {"interactionID":"CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN","cardType":"GenericCard","cardID":273,"actionType":"MAIL", "groupID" : "96", "opType" : "1"}
        # 
        # # {"cardType":"GenericCard","cardID":273}
        # 
        # response = get_details(json.dumps(body), headers1, hit_url)
        # print response
#         
#         cardsjsonurl : "https://twig.me/v1/zvice/interaction/3P5LAQ9J7DQ7Z"
# rawhtml : null
# method : "POST"
# content : "{"interactionID":"CommonInteraction_INTERACTION_TYPE_GET_CARDS_PERMISSIONS_USR_GRPS","cardType":"GenericCard","cardID":273,"actionType":"MAIL"}"
# widgets : null
# cardtype : "mastercard"
# title : "Communication via Mail"
# titleicon : null
# subtitle : null
# showcontent : "true"
# showHeader : "true"
# actions : null
# backgroundImageUrl : null
# refresh : "false"
# fullwidth : true
#         
#         
        ##### change permission code end
        
        ###### code to change admin/view permissions of a department
        # print grpname
        # grpID = '219'
        # actionType = 'VIEW'
        # RequestBody = { "interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN",
        #                 "opType": "1",
        #                 "actionType": actionType,
        #                 "groupID": grpID,
        #                 "cardID": "",
        #                 "cardType": ""
        #             }
        # zbotID = 'WNNGLRB8VA64K'
        # response = change_view_permissions(RequestBody, headers1, zbotID)                    
        # print response
        
        ######## end change permission code
        
#         basecard
#         supercard
#         buttoncard
#         textcard
#         [6:03 PM, 6/23/2016] Lankesh Zade: imagecard
# [6:04 PM, 6/23/2016]?Lankesh Zade:?slideshowcard
# [6:04 PM, 6/23/2016]?Lankesh Zade:?formcard
# [6:04 PM, 6/23/2016]?Lankesh Zade:?calendarcard
#         [6:04 PM, 6/23/2016] Lankesh Zade: calendareventcard
# [6:04 PM, 6/23/2016]?Lankesh Zade:?mastercard
# [6:04 PM, 6/23/2016]?Lankesh Zade:?headercard
#         [6:04 PM, 6/23/2016] Lankesh Zade: footercard
# [6:04 PM, 6/23/2016]?Lankesh Zade:?videocard
# [6:05 PM, 6/23/2016]?Lankesh Zade:?youtubecard
#         [6:05 PM, 6/23/2016] Lankesh Zade: webviewcard
# [6:05 PM, 6/23/2016]?Lankesh Zade:?linkcard
#         [6:05 PM, 6/23/2016] Lankesh Zade: locationcard
# [6:05 PM, 6/23/2016]?Lankesh Zade:?nextcard
#         
    #     
    #     // Card Type as in Card Settings DB Table's card type field
    # const CARD_TYPE_TEXT = "TEXT";
    # const CARD_TYPE_CHAT = "CHAT";
    # const CARD_TYPE_CHAT_COMMENT = "CHAT_COMMENT";
    # const CARD_TYPE_FORM = "FORM";
    # const CARD_TYPE_FORMSUB = "FORM_SUB";
    # const CARD_TYPE_CALENDAR = "CALENDAR";
    # const CARD_TYPE_LINK = "LINK";
    # const CARD_TYPE_EVENT = "EVENT";
    # const CARD_TYPE_GALLERY = "GALLERY";
    # const CARD_TYPE_REVIEW = "REVIEW";
    # const CARD_TYPE_REVIEW_COMMENT = "REVIEW_COMMENT";
    # const CARD_TYPE_VIDEO = "VIDEO";
    # const CARD_TYPE_ATTENDANCE = "ATTENDANCE";
    #     




        #### create a new text card in a department
        # groups = ['3 & 4', '5 & 6', '7 & 8', '9 & 10', '11 & 12']
        # for x in groups:
        #     title = 'Class ' + x + ' Teachers forum'
        #     description = 'Class ' + x + ' Teachers forum'
        #     RequestBody = { "cardType": "CHAT",
        #                     "opType": "1",
        #                     "cardData": {
        #                                 "title": title,
        #                                 "desc": description,
        #                                 "text" : title, 
        #                                 },
        #                     "interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
        #                     # "interactionID": CommonInteraction_INTERACTION_TYPE_GET_CARDS
        #                     }
        #     zbotID = '3P5LAQ9J7DQ7Z'
        #     response = create_text_card_dept(RequestBody, headers1, zbotID)                    
        #     print response
            # print x
        # response = json.loads(response)
       
        # 
        # zbotID = '3P5LAQ9J7DQ7Z'
        # RequestBody = {"Title":"Teachers gallery","Description":"Teachers Gallery"}
        # response = create_gallery(RequestBody, headers1, zbotID)
        # print response
        # 
        #
        
        ##### create the necessary cards inside the class departments.
        # with open(sys.argv[1], 'r') as csvfile:
        #     for line in csvfile:
        #         args = line.split('\t')
        #         tagID = args[0]
        #         classID = args[1]
        #         classes = expand(re.sub(r'Class (\d+)\*',r'\1',classID).strip())
        #         for x in classes:
        #             zbotID = tagID
        #             textcardsub = "HW for Class " + x
        #             calendarsub = "Time table for Class " + x
        #             gallerysub = "Gallery for Class " + x
        #             print textcardsub + calendarsub + gallerysub
        #             title = textcardsub
        #             description = textcardsub
        #             RequestBody = { "cardType": "TEXT",
        #                                "opType": "1",
        #                                "cardData": {
        #                                            "title": title,
        #                                            "desc": description,
        #                                            "text" : title, 
        #                                            },
        #                                "interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
        #                                # "interactionID": CommonInteraction_INTERACTION_TYPE_GET_CARDS
        #                                }
        #             response = create_text_card_dept(RequestBody, headers1, zbotID)                    
        #             print response
        #             
        #             title = calendarsub
        #             description = calendarsub
        #             RequestBody = { "cardType": "TEXT",
        #                                "opType": "1",
        #                                "cardData": {
        #                                            "title": title,
        #                                            "desc": description,
        #                                            "text" : title, 
        #                                            },
        #                                "interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
        #                                # "interactionID": CommonInteraction_INTERACTION_TYPE_GET_CARDS
        #                                }
        #             response = create_text_card_dept(RequestBody, headers1, zbotID)                    
        #             print response
        #             
        #             title = gallerysub
        #             description = gallerysub
        #             RequestBody = {"Title": gallerysub,"Description": gallerysub}
        #             response = create_gallery(RequestBody, headers1, zbotID)
        #             print response
        #             #           
                    # end code create text cards et al
        
        #         
        #     fieldnames 
        #     writer = csv.reader(csvfile)
        #     
        # print writer
        # # 
        # for k,v in writer.items():
        #     print (k, v)

          
      # 
      # ##### just getting the list of all cards at this level
      #   title = 'Delete this card'
      #   description = 'Delete this card'
        # zbotID = '3P5LAQ9J7DQ7Z'
        # url = 'https://www.twig.me/v1/zvice/detailscard/' + zbotID
        # # print url
        # RequestBody = {"recentTagIds":["3KMGPB7EPJBWP","CHECSR8W8ECHL","C3VNW7MVTK2K4","BWSVDSVU8NB6S","2PNNBUMU6KFFM","8T3AX56TQKTGP","7WM7FWQGQZMZC","32SRULXYRKUU2"]}
        # response = hit_url(RequestBody, headers1, LL.zbotID, url)
        # with open('tmp', 'w') as f:
        #     f.write(str(response))
        # response = json.loads(response)
        # # output = StringIO.StringIO(response)
        # 
        # # print response['data']['elements']
        # cards = response['data']['elements']
        # for x in cards:
        #     # print x['title']
        #     if re.search('Class', x['title']):
        #         classA = re.sub(r'Class (\d+) & (\d+).*', r'\1', x['title'])
        #         classB = re.sub(r'Class (\d+) & (\d+).*', r'\2', x['title'])
                # print x['actions'][0]
                # BASE_URL = x['actions'][5]['actions'][0]['actionUrl']
                # body = x['actions'][5]['actions'][0]['data']
                # # print body
                # body = json.loads(body)
                # # print body
                # 
                # 
                # response = change_view_permissions_fullurl(body, headers1, BASE_URL)
                # # print response
                # response = json.loads(response)
                # for a in response['data']['elements']:
                #     # if re.search('Calendar', a['title']):
                #         # print a['title']
                #         # print a['actions'][4]['actions'][1]
                #     if re.search('Forum', a['title']):
                #         # print a['title']
                
                
                
                # # # a = x
                # # # for s in a['actions']:
                # # #     if re.search('User Permission', s['title']):
                # # #         for u in s['actions']:
                # # #             if re.search('Communication', u['title']):
                # # #                 BASE_URL = u['actionUrl']
                # # #                 # print BASE_URL
                # # #                 # print u['data']
                # # #                 body = json.loads(u['data'])
                # # #                 # print body
                # # #                 response = change_view_permissions_fullurl(body, headers1, BASE_URL)
                # # #                 response = json.loads(response)
                # # #                 for b in response['data']['elements']:
                # # #                     if re.search('Communication via Mail', b['title']):  
                # # #                         BASE_URL = b['cardsjsonurl']
                # # #                         body = json.loads(b['content'])   
                # # #                         response = change_view_permissions_fullurl(body, headers1, BASE_URL)
                # # #                         # print response
                # # #                         response = json.loads(response)
                # # #                         for c in response['data']['elements']:
                # # #                             if re.search('Communication ', c['content']):
                # # #                                 print c['actions'][0]['actions'][0]['title']
                # # #                                 body = {}
                # # #                                 actionUrl = c['actions'][0]['actions'][0]['actionUrl']
                # # #                                 print actionUrl
                # # #                                 # i = 2
                # # #                                 for i in range (2, 7):
                # # #                                     body[c['actions'][0]['actions'][0]['inputs'][i]['properties'][0]['value']] = c['actions'][0]['actions'][0]['inputs'][i]['properties'][1]['value']
                # # #                                     # i += 1
                # # #                                 print (classA, classB)
                # # #                                 for y in expand(classA):
                # # #                                     group =  'Teachers ' + y
                # # #                                     body['groupID'] = grpname[group]
                # # #                                     response = change_view_permissions_fullurl(body, headers1, BASE_URL)
                # # #                                     print response
                # # #                                 for y in expand(classB):
                # # #                                     group =  'Teachers ' + y
                # # #                                     body['groupID'] = grpname[group]
                # # #                                     response = change_view_permissions_fullurl(body, headers1, BASE_URL)
                # # #                                     print response
                # # #                                     # print body
                # # #
                
                
      #           
      #           #### set permissions code
      #           print (classA, classB)
      #           for y in expand(classA):
      #               group =  'Teachers ' + y
      #               print grpname[group]
      #               # body = x['actions'][8]['actions'][0]['data']
      #               BASE_URL = x['actions'][0]['actionUrl']
      #               body = x['actions'][0]['data']
      #               body = json.loads(body)
      #               # print body
      #               
      #               response = change_view_permissions_fullurl(body, headers1, BASE_URL)
      #               response = json.loads(response)
      #               for a in response['data']['elements']:
      #                   if re.search('Calendar', a['title']):
      #                       # print a['title']
      #                       # print a['actions'][4]['actions'][1]
      #                       body = json.loads(a['actions'][4]['actions'][1]['data'])
      #                       BASE_URL = a['actions'][4]['actions'][1]['actionUrl']
      #                       body['groupID'] = str(grpname[group])
      #                       body['interactionID'] = 'CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN'
      #                       body['opType'] = "1"
      #                       print (body, BASE_URL)
      #                       response = change_view_permissions_fullurl(body, headers1, BASE_URL)
      #                       print response
      #           for y in expand(classB):
      #               group =  'Teachers ' + y
      #               print grpname[group]
      #               # body = x['actions'][8]['actions'][0]['data']
      #               BASE_URL = x['actions'][0]['actionUrl']
      #               body = x['actions'][0]['data']
      #               body = json.loads(body)
      #               # print body
      #               
      #               response = change_view_permissions_fullurl(body, headers1, BASE_URL)
      #               response = json.loads(response)
      #               for a in response['data']['elements']:
      #                   if re.search('Calendar', a['title']):
      #                       # print a['title']
      #                       # print a['actions'][4]['actions'][1]
      #                       BASE_URL = a['actions'][4]['actions'][1]['actionUrl']
      #                       body = json.loads(a['actions'][4]['actions'][1]['data'])
      #                       body['groupID'] = str(grpname[group])
      #                       body['interactionID'] = 'CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN'
      #                       body['opType'] = "1"
      #                       print (body, BASE_URL)
      #                       response = change_view_permissions_fullurl(body, headers1, BASE_URL)
      #                       print response
      #                       
                #     BASE_URL = x['actions'][8]['actions'][0]['actionUrl']
                #     print BASE_URL
                #     body = json.loads(body)
                #     body['groupID'] = str(grpname[group])
                #     body['interactionID'] = 'CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN'
                #     body['opType'] = "1"
                #     # body = json.dumps(body)
                #     print body
                #     response = change_view_permissions_fullurl(body, headers1, BASE_URL)
                #     print response
                # for y in expand(classB):
                #     group = 'Teachers ' + y
                #     print grpname[group]
                #     body = x['actions'][8]['actions'][0]['data']
                #     BASE_URL = x['actions'][8]['actions'][0]['actionUrl']
                #     print BASE_URL
                #     body = json.loads(body)
                #     body['groupID'] = str(grpname[group])
                #     body['interactionID'] = 'CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN'
                #     body['opType'] = "1"
                #     # body = json.dumps(body)
                #     print body
                #     response = change_view_permissions_fullurl(body, headers1, BASE_URL)
                #     print response
                    
                ### codes done

               
        # print response['data']['elements'][1]['actions'][7]['actions'][0]
        # hit_url = response['homeurl']
        # # hit_url = 'https://twig.me/v1/zvice/detailscard/7X5B5U27RCXCP'
        # # https://twig.me/v1/zvice/interaction/9J5EDAR3Y2PZA
        # body = response['data']
        # response = get_details(json.dumps(body), headers1, hit_url)
        # print response
        # # response = json.loads(response)
        # response = response['data']
        # response = response['elements']
        # # print response
        # for k in response:
        #     # print k
        #     for i, name in enumerate(k):
        #         if name == 'cardtype' :
        #             # if name == 'profileId':
        #             #     print k['cardtype'] + '\t' + k['title'] + '\t' + k['profileId']
        #             # # print cardtype
        #             # else:
        #             for j, name1 in enumerate(k):
        #                 if name1 == 'profileId' :
        #                     print k['cardtype'] + '\t' + k['title'] +  '\t' + k['profileId']
        #                 # else :
        #             print k['cardtype'] + '\t' + k['title'] 
        #         print k 
      ##### 
        
        
     
        
        # grpdetails = getUsersInGroup(headers1, "292" ,LL.zbotID)
        # print grpdetails
        # grpd = json.loads(grpdetails['reply'])        
        # grpd = grpd['output']
        # grpd = grpd['groupdetails']
        # print len(grpd)
        # if (len(grpd) > 0):
        #     print "long"
        # print "=========###########=============="
        # print grpd
        #
        
        #############start here for details of users in a group
        # for k, v in grpname.items():
        #     print "=========###########==============" 
        #     print (k)
        #     print (v)
        #     grpdetails = getUsersInGroup(headers1, str(v) ,LL.zbotID)
        #     if(grpdetails['code'] == 200):
        #         print "=================================="
        #         grpd = json.loads(grpdetails['reply'])        
        #         grpd = grpd['output']
        #         grpd = grpd['groupdetails']
        #         if (len(grpd) > 0):
        #             if 'users' in grpd.keys():
        #                 # print "found users"
        #                 grpd = grpd['users']
        #                 for k, v in grpd.items():
        #                     print (k, v)
        #             else:
        #                 for k, v in grpd.items():
        #                     print (k, v)
        #                     
                            
        ######### end details of users in a group
        
        
        
                # # if (len(grpd) == 1):
                # #     for k, v in grpd.items():
                # #         print (k, v)
                # # 
        # 
        # 
        # print grpname
        # print " groups : %s " % grpname.keys()
        # print "=======================****"
        # for k, v in grpname.items():
        #     print (k)
        # groupA = groupnames.split("\"")
        # groupA = [w.replace(':', '') for w in groupA]
        # groupA = [w.replace(',', '') for w in groupA]
        
        ## and create the key value pairs
        # dict1 = dict(zip(groupA[1::2],groupA[2::2]))
        # dict1 = grpname
        # print grpname
        # 
        # grpdetails = getUsersInGroup(headers1, '162' ,LL.zbotID)
        # 
        # print "=========#####=============="
        # grpd = json.loads(grpdetails['reply'])        
        # grpd = grpd['output']
        # grpd = grpd['groupdetails']
        # grpd = grpd['users']
        # for k, v in grpd.items():
        #     print (k, v)
       
        #dict1 is the golden dictionary for this script now
        
        # # now open that file specified on the command line format of which is
        # # zvice_id   group_name
        # # 
        # with open(sys.argv[1], 'r') as f:
        #     for line in f:
        #         needs = line.split('\t')
        #         trialgrp = needs[1].strip()
        #         originalgrp = needs[0].strip()
        #         if len(originalgrp) > 0 :
        #             g1 = grpname[originalgrp]
        #             print g1
        #         if len(trialgrp) > 0:
        #             grpID = grpname[trialgrp]
        #             
        #             print str(g1)
        #             print str(grpID)
        #             body = { "grpUserGroupID" : str(g1) }
        #             add_usergrps_grps(json.dumps(body), headers1, LL.zbotID, str(grpID))
        #                         
        #             
        #         zvice = needs[0]
        #         grpID = dict1[trialgrp]
        #         body = { 'grpUserZviceID'  : zvice}
#    	 "grpUserGroupID" : <UserGroupID>
# add_usergrps_grps
        #         add_user(json.dumps(body), headers1, LL.zbotID, str(grpID))
        # 
        
