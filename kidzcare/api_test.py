
import login1 as LL
import json
zbotID="WH4ULS9BHSAKZ"

headers, headers1 = LL.req_headers()


def hit_url_method(body, headers, BASE_URL,method):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    print(jsondata)
    return jsondata['reply']

actionUrl = LL.BASE_URL + "zvice/interaction/" + zbotID
method = "POST"
responseBody = {'username': '', 'expired' : 'false', 'interactionID' : 'CommonInteraction_INTERACTION_TYPE_SEARCH_LIB_USER_PROFILE', "pagesize" : 5000}

jsondata = hit_url_method(responseBody, headers1, actionUrl, method)


for a in json.loads(jsondata)['data']['elements']:
    if 'AKASH'== a['title']:
        tagid=a['tagId']
        print tagid
