
import json
import sys
import csv
import re
import hashlib\


import lib.login1 as LL

    
def getAllUserGroups(headers, zbotID):
    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + zbotID, None, headers)
    return jsondata['reply']

def getConfigCards(body, headers, zbotID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'zvice/interaction/' + zbotID, body, headers)
    return json.loads(jsondata['reply'])

def configureCards(body, headers, zbotID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'zvice/interaction/'  , body, headers)
    
    return jsondata['reply']
    # return json.loads(jsondata['reply'])


def change_view_permissions(body, headers, zbotID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'zvice/interaction/' + zbotID, json.dumps(body), headers)
    return jsondata['reply']


def create_nested_cards(body, headers, zbotID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + "zvice/interaction/" + zbotID, json.dumps(body), headers)
    return jsondata['reply']

def getcardID(body, headers, zbotID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + "zvice/interaction/" + zbotID, json.dumps(body), headers)
    return jsondata['reply']


if __name__ == '__main__':
        #log in of course
    headers, headers1 = LL.req_headers()
    
    usergroups = json.loads(getAllUserGroups(headers1, LL.zbotID))
    
    grps = []
    grpdict = usergroups['output']['usergroup']
    for k, v in usergroups['output']['usergroup'].items():
        grps.append(k)
    if (len(grps) != len(set(grps))):
        print "duplicate groups found"
    else:
        print grpdict
    
    # body = {
    #         "interactionID": "INTERACTION_TYPE_GET_CONFIG_CARDS"
    #         }
    # response = getConfigCards(json.dumps(body), headers1, LL.zbotID)
    # response = response['data']['elements']
    # for x in response:
    #     flag = 0
    #     for k,v in x.items():
    #         if k == 'hidden':
    #             flag = 1
    #     if flag == 1 :
    #         print x['title'] + '\t' + str(x['hidden'])
    #     else:
    #         print x['title']
    # 
    # print response[4]
    # # None = 'None'
    # resp = {'tagId': '9J5EDAR3Y2PZA', 'hidden': False,  'title': 'Send a note to school',  'fullwidth': True, }
    # requestBody = {
    #     "interactionID": "INTERACTION_TYPE_SET_CONFIG_CARDS",
    #     "applyforall": 'false',
    #     "customcards": resp }
    # print "======================"
    # print requestBody
    # response = configureCards(json.dumps(requestBody), headers1, LL.zbotID)
    # print response
    # 
        
    # l = [1,2,3,4,4,5,5,6,1]
    # print len(l)
    # u = set(l)
    # print u
    # print len(u)
    # # set([x for x in l if l.count(x) > 1])
    
    
    tadIDdict = {}

##### read the tag IDs for the various departments

    filename = '../millennium/script_inputs/mill_dept_tagids.csv'
    with open(filename, 'r') as csvfile:
        text = csvfile.readline().strip().split(',')
    with open(filename, 'r') as csvfile:
        # spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        # for item in spamreader:
            # print item
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (re.search('Class', row[text[1]])):
                print (row[text[0]], row[text[1]])
                students = re.sub(r'(Class\s+(\d+))', r'\1', row[text[1]])
                # teachers = 'Teachers ' + re.sub(r'.* for (Class\s+(\d+.*))', r'\2', row[text[1]])
                print (students)
                tadIDdict[students] =  row[text[0]]
                # print tadIDdict
### end read tag IDs


# ## read the gallery cards file
#     filename = '../millennium/script_inputs/gallery_cards.txt'
#     with open(filename, 'r') as csvfile:
#         gal = csvfile.readline().strip().split(',')
#     with open(filename, 'r') as csvfile:
#         # spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
#         # for item in spamreader:
#             # print item
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if (re.search('Class', row[gal[2]])):
#                 print (row[gal[0]], row[gal[1]], row[gal[2]])
#                 students = re.sub(r'.*(Class\s+(\d+.*))', r'\1', row[gal[2]])
#                 dept = re.sub(r'.*(Class\s+(\d+)).*', r'\1', row[gal[2]])
#                 teachers = 'Teachers ' + re.sub(r'.*(Class\s+(\d+.*))', r'\2', row[gal[2]])
#                 print (students, teachers)
#                 print (row[gal[0]], grpdict[students], grpdict[teachers])
#                 cardID = row[gal[0]]
#                 grpID = grpdict[teachers]
#                 zbotID = tadIDdict[dept]
#                 print (cardID, grpID, zbotID)
#                 actionType = 'ADMIN'
#                 RequestBody = { "interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN",
#                                                     "opType": "1",
#                                                     "actionType": actionType,
#                                                     "groupID": str(grpID),
#                                                     "cardID": str(cardID),
#                                                     "cardType": "GenericCard"
#                                                 }
#                 response = change_view_permissions(RequestBody, headers1, zbotID)                    
#                 print response
                 
## end read gallery cards


       ######### create a card inside a card - confirmed working.
        # 
        # parentID = '94'
        # ctype = 'TEXT'
        # desc = 'delete this card - testing only'
        # title = 'test card'
        # zbotID = 'WNNGLRB8VA64K'  ## the tagID of the correct department must be specified here.
        # RequestBody = {"cardData":
        #                   {"desc":desc, "title":title},
        #                   "opType":"1",
        #                   "parentCardID":parentID,
        #                   "cardType": ctype,
        #                   "interactionID":"CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
        #             }
        # response = create_nested_cards(RequestBody, headers1, zbotID)
        # print response
        # 
        ######## end create nested cards
      

### read the text cards file
    # filename = '../millennium/script_inputs/text_cards.txt'
    # with open(filename, 'r') as csvfile:
    #     text = csvfile.readline().strip().split(',')
    # with open(filename, 'r') as csvfile:
    #     # spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    #     # for item in spamreader:
    #         # print item
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         if (re.search('for Class', row[text[1]])):
    #             print (row[text[0]], row[text[1]], row[text[2]])
    #             students = re.sub(r'.* for (Class\s+(\d+.*))', r'\1', row[text[1]])
    #             teachers = 'Teachers ' + re.sub(r'.* for (Class\s+(\d+.*))', r'\2', row[text[1]])
    #             dept = re.sub(r'.* for (Class\s+(\d+)).*', r'\1', row[text[2]])
    #             # print (students, teachers)
    #             # print (row[text[0]], grpdict[students], grpdict[teachers])
    #             cardID = row[text[0]]
    #             grpID = grpdict[teachers]
    #             zbotID = tadIDdict[dept]
    #             print (cardID, grpID, zbotID)
    #             actionType = 'ADMIN'
    #             RequestBody = { "interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN",
    #                                                 "opType": "1",
    #                                                 "actionType": actionType,
    #                                                 "groupID": str(grpID),
    #                                                 "cardID": str(cardID),
    #                                                 "cardType": "GenericCard"
    #                                             }
    #             response = change_view_permissions(RequestBody, headers1, zbotID)                    
    #             print response
            ### end read text cards
    


    # zbotID = tadIDdict['Class 1']
    # for k,v in tadIDdict.items():
    #     print tadIDdict[k]
    #  
    # zbotID = tadIDdict['Class 1']
    # print zbotID

    # zbotID = 'WNNGLRB8VA64K'
    # print zbotID
    # grpID = 60
    # actionType = 'VIEW'
    # RequestBody = { "interactionID": "CommonInteraction_INTERACTION_TYPE_CARD_SETTINGS_USERGROUP_OPN",
    #                                     "opType": "1",
    #                                     "actionType": actionType,
    #                                     "groupID": str(grpID),
    #                                     "cardID": "96",
    #                                     "cardType": "GenericCard"
    #                                 }
    # response = change_view_permissions(RequestBody, headers1, zbotID)                    
    # print response
 
    
    response = getcardID(RequestBody, headers1, zbotID)
    