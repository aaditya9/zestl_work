#!/usr/local/bin/python

# usage create_groups.py <file_containing_grpnames_to_create>
# ensure the file dev_millennium.py in the lib directory is configured correctly

import json
import sys
import time
import hashlib\

import lib.login1 as LL

def set_groups(body, headers, zviceID):
    return LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/add/' + zviceID, json.dumps(body), headers)

def change_linked_user(body, headers, zviceID):
    return LL.invoke_rest('POST', LL.BASE_URL + 'zvice/interaction/' + zviceID, json.dumps(body), headers)

# errorFile = "gold.txt"
if __name__ == '__main__':

        headers, headers1 = LL.req_headers()
        inputfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.txt"

        with open(inputfile, 'r') as f:
            # with open(errorFile, "a") as ef:

            for line in f:
                details = line.split('\t')
                zviceID = details[0].strip()
                emailID = details[1].strip()
                body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_LINK_USERPROFILE","linkemail": emailID}
                response = change_linked_user(body, headers1, zviceID)
                # ef.write(zviceID + "  ::  " + response + "\n")
                print zviceID
                print emailID
                print response