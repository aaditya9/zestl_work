import logon as LL
import common as CM
import json
SERVER = "http://35.154.64.11/"
version = "v5/"
BASE_URL = SERVER + version
#
# zviceID = "876MD568TAUH2"    ####  Business ID
#
email = "admin@zestl.com"
pwd = "TwigMeNow"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

########  code for create user group  ########
def create_user_group(jsonresponse):
    for sub in json.loads(jsonresponse)['data']['elements']:
        title = "User Groups"
        if title == sub['content']:
            print "4rth level"
            for sub1 in sub['actions']:
                title = "Add New Group"
                if title in sub1['title']:
                    print "5th level"
                    method = "POST"
                    url = sub1['actionUrl']
                    body = {}
                    body['groupName'] = "pushakar test"
                    body['groupDesc'] = "pushakar"
                    jsonresponse1 = CM.hit_url_method(body, headers1, method, url)
                    return jsonresponse1

 ###############  code for deleting the user group  #############
def delete_user_group(jsonresponse):
    for sub in json.loads(jsonresponse)['data']['elements']:
        title = "Lankesh test"
        if title == sub['title']:
            print "found group name"
            for sub1 in sub['actions']:
                title = "Delete Group sayali test"
                if title == sub1['title']:
                    print "ready to delete"
                    method = "POST"
                    url = sub1['actionUrl']
                    body = {}
                    jsonresponse1 = CM.hit_url_method(body, headers1, method, url)
                    return jsonresponse1

#########  Code for Editing the user group Name  ########
def edit_name_userGroup(jsonresponse):
    for sub in json.loads(jsonresponse)['data']['elements']:
        title = "sayali test"
        if title == sub['title']:
            print "found group name"
            for sub1 in sub['actions']:
                title = "Edit Group Name"
                if title == sub1['title']:
                    print "ready to Edit"
                    method = "PUT"
                    url = sub1['actionUrl']
                    body = {}
                    body['groupName'] = "Lankesh test"
                    body['groupDesc'] = "minal"
                    jsonresponse1 = CM.hit_url_method(body, headers1, method, url)
                    return jsonresponse1

############### Code for  sending Mail ###########
def mail_mail(jsonresponse):
    for sub in json.loads(jsonresponse)['data']['elements']:
        title = "Sujoy test"
        if title == sub['title']:
            print "found group name"
            for sub1 in sub['actions']:
                title = "Message"
                if title == sub1['title']:
                    print "ready to send message"
                    for sub2 in sub1['actions']:
                        title = "Mail"
                        if title == sub2['title']:
                            print "I am sending Mail"
                            method = "POST"
                            url = sub2['actionUrl']
                            body = {}
                            body['commtype'] = "MAIL"
                            body['title'] = "birthday party"
                            body['msg'] = "all r invited for my birthday party"
                            jsonresponse1 = CM.hit_url_method(body, headers1, method, url)
                            return jsonresponse1

################  Code for Notifyyy  #########
def mail_notify(jsonresponse):
    for sub in json.loads(jsonresponse)['data']['elements']:
        title = "Sujoy test"
        if title == sub['title']:
            print "found group name"
            for sub1 in sub['actions']:
                title = "Message"
                if title == sub1['title']:
                    print "ready to send message"
                    for sub2 in sub1['actions']:
                        title = "Mail"
                        if title == sub2['title']:
                            print "I am sending Notification"
                            method = "POST"
                            url = sub2['actionUrl']
                            body = {}
                            body['commtype'] = "NOTIFY"
                            body['title'] = "birthday party"
                            body['msg'] = "all r invited for my birthday party"
                            jsonresponse1 = CM.hit_url_method(body, headers1, method, url)
                            print jsonresponse1
                            return jsonresponse1

############  Code for sending Message   ##########
def mail_message(jsonresponse):
    for sub in json.loads(jsonresponse)['data']['elements']:
        title = "Sujoy test"
        if title == sub['title']:
            print "found group name"
            for sub1 in sub['actions']:
                title = "Message"
                if title == sub1['title']:
                    print "ready to send message"
                    for sub2 in sub1['actions']:
                        title = "Mail"
                        if title == sub2['title']:
                            print "I am sending SMS"
                            method = "POST"
                            url = sub2['actionUrl']
                            print sub2['actionUrl']
                            body = {}
                            body['commtype'] = "SMS"
                            body['title'] = "birthday party"
                            body['msg'] = "all r invited for my birthday party"
                            jsonresponse1 = CM.hit_url_method(body, headers1, method, url)
                            return jsonresponse1