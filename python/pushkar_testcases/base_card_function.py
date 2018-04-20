import logon as LL
import common as CM
import info as info

BASE_URL = info.url
email = info.email
pwd = info.pwd

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
def basecard(desc, bId):

    body = {}
    body['desc'] = desc
    # body['Title'] = title
    print body['desc']
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"
    url = "http://35.154.64.11/v5/zvice/interaction/" + bId
    method = "POST"
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    print jsonresponse