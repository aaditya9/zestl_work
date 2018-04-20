import logon as LL
import common as CM
import json

SERVER = "http://35.154.64.11/"
version = "v8/"
BASE_URL = SERVER + version

zviceID = "876MD568TAUH2"

email = "minal@zestl.com"
pwd = "minal123"
fname = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Test_Case_files/try_1.txt"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
errorFile = "actions.txt"
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    with open(fname, 'r') as json_data:
        for line in json_data:
            d = json.loads(line)
            cmd = d['cmd']
            if cmd == a['title']:
                with open(errorFile, "a") as ef:
                    ef.write(d['cmd'] + "\n")
                    for action in a['actions']:
                        print action['title']
                        ef.write("Base Level : ---   " + action['title']+ "\n")

                    title = d['type']
                    if title == action['title']:
                        # print "1----"
                        body = {}
                        url = action['actionUrl']
                        method = action['method']
                        jsonresponse = CM.hit_url_method(body, headers1, method, url)
                        print jsonresponse
                        ef.write("\n")
                        for subaction in json.loads(jsonresponse)['data']['ondemand_action']:
                            ef.write("All Actions Level : ---   " + subaction['title'] + "\n")

                            if "User Permission Settings" == subaction['title']:
                                print "User Permission Settings"
                                body1 = subaction['data']
                                url = subaction['actionUrl']
                                method = subaction['method']
                                jaction = CM.hit_url_method_without_convesion(body1, headers1, method, url)
                                print jaction
                                ef.write("\n")
                                for user_permission_actions in json.loads(jaction)['data']['ondemand_action']:
                                    print user_permission_actions['title']
                                    ef.write("User Permission Actions Level : ---   " + user_permission_actions['title'] + "\n")

                            elif "Message" == subaction['title']:
                                print "Message"
                                body1 = subaction['data']
                                url = subaction['actionUrl']
                                method = subaction['method']
                                jaction = CM.hit_url_method_without_convesion(body1, headers1, method, url)
                                print jaction
                                ef.write("\n")
                                for message in json.loads(jaction)['data']['ondemand_action']:
                                    print message['title']
                                    ef.write("Message Actions Level : ---   " + message['title'] + "\n")

                            elif "Add Card" == subaction['title']:
                                print "Add Card"
                                body = {}
                                url = subaction['actionUrl']
                                method = subaction['method']
                                jaction = CM.hit_url_method(body, headers1, method, url)
                                print jaction
                                ef.write("\n")
                                for add_card in json.loads(jaction)['data']['ondemand_action']:
                                    print add_card['title']
                                    ef.write("All Cards Actions Level : ---   " + add_card['title'] + "\n")

                            elif "Settings" == subaction['title']:
                                print "setting"
                                body = {}
                                url = subaction['actionUrl']
                                method = subaction['method']
                                jaction = CM.hit_url_method(body, headers1, method, url)
                                ef.write("\n")
                                for settings_actions in json.loads(jaction)['data']['ondemand_action']:
                                    ef.write("Settings Actions Level : ---   " + settings_actions['title'] + "\n")