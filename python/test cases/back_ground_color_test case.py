import logon as LL
import common as CM
import base64



SERVER = "http://35.154.64.11/"
version = "v5/"
BASE_URL = SERVER + version

zviceID = "876MD568TAUH2"    ####  Business ID

email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
# fname = "C:/Users/User/Dropbox/Zestl-Deployment/minal/try.jpg"
fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/minal 1/minal.jpg"

for a in jsondata['data']['elements']:
    cardtype = "basecard"
    # cardtype = "Minal Test"
    if cardtype in a['cardtype']:
    # if cardtype in a['title']:
        print "1st level"
        for b in a['actions']:
            title = "Add Cards"
            if title in b['title']:
                print "2nd level"
                for c in b['actions']:
                    title = "Background Image"
                    if title in c['title']:
                        print "3rd level"
                        with open(fname, "rb") as fn:
                            encoded_string = base64.b64encode(fn.read())
                        encoded_string = encoded_string.encode('utf8')
                        typ = "image/jpg"    ### please write "image" if u write "img" then it will not work
                        body = {}
                        body['media'] = encoded_string
                        body['media_type'] = typ
                        body['media_ext'] = "JPG"
                        body['media_size'] = 120000
                        body['remove'] = "false"
                        body['media_compressed'] = True
                        body['pallete'] = ""   #### if u want to set only color then put here color code
                        body['interactionID'] = "CommonInteraction_INTERACTION_UPLOAD_BGIMG_ORG"
                        url = c['actionUrl']
                        method = "POST"
                        jsonresponse = CM.hit_url_method(body, headers1, method, url)
                        print jsonresponse