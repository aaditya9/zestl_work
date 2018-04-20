import logon as LL
import common as CM
import info as info
import requests

BASE_URL = info.url
email = info.email
pwd = info.pwd
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

def forum_card_edit(bId,title,Card_ID):
    body = {}
    body['Text'] = title
    body['remove'] = "false"
    method = "PUT"
    url = BASE_URL + "forum/" + bId + "/" + Card_ID
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def text_card_edit(bId,title,Card_ID,desc):
    body = {}
    body['cardData'] = {"title" : title, "desc" : desc, "Flags" : "false"}
    body['CardID'] = Card_ID
    body['opType'] = 3
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
    body['FlagsInsideOld'] = "false"
    method = "POST"
    url = BASE_URL + "textcard/edit/" + bId
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def calendar_card_edit(bId,title,Card_ID,desc):
    body = {}
    r = requests.get("http://twig.me/v1/push/dectest/" + bId)
    tagnum = r.json()['decTagID']
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_EDIT_CALENDAR"
    body['categorytype'] = "Calendar"
    body['CalendarID'] = Card_ID
    body['ZviceID'] = tagnum
    body['LinkType'] = "CALENDAR"
    body['Title'] = title
    body['Description'] = desc
    body['remove'] = "false"
    method = "PUT"
    url = BASE_URL + bId + "/calendars/" + Card_ID
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def gallery_card_edit(bId,title,Card_ID,desc):
    body = {}
    body['GalleryID'] = Card_ID
    body['Title'] = title
    body['Description'] = desc
    body['remove'] = "false"
    method = "PUT"
    url = BASE_URL + bId + "/gallery/" + Card_ID
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def contact_detail_card_edit(bId,title,desc):
    body = {}
    # body['params'].body['ContactCard'] = {"title" : title, "desc" : desc}
    # body['title'] = title
    # body['subtitle'] = desc
    body['remove_image'] = "false"
    body['paramtype'] = 1
    method = "PUT"
    url = BASE_URL + "zvice/customparams/" + bId
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def location_card_edit(bId,title,Card_ID,desc):
    body = {}
    body['LTCardID'] = Card_ID
    body['UserIDList'] = ""
    body['remove'] = "false"
    body['AuthorID'] = 3211
    body['Title'] = title
    body['Description'] = desc
    method = "PUT"
    url = BASE_URL + "lt/" + bId +"/" + Card_ID
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def link_card_edit(bId,title,Card_ID,desc):
    body = {}
    body['cardData'] = {"title" : title , "link" : desc}
    body['cardID'] = Card_ID
    body['opType'] = 3
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
    method = "POST"
    url = BASE_URL + "zvice/interaction/" + bId
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def baner_card_edit(bId,title,Card_ID,desc):
    body = {}
    body['Title'] = title
    body['CardID'] = Card_ID
    body['Description'] = desc
    method = "PUT"
    url = BASE_URL + "carousel/banner/" + bId + "/" + Card_ID
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def product_card_edit(bId,title,Card_ID,desc):
    body = {}
    body['Title'] = title
    body['CardID'] = Card_ID
    body['Description'] = desc
    method = "PUT"
    url = BASE_URL + "carousel/products/" + bId + "/" + Card_ID
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction


def attendance_card_edit(bId,title,Card_ID,desc):
    body = {}
    body['FSCardID'] = Card_ID
    body['Title'] = title
    body['Description'] = desc
    body['ScanType'] = "FAST"
    body['MembershipPlanID'] = None
    body['remove'] = "false"
    method = "PUT"
    url = BASE_URL + bId + "/fastscan/attendance/" + Card_ID
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction