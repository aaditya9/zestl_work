import common as CM
import logon as LL
import json

BASE_URL = "http://twig-me.com/v13/"  ### dev server
# BASE_URL = "https://future.twig.me/v13/"
email = "admin@zestl.com"
pwd = "TwigMeNow"
# zviceID = "WHGJ7HTVTDFH3"
zviceID = "WKMUYXELA9LCC"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

def unhide_card(headers1,BASE_URL,zviceID,c_name):
    url = BASE_URL + "zvice/interaction/" + zviceID
    method = "POST"
    body = {"interactionID": "INTERACTION_TYPE_GET_CONFIG_CARDS"}
    elements = []
    jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
    elements = CM.unpaginate(jsondata['data']['elements'], elements, headers1)
    for el in elements:
        if el['title'] == c_name:
            el[
                'hidden'] = False  # IF U want to hide the cards then falg is TRUE. AND if u want to show the cards then flag is FALSE
    body = {}
    body['customcards'] = elements
    body['applyforall'] = False
    method = "POST"
    url = BASE_URL + "zvice/interaction/" + zviceID
    method = "POST"
    body["interactionID"] = "INTERACTION_TYPE_SET_CONFIG_CARDS"
    body['custom_theme'] = jsondata['data']['custom_theme']
    jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
    print jsondata
    url = BASE_URL + "zvice/interaction/" + zviceID
    method = "POST"
    body = {"interactionID": "INTERACTION_TYPE_GET_CONFIG_CARDS"}
    jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
    return jsondata



# card_Name = "Milestone Estimate Time form"
card_Name = "164"
result = unhide_card(headers1, BASE_URL, zviceID, card_Name)
print result