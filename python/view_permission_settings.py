import logon as LL
import common as CM
import json
import csv

SERVER = "http://twig.me/"
version = "v8/"
BASE_URL = SERVER + version
zviceID = "DU8BFMK4WUBZF"
email = "minal@zestl.com"
pwd = "minal123"
outfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/more_view.csv"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
#****************** CONTACT CARD *********************************************/
# url = "https://twig.me/v8/DU8BFMK4WUBZF/contacts/page"
# method = "POST"
# body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_CONTACT_DETAILS"}
# ja = CM.hit_url_method(body, headers1, method, url)
# print ja
#
# url = "https://twig.me/v8/card/get/permissions/DU8BFMK4WUBZF"
# method = "POST"
# body = {"cardType":"ContactCard","cardID":"","actionType":"VIEW"}
# ja = CM.hit_url_method(body, headers1, method, url)
# print ja
###################################################################################

#************************* MORE DETAILS CARD ***************************************#
    if "More Details" == a['title']:
        print "present"
        for action in a['actions']:
            if "Explore" in action['title']:
                body = {"interactionID": "CommonInteraction_INTERACTION_TYPE_SHOW_GENERIC_NOTES", "notetype": "P",
                        "useclubbing": "false"}
                url = action['actionUrl']
                print url
                method = "POST"
                ja = CM.hit_url_method(body, headers1, method, url)
                print ja
                url = "https://twig.me/v8/card/get/permissions/DU8BFMK4WUBZF"
                method = "POST"
                body = {"cardType":"GenericNotesCard","cardID":"","actionType":"VIEW"}
                ja = CM.hit_url_method(body, headers1, method, url)
                print ja

#****************************************************************
with open(outfile, 'w') as wf:
    for a in json.loads(ja)['data']['elements']:
        if "mastercard" in a['cardtype']:
            title = a['title']
            print title
            wf.write(zviceID + "," + title +"\n")

        elif "textcard" in a['cardtype']:
            title = a['title']
            print title
            if title != None:
                wf.write(zviceID + "," + title + "\n")
            else:print "none"