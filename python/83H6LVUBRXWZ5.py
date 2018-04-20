import time
import hashlib
import json
import logon as LL
import common as CM
import csv

akey = 'dfd8f390c6cbd8fd95c34f79aa4a9480eff582befdb1d86f0027d2703de42996d230fed3ae4c2bb59a7995d9a99c390acbee86d1fd86f20dfb72f81e0a4e5a68'
hasec = '984e6a3c9253b494d96ee364efa203d306e88b180d9c630711d4f07ce787d7ed79df0a28adc0ed5de9c8e353b4110b4f181796b563ea9776d05730399a528e3a'


def login_user(email, pwd, BASE_URL):
    sha512pwd = hashlib.sha512(pwd).hexdigest()
    sha512apwd = hashlib.sha512(akey + hasec + email + sha512pwd).hexdigest()
    payload = {'email': email, 'password': sha512pwd}
    header = {'AKEY': akey, 'APWD': sha512apwd}
    jsonreply = CM.invoke_rest('POST', BASE_URL + 'user/login', payload, header)
    # print jsonreply
    return jsonreply

def getMPWD(authkey_salt, timestamp, pwd):
    sha512pwd = hashlib.sha512(pwd).hexdigest()
    hpwd = hashlib.sha512(sha512pwd + authkey_salt).hexdigest()
    mpwd = hashlib.sha512(hpwd + str(timestamp) + hasec).hexdigest()
    return mpwd

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


def add_users_in_bulk(body, w_ID, zviceID, headers1, BASE_URL):
    hasHeader = "Y"
    csvFile = body['FormData']['File Name']
    print csvFile
    Business_ID = str(body['BusinessTag'])
    inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/" + csvFile + ".csv"
    # errorFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
    with open(inputFile, 'r') as rf:
        d_reader = csv.DictReader(rf)
        top_headers = d_reader.fieldnames
        # counter = 0
        for line in d_reader:
            # print(line['Name'])
        # data = csv.reader(rf, delimiter=',')
        # if hasHeader == "Y":
        #     row1 = data.next()

        #
        # for row in data:
        #     counter += 1
            name = line['NAME'].strip()
            desc = line['DESC'].strip()
            email_ID = line['EMAIL_ID']
            # method = "POST"
            # url = BASE_URL + 'zvice/interaction/' + Business_ID
            # body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat','long': 'long', 'tagprofile': 0, 'media_type': 'image/jpg','media_ext': 'jpg', 'media': "", 'media_size': 0, 'zbotid': Business_ID}
            # body['title'] = name
            # body['linkemail'] = email_ID
            # body['zviceinfo'] = desc
            # body['autogentag'] = "true"
            # body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"
            # jsonreply = CM.hit_url_method(body, headers1, method, url)
            # print jsonreply
            # jsonreply = json.loads(result)
            # user_id = jsonreply['data']['usertagid']

            # for hrd in top_headers:
            #     if hrd == "NAME" or hrd == "EMAIL_ID" or hrd == "GROUP":
            #         print "found"
            #     else:
            #         key = hrd
            #         val= line[hrd]
            #         print key
            #         print val
            #         method = "PUT"
            #         url = BASE_URL + 'ztag/notes_PP/' + zviceID
            #         tagNote = {"NoteHeader": key, "Note": val};
            #         body = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes','tagnotes': json.dumps(tagNote)}
            #         jsonreply = CM.hit_url_method(body, headers1, method, url)
            #         print jsonreply

            # grp_name = line['GROUP']
            # g_ID = CM.find_out_grp_ID(grp_name,headers1,Business_ID,BASE_URL)
            # result = CM.add_user_to_group(g_ID,user_id,Business_ID,headers1,BASE_URL)
            # print result
            f_name = line['father name']
            f_email = line['father email']
            method = "GET"
            body = {"condition":
                        {"Title": {"mandatory": True, "value": f_name},
                         "EmailID": {"mandatory": True, "value": f_email}}  # here "True" means exact matching
                , "min_non_mandatory_match": 0}

            url = BASE_URL + zviceID + "/getMatchingBUs?filter=" + json.dumps(body)
            # url = "https://twig.me/v8/products/8LS8752NB6U5Y/maxproducts/30"
            jasub = CM.hit_url_method(body, headers1, method, url)
            print jasub
            result = json.loads(jasub)
            matches = result['data']['matches']
            print matches
            if not matches:
                print "empty"

            else:
                print "not empty"




def mainworkflow(body, h1, B_URL):

    global BASE_URL
    global headers1
    BASE_URL = B_URL
    headers1 = h1

    try:
        w_ID = body['FormData']['WorkflowID']
        w_ID = str(w_ID)
    except:
        w_ID = 0

    adding_in_bulk = "268"


    if  body['Cmd'] == "form-submit":
        if body['FormID'] == adding_in_bulk:
            add_users_in_bulk(body, w_ID,  body['BusinessTag'], headers1, BASE_URL)