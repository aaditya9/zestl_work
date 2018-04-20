import logon as LL
import common as CM
import info as info
import requests

BASE_URL = info.url
email = info.email
pwd = info.pwd
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

def form_card_delete(bId,Card_ID):
    body = {}
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_DELETE_FORM"
    body['FormID'] = Card_ID
    body['ZviceID'] = bId
    body['categorytype'] = "FormCard"
    method = "POST"
    url = BASE_URL + "archive/" + bId + "/forms/" + Card_ID
    print url
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def text_card_delete(bId,Card_ID):
    body = {}
    body['cardID'] = Card_ID
    body['opType'] = 2
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
    method = "POST"
    url = BASE_URL + "archive/" + bId + "/textcard/" + Card_ID
    print url
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def text_card_delete(bId,Card_ID):
    body = {}
    body['cardID'] = Card_ID
    body['opType'] = 2
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
    method = "POST"
    url = BASE_URL + "archive/" + bId + "/textcard/" + Card_ID
    print url
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def forum_card_delete(bId,Card_ID):
    body = {}
    method = "POST"
    url = BASE_URL + "forum/" + bId + "/archive/" + Card_ID
    print url
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def LOcation_card_delete(bId,Card_ID):
    body = {}
    body['LTCardID'] = Card_ID
    method = "POST"
    url =  BASE_URL + "lt/" + bId + "/delete/" + Card_ID
    print url
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def link_card_delete(bId,Card_ID):
    body = {}
    body['cardID'] = Card_ID
    body['opType'] = 2
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
    method = "POST"
    url =  BASE_URL + "archive/" + bId + "/link/" + Card_ID
    print url
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def calendar_card_delete(bId,Card_ID):
    body = {}
    r = requests.get("http://twig.me/v1/push/dectest/" + bId)
    tagnum = r.json()['decTagID']
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_DELETE_CALENDAR"
    body['CalendarID'] = Card_ID
    body['ZviceID'] =tagnum
    body['categorytype'] = "CalendarCard"
    method = "POST"
    url =  BASE_URL +"archive/" + bId + "/calendars/" + Card_ID
    print url
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def gallery_card_delete(bId,Card_ID):
    body = {}
    body['GalleryID'] = Card_ID
    method = "POST"
    url =  BASE_URL + "archive/" + bId + "/gallery/" + Card_ID
    print url
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def attendance_card_delete(bId,Card_ID):
    body = {}
    body['FSCardID'] = Card_ID
    method = "POST"
    url =  BASE_URL + "archive/" + bId + "/fastscan/attendance/" + Card_ID
    print url
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def banner_card_delete(bId,Card_ID):
    body = {}
    body['CardID'] = Card_ID
    method = "POST"
    url =  BASE_URL + "carousel/banner/" + bId + "/delete/" + Card_ID
    print url
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def product_card_delete(bId,Card_ID):
    body = {}
    body['CardID'] = Card_ID
    method = "POST"
    url =  BASE_URL + "carousel/products/" + bId + "/delete/" + Card_ID
    print url
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction