#!/usr/local/bin/python

# usage create_groups.py <file_containing_grpnames_to_create>
# ensure the file dev_millennium.py in the lib directory is configured correctly

import json
import sys
import hashlib\

import lib.login1 as LL

def set_groups(grpname, headers, zviceID, BASE_URL):
    body = {'groupName': grpname}
    return LL.invoke_rest('POST', BASE_URL + 'usergroups/add/' + zviceID, json.dumps(body), headers)


if __name__ == '__main__':
        #log in of course
        headers, headers1 = LL.req_headers()
        
        # open the file specified on command line
        grplist = []
        with open(sys.argv[1], 'r') as my_file:
            for line in my_file:
                groupnames = line.split('\t')
                gn = groupnames[1].strip()
                if(len(gn) > 0):
                    if  gn not in grplist:
                        grplist.append(gn)
                        # print grplist
        for x in grplist:
            print x
        
        
        # go ahead and create those groups    
        for x in grplist: 
            body =  {'groupName': x}
            print set_groups(x, headers1, LL.zbotID)
            # print result_setgrps
        
 
