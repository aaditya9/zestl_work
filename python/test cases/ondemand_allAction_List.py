import logon as LL
import common as CM
import json

SERVER = "http://35.154.64.11/"
version = "v8/"
BASE_URL = SERVER + version

# zviceID = "876MD568TAUH2"
zviceID = "4X6WPSGA9E3N6" # dept
# zviceID = "CTYXZYKL7DPT4" # Lib
# zviceID = "7QLQDCME6EDVU" # one user

# email = "admin@zestl.com"
email = "sayali@zestl.com"
pwd = "zestl123"

def action_list(action):
    if action['actionType'] != "ON_DEMAND":
        return None
    else:
        url = action['actionUrl']
        method = action['method']
        body = action['data']
        jsonresponse = CM.hit_url_method_without_convesion(body, headers1, method, url)
        return jsonresponse

def sub_action_list(resoponse):
    if resoponse is None:
        print "Stop"
        return
    else:
        for subaction in json.loads(resoponse)['data']['ondemand_action']:
            print subaction['title']
            ef.write("All Action Level : ---   " + subaction['title'] + "\n")
            return

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
errorFile = "act.txt"
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    title = "Dpartment test test test"
    if title == a['title']:
        with open(errorFile, "a") as ef:
            for action in a['actions']:
                title = action['title']
                if title in action['title']:
                    ef.write("Base Level : ---   " + action['title'] + "\n")
                resoponse = action_list(action)
                if resoponse is None:
                    print "Stop"
                else:
                    for subaction in json.loads(resoponse)['data']['ondemand_action']:
                        print subaction['title']
                        ef.write("All Action Level : ---   " + subaction['title']+ "\n")

                        resoponse = action_list(subaction)
                        if resoponse is None:
                            print "Stop"
                        else:
                            for subaction1 in json.loads(resoponse)['data']['ondemand_action']:
                                print subaction['title']
                                ef.write("Inside Level : ---"+subaction['title']+"------"+ subaction1['title'] + "\n")

                                resoponse = action_list(subaction1)
                                if resoponse is None:
                                    print "Stop"


            # title = "All actions"
            # if title == action['title']:
            #     print "1----"
            #     body = {}
            #     url = action['actionUrl']
            #     method = action['method']
            #     jsonresponse = CM.hit_url_method(body, headers1, method, url)
            #     # print jsonresponse
            #     ef.write("\n")
            #     for subaction in json.loads(jsonresponse)['data']['ondemand_action']:
            #         # print subaction['title']
            #         ef.write("All Actions Level : ---   " + subaction['title'] + "\n")
            #
            #         title = "Settings"
            #         if title == subaction['title']:
            #             print "setting"
            #             body = {}
            #             url = subaction['actionUrl']
            #             method = subaction['method']
            #             jaction = CM.hit_url_method(body, headers1, method, url)
            #             # print jaction
            #
            #             ef.write("\n")
            #             for settings_actions in json.loads(jaction)['data']['ondemand_action']:
            #                 # print settings_actions['title']
            #                 ef.write("Settings Actions Level : ---   " + settings_actions['title'] + "\n")
            #
            #         # title = "User Permission Settings"
            #         elif title == subaction['title']:
            #             print "User Permission Settings"
            #             body = {}
            #             url = subaction['actionUrl']
            #             method = subaction['method']
            #             jaction = CM.hit_url_method(body, headers1, method, url)
            #             print jaction
            #
            #             ef.write("\n")
            #             for user_permission_actions in json.loads(jaction)['data']['ondemand_action']:
            #                 print user_permission_actions['title']
            #                 ef.write("User Permission Actions Level : ---   " + user_permission_actions['title'] + "\n")
            #
            #         title = "Message"
            #         if title == subaction['title']:
            #             print "Message"
            #             body = {}
            #             url = subaction['actionUrl']
            #             method = subaction['method']
            #             jaction = CM.hit_url_method(body, headers1, method, url)
            #             print jaction
            #
            #             ef.write("\n")
            #             for message in json.loads(jaction)['data']['ondemand_action']:
            #                 print message['title']
            #                 ef.write("Message Actions Level : ---   " + message['title'] + "\n")
            #
            #         title = "Add Card"
            #         if title == subaction['title']:
            #             print "Add Card"
            #             body = {}
            #             url = subaction['actionUrl']
            #             method = subaction['method']
            #             jaction = CM.hit_url_method(body, headers1, method, url)
            #             print jaction
            #
            #             ef.write("\n")
            #             for add_card in json.loads(jaction)['data']['ondemand_action']:
            #                 print add_card['title']
            #                 ef.write("All Cards Actions Level : ---   " + add_card['title'] + "\n")