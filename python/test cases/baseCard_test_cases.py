import logon as LL
import common as CM
import info as info

BASE_URL = info.url

    ####  Business ID

email = info.email
pwd = info.pwd

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
def basecard(bName,desc,bId):
    zviceID = bId
    jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
    # fname = "C:/Users/User/Dropbox/Zestl-Deployment/minal/try.jpg"
    fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/minal 1/minal.jpg"

    for a in jsondata['data']['elements']:
        # cardtype = "basecard"
        cardtype = bName
        # if cardtype in a['cardtype']:
        if cardtype in a['title']:
            print "1st level"
            for b in a['actions']:

                ###############   To add Base card Image   #########
                title = "Upload"
                if title in b['title']:
                    print "2nd level"

                    # with open(fname, "rb") as fn:


                        # encoded_string = base64.b64encode(fn.read())
                    # encoded_string = encoded_string.encode('utf8')
                    # typ = "img/jpg"
                    body = {}
                    # body['media'] = encoded_string
                    # body['media_type'] = typ
                    # body['media_ext'] = "jpg"
                    # body['media_size'] = 120000
                    # body['media_name'] = "minal.jpg"
                    # body['Caption'] = "minal"
                    # body['Title'] = "Minal Test"
                    body['desc'] = desc
                    print body['desc']
                    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"
                    url = b['actionUrl']
                    method = "POST"
                    jsonresponse = CM.hit_url_method(body, headers1, method, url)
                    print jsonresponse