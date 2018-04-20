import json
import logon as LL
import common as CM
import sys

# form_name = ["Generate Report", "3A", "2B", "2A", "1C", "1B", "1A", "start"]
# form_id = [1643, 1642, 1641, 1640, 1639, 1638, 1637, 1636]  #### these ids for DEV server


def submit_form(a):
    # BASE_URL = "http://twig-me.com/v8/"  ### dev server
    # zviceID = "X5NXPTNGRG2H3"  # Work flow demo department

    # BASE_URL = "http://35.154.64.119/v8/"   ### testtttttttttttt
    # zviceID = "BBMAUZGTSPJLM"   # test minal business id
    #
    # email = "admin@zestl.com"
    # pwd = "TwigMeNow"
    #
    # headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

    # jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
    # form_name = ["Generate Report" , 3A , 2B , 2A , 1C , 1B , 1A , start]

# {"Cmd":"form-submit","BusinessTag":"X5NXPTNGRG2H3","FormID":"1636","FormSubmissionID":"1709","FormData":{"start":null,"Patient name":"DWNWRDGBMWRBK","Test type":"Test 1","Expedite?":"true","Special Notes":"none","WorkflowID":"32"}}


    form_id = [1643, 1642, 1641, 1640, 1639, 1638, 1637, 1636]  #### these ids for DEV server

    # form_id = [1925,1926,1927]  ### these ids for test server
    for row in form_id:
        id = row
        body = {}
        url = BASE_URL + "submit_action/" + zviceID + "/form/" + str(id)
        method = "GET"
        jsonresponse = CM.hit_url_method(body, headers1, method, url)
    #    print jsonresponse

        for subac1 in json.loads(jsonresponse)['data']['ondemand_action']:
            data1 = subac1['data']
     #       print subac1['data']
            data1 = json.loads(subac1['data'])
            c = 0
            for element in data1['Elements'][0]['Elements']:
                # if element['ElementID'] == "Work FlowId":
                if element['ElementID'] == "WorkflowID":
      #              print "found element"
                    data1['Elements'][0]['Elements'][c]["Value"] = a
                c = c + 1
       #         print "Element position: " + str(c)
        body = data1
        method = subac1['method']
        url = subac1['actionUrl']
        jsonresponse = CM.hit_url_method(body, headers1, method, url)
      #  print jsonresponse

def publish_submission(submission_id):
    url = "http://www.twig-me.com/v8/formsubmission/X5NXPTNGRG2H3/publish/" + submission_id
    method = "POST"
    body = {}
    body['Flags'] = "true"
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

#*************************  this part is giving us Form card id and form submission id related to this work flow
def get_submission_id(w_ID):
    body = {}
    method = "GET"
    url = "http://www.twig-me.com/v11/X5NXPTNGRG2H3/forms/submissions/workflow/" + w_ID
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

if __name__ == "__main__":
    BASE_URL = "http://twig-me.com/v8/"  ### dev server
    zviceID = "X5NXPTNGRG2H3"  # Work flow demo department
    email = "admin@zestl.com"
    pwd = "TwigMeNow"
    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
#*******************  this will take input from PHP   ****************
    # try :
    body = json.loads(sys.argv[1])
    with open("/tmp/o.txt", 'a') as wf:
        wf.write("i was here\n")
        wf.write(sys.argv[1])
    # except:
    #     print "Something went wrong"
    #     sys.exit(1)

    # body = {}
    # body['Cmd'] = 'workflow-create'                        # String, should be used to switch execution in python script
    # body['BusinessTag'] = "A4CJTF34DSDS"               # Business Encrypted Tag
    # body['WorkflowID'] = 3                      # Integer
    # body['WorkflowTypeID'] = 2                  #Integer
    # body['WorkflowTitle'] = "august"               #String
#*****************************************************************************************


#**************  Pushkar sir will send body for this   ***************
    # body = {}
    # body['Cmd'] = 'form-submit' #String, should be used to switch execution in python script
    # body['BusinessTag'] = "A4CJ2VHTTJS9Y"
    # body['FormID'] = 1636       # Generate Report form card ID
    # body['FormSubmissionID'] = 1651
    # content = {}
    # content['Patient name'] = "ABC"
    # content['Test type'] = "Test 3"
    # content['Expedite?'] = "true"
    # content['Special Notes'] = "DEF"
    # content['WorkflowID'] = 2
    # body['FormData'] = content
# {"Cmd":"form-submit","BusinessTag":"X5NXPTNGRG2H3","FormID":"1636","FormSubmissionID":"1709","FormData":{"start":null,"Patient name":"DWNWRDGBMWRBK","Test type":"Test 1","Expedite?":"true","Special Notes":"none","WorkflowID":"32"}}
    try:
        w_ID = body['FormData']['WorkflowID']
        # w_ID = 21
        w_ID = str(w_ID)
    except:
        w_ID = 0

    if body['Cmd'] == "workflow-create" and body['BusinessTag'] == "A4CJ2VHTTJS9Y":
        result = submit_form(body['WorkflowID'])

    d = {'Test 1' : 1637 , 'Test 2' : 1640 , 'Test 3' : 1642}
    if body['Cmd'] == "form-submit" and body['BusinessTag'] == "X5NXPTNGRG2H3":
        result_1 = get_submission_id(w_ID)
        print result_1
        for sub_id in json.loads(result_1)['data']['matchedRows']:
          #  print sub_id['FormID']
            for k,v in d.items():
                if body['FormData']['Test type'] == k:
                    if v == sub_id['FormID']:
                        submission_id = sub_id['FormSubmissionID']
                        submission_id = str(submission_id)
                        result = publish_submission(submission_id)
                        output = {}
                        output['FormID'] = sub_id['FormID']
                        output['FormSubmissionID'] = sub_id['FormID']
                        output['BusinessTag'] = 'X5NXPTNGRG2H3'
                        print json.dumps(output)
