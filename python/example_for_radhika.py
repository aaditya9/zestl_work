#!/usr/local/bin/python

# usage create_groups.py <file_containing_grpnames_to_create>
# ensure the file dev_millennium.py in the lib directory is configured correctly

import json
import sys
import hashlib
import argparse
from ast import literal_eval
#
import lib.login1 as LL

#def set_groups(body, headers, zviceID):
#    return LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/add/' + zviceID, json.dumps(body), headers)

def return_title_and_desc(body, headers, zviceID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'zvice/detailscard/' + zviceID, json.dumps(body), headers)
    return jsondata['reply']
    
def return_linked_user_mail(url, body, headers):
    #print url
    jsondata = LL.invoke_rest('POST', url, json.dumps(body), headers)
    return jsondata['reply']


def return_more_details(body, headers, zviceID):
    jsondata =  LL.invoke_rest('POST', LL.BASE_URL + 'zvice/interaction/' + zviceID, json.dumps(body), headers)
    return jsondata['reply']

if __name__ == '__main__':
        #log in of course
        headers, headers1 = LL.req_headers()
        
        #take zviceID from prompt
        parser = argparse.ArgumentParser()
        parser.add_argument('-tagid', nargs=1, type=str, required=True, dest='tagID', help = 'Provide tag ID')
        args = parser.parse_args()

        zviceID = args.tagID[0]
        print "User TagID : " + zviceID
        
        #fetch user name and description
        response = json.loads(return_title_and_desc(None, headers1, zviceID))
        rdata = response['data']
        rdata = rdata['elements']
        for x in rdata:
            if x['cardtype'] == 'basecard':
                print "User Title : " + x['title']
                print "User Description : " + x['content']
                
            #fetch linked user mail id
            if x['title'] == 'Link to TwigMe User':
                for y in x['actions']:
                    if y['title'] == 'Linked User':
                        linkedUser = y['data']
                        linkedUser = literal_eval(linkedUser)
                        linkedUser = linkedUser['tagIds'][0]
                        print "Linked User Twig Me Tag : " + linkedUser
                        response = json.loads(return_title_and_desc(None, headers1, linkedUser))
                        print response
                    #    linkedResponse = json.loads(return_linked_user_mail (y['actionUrl'], y['data'], headers1))
                     #   print linkedResponse
#                        a = y['data']
#                        print a
#                        print type(a)
            #print x['title']
           # break
  #          for i, name in enumerate(x):
 #               print name
   #             if name == 'title':
    #                print x[name]
 #                   print (x['title'] + '\t' + x['content'])
 #               if name ==  'tagID':
 #                   print (x['title'] + '\t' + x['content'])
                
        print "============================"
        
        RequestBody = {
            "interactionID": "CommonInteraction_INTERACTION_TYPE_SHOW_GENERIC_NOTES",
            "notetype": "P",
            "useclubbing": 'false'
        }
 
        zviceID = 'FL4BEYWC9TZ4E' ## sudents qr code
#        print return_more_details(RequestBody, headers1, zviceID)
        response = json.loads(return_more_details(RequestBody, headers1, zviceID))
        rdata = response['data']
        rdata = rdata['elements']
        for x in rdata:
            for i, name in enumerate(x):
                if name == 'content':
                    print (x['title'] + '\t' + x['content'])
 
 
 
