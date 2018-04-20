import logon as LL
import common as CM
import info as info
import requests

BASE_URL = info.url
email = info.email
pwd = info.pwd
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

def form_card(title,desc,user_tag,bId,parentCardID):
    r = requests.get("http://twig.me/v1/push/dectest/" + bId)
    tagnum = r.json()['decTagID']
    user_tag = r.json()['decTagID']
    body = {"FormTitle": title, "FormDescription": desc, "ZviceID": tagnum, "ZbotID": user_tag,
            "LinkType": "FORM", "parentCardID" : parentCardID}
    method = "POST"
    url = BASE_URL+ bId +"/forms"
    print url
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def text_card(tname,tdesc,bId,flag,parentCardID):
    body = {}
    if parentCardID != "":
        body['parentCardID'] = parentCardID

    body['cardData'] = {"title": tname, "desc": tdesc, "Flags": flag}
    body['cardType'] = "TEXT"
    body['opType'] = 1
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
    method = "POST"
    url = BASE_URL + "zvice/interaction/" + bId
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def forum_card(forum_name,bId,flag):
    body = {}
    body['Text'] = forum_name
    body['Flags'] = flag
    body['FlagsInside'] = False
    method = "POST"
    url = BASE_URL + "forum/" +bId
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def calendar_card(cal_name,desc,bId):
    body = {}
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_EDIT_CALENDAR"
    body['categorytype'] = "Calendar"
    body['CalendarID'] = ""
    r = requests.get("http://twig.me/v1/push/dectest/" + bId )
    tagnum = r.json()['decTagID']
    print tagnum
    body['ZviceID'] = tagnum
    body['LinkType'] = "CALENDAR"
    body['Title'] = cal_name
    body['Description'] = desc
    body['DefaultView'] = "List View"
    method = "POST"
    url = BASE_URL +bId +"/calendars/"
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def gallery_card(title,desc,bId):
    body = {}
    body['Title'] = title
    body['Description'] = desc
    body['Flags'] = False
    method = "POST"
    url = BASE_URL + bId + "/gallery"
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def locationTrack_card(title,desc,bId):
    body = {}
    body['Title'] = title
    body['Description'] = desc
    method = "POST"
    url = BASE_URL + "lt/add/" + bId
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def link_card(title,desc,bId,dlink):
    body = {}
    body['cardData'] = {"title": title, "desc": desc, "link": dlink}
    body['cardType'] = "LINK"
    body['opType'] = 1
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
    method = "POST"
    url = BASE_URL + "zvice/interaction/" + bId
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def attendance_card(title,desc,bId):
    body = {}
    body['Title'] = title
    body['Description'] = desc
    body['ScanType'] = "FAST"
    body['MembershipPlanID'] = "NONE"
    method = "POST"
    url = BASE_URL + "fastscan/attendance/" + bId
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def department(title,desc,bId,dept_tag,dept_type):
    body = {}
    body['title'] = title
    body['zviceinfo'] = desc
    body['zviceid'] = dept_tag
    body['zbotid'] = bId
    body['zvicetype'] = "ZTAG"
    body['zvicelink'] = "NEW"
    body['lat'] = "-"
    body['long'] = "-"
    body['zviceloc'] = "---"
    body['tagprofilestr'] = dept_type
    method = "PUT"
    # url = "http://35.154.64.11/v7/" + bId + "/register"
    url = BASE_URL + "zvice/register"
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def create_product_card(title,desc,bId):
    body = {}
    body['Title'] = title
    body['Description'] = desc
    method = "POST"
    url = BASE_URL + "carousel/products/add/" + bId
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction

def create_baner_card(title,desc,bId):
    body = {}
    body['Title'] = title
    body['Description'] = desc
    method = "POST"
    url = BASE_URL + "carousel/banner/add/" +bId
    jaction = CM.hit_url_method(body, headers1, method, url)
    return jaction
