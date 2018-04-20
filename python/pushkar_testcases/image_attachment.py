import logon as LL
import common as CM
import base64
import info as info
import requests

BASE_URL = info.url
email = info.email
pwd = info.pwd

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
#*******************   Code for attachment on all Cards who support attachment **************

def attach(f_name,cardID,ext,bID,typ):
    fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/TEST_ATTACHMENT/" + f_name
    method = "POST"
    url = BASE_URL + "cards/" + cardID + "/attachment/" + bID
    print url
    with open(fname, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string = encoded_string.encode('utf8')

    typ = typ    ### please write "image" if u write "img" then it will not work
    body = {}
    body['media_name'] = f_name
    body['media'] = encoded_string
    body['media_type'] = typ
    body['media_ext'] = ext
    body['media_size'] = 120000
    body['media_compressed'] = True
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

#************** Upload Images To Gallery *************#
def gallery_upload(f_name,cardID,ext,bID,typ,caption):
    fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/TEST_ATTACHMENT/" + f_name
    method = "POST"
    url = BASE_URL + bID + "/gallery/" + cardID + "/image"
    print url
    with open(fname, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string = encoded_string.encode('utf8')

    typ = typ    ### please write "image" if u write "img" then it will not work
    body = {}
    body['media_name'] = f_name
    body['media'] = encoded_string
    body['media_type'] = typ
    body['media_ext'] = ext
    body['media_size'] = 120000
    body['media_caption'] = caption
    body['media_compressed'] = True
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

#**************  Add Attachment in chating  box ************//////////

def image_attachment_chatbox(f_name,ext,typ):

    fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/TEST_ATTACHMENT/" + f_name
    # method = "POST"
    # url = "http://35.154.64.11/v7/forum/" + bID + "/comments/" + cardID
    # print url
    with open(fname, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string = encoded_string.encode('utf8')

    att1 = {}
    typ = typ
    att1['media_name'] = f_name
    att1['media'] = encoded_string
    att1['media_type'] = typ
    att1['media_ext'] = ext
    att1['media_size'] = 120000
    att1['media_compressed'] = True
    return att1

def try1(att2,bID,cardID,text):

    body = {}
    body['media'] = att2
    body['Text'] = text
    method = "POST"
    url = BASE_URL + "forum/" + bID + "/comments/" + cardID
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

#*********** Form and TEXT card Backgroud colour  ***********************#
def form_text_background(f_name,cardID,ext,bID,typ):
    fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/TEST_ATTACHMENT/" + f_name
    method = "POST"
    url = BASE_URL + "cards/" + cardID + "/bgimage/" + bID
    print url
    with open(fname, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string = encoded_string.encode('utf8')

    typ = typ    ### please write "image" if u write "img" then it will not work
    body = {}
    body['media_name'] = f_name
    body['media'] = encoded_string
    body['media_type'] = typ
    body['media_ext'] = ext
    body['media_size'] = 120000
    body['remove'] = False
    body['media_compressed'] = True
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

#*********** FORUM card Backgroud colour  ***********************#
def forum_background(f_name,cardID,ext,bID,typ,title):
    fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/TEST_ATTACHMENT/" + f_name
    method = "PUT"
    url = BASE_URL + "forum/" + bID + "/" + cardID
    print url
    with open(fname, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string = encoded_string.encode('utf8')

    typ = typ    ### please write "image" if u write "img" then it will not work
    body = {}
    body['media_name'] = f_name
    body['media'] = encoded_string
    body['media_type'] = typ
    body['media_ext'] = ext
    body['media_size'] = 120000
    body['remove'] = False
    body['media_compressed'] = True
    body['Text'] = title
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

#*********** Gallery card Backgroud colour  ***********************#
def Gallery_background(f_name,cardID,ext,bID,typ,title):
    fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/TEST_ATTACHMENT/" + f_name
    method = "PUT"
    url = BASE_URL + bID + "/gallery/" + cardID
    print url
    with open(fname, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string = encoded_string.encode('utf8')

    typ = "img/jpg"    ### please write "image" if u write "img" then it will not work
    body = {}
    body['media_name'] = f_name
    body['media'] = encoded_string
    body['media_type'] = typ
    body['media_ext'] = ext
    body['media_size'] = 120000
    body['remove'] = False
    body['media_compressed'] = True
    body['Title'] = title
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

#*********** Calendar card Backgroud colour  ***********************#
def Calendar_background(f_name,cardID,ext,bId,typ,title):
    fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/TEST_ATTACHMENT/" + f_name
    method = "PUT"
    url = BASE_URL + bId + "/calendars/" + cardID
    print url
    with open(fname, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string = encoded_string.encode('utf8')

    typ = typ    ### please write "image" if u write "img" then it will not work
    body = {}
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_EDIT_CALENDAR"
    body['categorytype'] = "Calendar"
    r = requests.get("http://twig.me/v1/push/dectest/" + bId)
    tagnum = r.json()['decTagID']
    print tagnum
    body['ZviceID'] = tagnum
    body['LinkType'] = "CALENDAR"
    body['DefaultView'] = "Calendar View"
    body['CalendarID'] = cardID
    body['media_name'] = f_name
    body['media'] = encoded_string
    body['media_type'] = typ
    body['media_ext'] = ext
    body['media_size'] = 120000
    body['remove'] = False
    body['media_compressed'] = True
    body['Title'] = title
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

#*********** Attendace card Backgroud colour  ***********************#
def Attendance_background(f_name,cardID,ext,bID,typ,title):
    fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/TEST_ATTACHMENT/" + f_name
    method = "PUT"
    url = BASE_URL + bID + "/fastscan/attendance/" + cardID
    print url
    with open(fname, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string = encoded_string.encode('utf8')

    typ = typ    ### please write "image" if u write "img" then it will not work
    body = {}
    body['FSCardID'] = bID
    body['ScanType'] = "FAST"
    body['MembershipPlanID'] = "NONE"
    body['media_name'] = f_name
    body['media'] = encoded_string
    body['media_type'] = typ
    body['media_ext'] = ext
    body['media_size'] = 120000
    body['remove'] = False
    body['media_compressed'] = True
    body['Title'] = title
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

#*********** Location Track card Backgroud colour  ***********************#
def Location_track_background(f_name,cardID,ext,bID,typ,title):
    fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/TEST_ATTACHMENT/" + f_name
    method = "PUT"
    url = BASE_URL + "lt/" + bID + "/" + cardID
    print url
    with open(fname, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string = encoded_string.encode('utf8')

    typ = typ    ### please write "image" if u write "img" then it will not work
    body = {}
    body['LTCardID'] = cardID
    body['UserIDList'] = ""
    body['AuthorID'] = 3122
    body['media_name'] = f_name
    body['media'] = encoded_string
    body['media_type'] = typ
    body['media_ext'] = ext
    body['media_size'] = 120000
    body['remove'] = False
    body['media_compressed'] = True
    body['Title'] = title
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

#*********** Base card Backgroud Image  ***********************#
def Department_background(f_name,ext,bID,typ,title):
    fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/TEST_ATTACHMENT/" + f_name
    method = "POST"
    url = BASE_URL + "zvice/interaction/" + bID
    print url
    with open(fname, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    encoded_string = encoded_string.encode('utf8')

    typ = typ    ### please write "image" if u write "img" then it will not work
    body = {}
    body['media_name'] = f_name
    body['media'] = encoded_string
    body['media_type'] = typ
    body['media_ext'] = ext
    body['media_size'] = 120000
    body['remove'] = False
    body['media_compressed'] = True
    body['Title'] = title
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse