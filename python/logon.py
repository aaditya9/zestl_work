
import hashlib
import time
import requests
import json

akey = 'dfd8f390c6cbd8fd95c34f79aa4a9480eff582befdb1d86f0027d2703de42996d230fed3ae4c2bb59a7995d9a99c390acbee86d1fd86f20dfb72f81e0a4e5a68'
hasec = '984e6a3c9253b494d96ee364efa203d306e88b180d9c630711d4f07ce787d7ed79df0a28adc0ed5de9c8e353b4110b4f181796b563ea9776d05730399a528e3a'

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def login_user(email, pwd, BASE_URL):
    sha512pwd = hashlib.sha512(pwd).hexdigest()
    sha512apwd = hashlib.sha512(akey + hasec + email + sha512pwd).hexdigest()
    payload = {'email': email, 'password': sha512pwd}
    header = {'AKEY': akey, 'APWD': sha512apwd, "Content-Type" : "application/x-www-form-urlencoded"}
    jsonreply = invoke_rest('POST', BASE_URL + 'user/login', payload, header)
    # print jsonreply
    return jsonreply
def req_headers(email, pwd, BASE_URL):
    BASE_URL = BASE_URL
    email = email
    pwd = pwd
    sha512pwd = hashlib.sha512(pwd).hexdigest()

    jsondata = login_user(email, pwd, BASE_URL)


    if jsondata['code'] == 200:
        try:
            reply = jsondata['reply']
            json_reply = json.loads(reply)
            loginToken = json_reply['loginToken']
            authorization = json_reply['AuthKey']
            # print authorization
            timestamp = int(time.time())
            # timestamp = 1475499814
            # loginToken = '2LZ59A2AE3EMV'
            # authorization = 'c25604314c45dc6b38d17a91bc072d75128590d95da2859463b9b2734d01207e590ed3e86780cb0f71ed292e07c012db8a16fc3f8188daa2430de9ee47173b47'

            url = BASE_URL + "thirdparty/get/mpwd"
            method = "POST"
            body = {'akey': akey, 'email': email, 'pwd': sha512pwd, 'authkey': authorization, 'logintoken' : loginToken, 'TimeStamp': timestamp}
            header = {'content-type' : "application/json"}
            body = json.dumps(body)
            # jsondata = hit_url_method(body, headers, method, BASE_URL)
            jsondata = invoke_rest(method, url, body, header)

            mpwd = json.loads(jsondata['reply'])['mpwd']
            # print mpwd

            # mpwd = getMPWD(authorization, timestamp, pwd)


            headers = {'Authorization': authorization, 'LoginToken': loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey,'MPWD': mpwd, 'device' : 'android'}
            headers1 = {'Content-type': 'application/json;charset=UTF-8', 'Authorization': authorization, 'LoginToken': loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey, 'MPWD': mpwd, 'device' : 'android'}
            return (headers, headers1)
        except KeyError:
            print jsondata
            return (None, None)
    else:
        return (None, None)


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
