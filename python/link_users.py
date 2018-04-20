#!/usr/local/bin/python

# usage create_groups.py <file_containing_grpnames_to_create>
# ensure the file dev_millennium.py in the lib directory is configured correctly

import json
import sys
import hashlib\

import lib.login1 as LL

def set_groups(body, headers, zviceID):
    return LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/add/' + zviceID, json.dumps(body), headers)

def change_linked_user(body, headers, zviceID):
    return LL.invoke_rest('POST', LL.BASE_URL + 'zvice/interaction/' + zviceID, json.dumps(body), headers)


if __name__ == '__main__':
        #log in of course
        headers, headers1 = LL.req_headers()
  
        inputfile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/UserLinking_17Nov.txt"
  #read from a file
        
        with open(inputfile, 'r') as f:
            for line in f:
                details = line.split('\t')
                zviceID = details[0].strip()
                emailID = details[1].strip()
                body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_LINK_USERPROFILE","linkemail": emailID}
                response = change_linked_user(body, headers1, zviceID)
                try:
                    response = json.loads(response['reply'])['message']
                except:
                    response = response
                print zviceID
                print emailID
                print response
