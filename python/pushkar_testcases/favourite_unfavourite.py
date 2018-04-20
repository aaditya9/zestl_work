import logon as LL
import common as CM
import info as info

BASE_URL = info.url
email = info.email
pwd = info.pwd
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
def fav_unfav_action(bId, flag):
    body = {}
    body['currentvalue'] = flag  # **** put True value to favourite . and put False value to Unfavourite******
    method = "PUT"
    url = BASE_URL + "ztag/favourite/" + bId
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    print jsonresponse