
import requests
import urllib
import json
import time

import hashlib
import csv

akey = 'dfd8f390c6cbd8fd95c34f79aa4a9480eff582befdb1d86f0027d2703de42996d230fed3ae4c2bb59a7995d9a99c390acbee86d1fd86f20dfb72f81e0a4e5a68'
hasec = '984e6a3c9253b494d96ee364efa203d306e88b180d9c630711d4f07ce787d7ed79df0a28adc0ed5de9c8e353b4110b4f181796b563ea9776d05730399a528e3a'



def login_user(email, pwd, BASE_URL):
    sha512pwd = hashlib.sha512(pwd).hexdigest()
    sha512apwd = hashlib.sha512(akey + hasec + email + sha512pwd).hexdigest()
    payload = {'email': email, 'password': sha512pwd}
    header = {'AKEY': akey, 'APWD': sha512apwd}
    jsonreply = invoke_rest('POST', BASE_URL + 'user/login', payload, header)
    # print jsonreply
    return jsonreply


def getMPWD(authkey_salt, timestamp, pwd):
    sha512pwd = hashlib.sha512(pwd).hexdigest()
    hpwd = hashlib.sha512(sha512pwd + authkey_salt).hexdigest()
    mpwd = hashlib.sha512(hpwd + str(timestamp) + hasec).hexdigest()
    return mpwd


def invoke_rest(request_type, rest_url, payload=None, headers=None):
    count = 1
    while True:
        try:
            api_url = rest_url
            if request_type == 'GET':
                r = requests.get(api_url, headers=headers)

                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            elif request_type == 'POST':
                r = requests.post(api_url, data=payload, headers=headers)
                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            elif request_type == 'PUT':
                r = requests.put(api_url, data=payload, headers=headers)
                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            else:
                return "Invalid request type ", request_type
        except Exception, e:
            print "Error in invoking " + request_type + ", " + api_url + ", Reattempting " + str(count)
            count = count + 1
            time.sleep(50.0 / 1000.0);  # Sleep 50 milli sec
            # return "Exception:", e, " in getting the API call"



def req_headers(email, pwd, BASE_URL):
    BASE_URL = BASE_URL
    email = email
    pwd = pwd
    jsondata = login_user(email, pwd, BASE_URL)
    if jsondata['code'] == 200:
        try:
            reply = jsondata['reply']
            json_reply = json.loads(reply)
            loginToken = json_reply['loginToken']
            authorization = json_reply['AuthKey']
            timestamp = int(time.time())
            mpwd = getMPWD(authorization, timestamp, pwd)


            headers = {'Authorization': authorization, 'LoginToken': loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey,
                   'MPWD': mpwd}
            headers1 = {'Content-type': 'application/json;charset=UTF-8', 'Authorization': authorization,
                    'LoginToken': loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey, 'MPWD': mpwd}
            return (headers, headers1)
        except KeyError:
            return (None, None)
    else:
        return (None, None)

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']



if __name__ == '__main__':

    adminemail = ""
    # BASE_URL = "http://twig-me.com/v1/"
    BASE_URL = "https://www.twig.me/v7/"  ### Production
    # BASE_URL = "http://35.154.64.11/v5/"    ###Test
    email = 'admin@zestl.com'

    passkey = 'Zspladmin99'

    ZbotID = "8SFKZCV5PFAXV"

    # inputFile = "C:/Users/user/Dropbox/Zestl-scripts/python/tmpfile"
    inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/date_check.csv"

    createNewUser = "N"

    uploadpicture = "N"

    tagCol = 0
    NameCol = -1
# <<<<<<< HEAD
    emailCol = -1
    descCol = -1
    useAdminLink = "Y"
    hasHeader = "Y"
    media = ""
    media_size = 0
    photo = -1


    hasmoredetails = "N"
    mobColumn = 5

    hasnotes = "Y"

# <<<<<<< HEAD
# =======
#     hasnotes = "N"
# >>>>>>> 759a935472b9a1a42258b58d29b5482a44fff032
    notename = [None] * 20
    noteCol = [None] * 20
    noOfNotes = 3

    notename[0] = "Date_sayali"
    noteCol[0] = 1
    notename[1] = "end date_sayali"
    noteCol[1] = 2
    notename[2] = "start Date_minal"
    noteCol[2] = 3

    # login
    headers, headers1 = req_headers(email, passkey, BASE_URL)

    body = {}
    body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat',
            'long': 'long',  'tagprofile': 0, 'media_type': 'image/jpg',
    'media_ext': 'jpg', 'media': media, 'media_size': media_size, 'zbotid': ZbotID}

    ### input management
    with open(inputFile, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        if hasHeader == "Y":
            row1 = data.next()
        method = "POST"

        counter = 0
        for row in data:

            counter += 1
            print counter
            zviceID = row[tagCol]
            if uploadpicture == "Y":
                url = BASE_URL + 'zvice/interaction/' + zviceID
                # body = {"moreInfo": {"Mobile number": mobile},
                body = {"interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
                if NameCol > -1 :
                    title = row[NameCol]
                    body["title"] = title
                if descCol > -1 :
                    desc = row[descCol]
                    body["desc"] = desc
                if photo > -1:
                    media = row[photo]
                    body["profilepic"] = media
                jsonreply = hit_url_method(body, headers1, method, url)
                print jsonreply

            if hasmoredetails == "Y":
                body = {}
                if mobColumn == -1:
                    mobile = ''

                else:
                    mobile = row[mobColumn]
                    body["Contact"] = mobile
                method = "POST"
                if emailCol == -1:
                    email = ""
                else:
                    body["EmailID"] = row[emailCol]

                url = BASE_URL + 'zvice/interaction/' + zviceID
                # body = {"moreInfo": {"Mobile number": mobile},
                # body = { "interactionID": "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
                # if photo > -1:
                #     body["profilepic"] =  media
                # jsonreply = hit_url_method(body, headers1, method, url)
                # print jsonreply
                body["interactionID"] = "CommonInteraction_INTERACTION_TYPE_MODIFY_CONTACT_INFO"
                jsonreply = hit_url_method(body, headers1, method, url)
                time.sleep(500.0 / 1000.0);
                print jsonreply

            if hasnotes == "Y":
                method = "PUT"
                url = BASE_URL + 'ztag/notes_PP/' + zviceID
                for i in range(0, noOfNotes):
                    if noteCol[i] == -1 :
                        note = ""
                    else:
                        note = row[noteCol[i]]

                    tagNote = {"NoteHeader": notename[i], "Note": note};
                    body = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes': json.dumps(tagNote)}
                    jsonreply = hit_url_method(body, headers1, method, url)
                    print jsonreply