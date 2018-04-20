#!/usr/local/bin/python

import base64
import time
import urllib2
from urllib2 import URLError
from urllib2 import HTTPError
import requests
import urllib
import json
import time
import os
import sys
import hashlib


# BASE_URL="http://54.153.24.183/v1/"
# email = 'archanahp14@gmail.com'
# pwd = 'underthesky123'

BASE_URL="http://54.193.20.204/v1/"
email = 'sujoy@zestl.com'
pwd = 'Zestl123'
sha512pwd = hashlib.sha512(pwd).hexdigest()
akey = 'dfd8f390c6cbd8fd95c34f79aa4a9480eff582befdb1d86f0027d2703de42996d230fed3ae4c2bb59a7995d9a99c390acbee86d1fd86f20dfb72f81e0a4e5a68'
hasec = '984e6a3c9253b494d96ee364efa203d306e88b180d9c630711d4f07ce787d7ed79df0a28adc0ed5de9c8e353b4110b4f181796b563ea9776d05730399a528e3a'
sha512apwd = hashlib.sha512(akey + hasec + email + sha512pwd).hexdigest()

def login_user():
        payload = {'email': email, 'password' : sha512pwd}
        header = {'AKEY': akey, 'APWD': sha512apwd}
        return invoke_rest('POST', BASE_URL + 'user/login', payload, header)

def registerZvice(headers, body, zviceID):
    return invoke_rest('PUT', BASE_URL + 'zvice/register/' + zviceID, body, headers)

def getMPWD(authkey_salt, timestamp):
    hpwd = hashlib.sha512(sha512pwd + authkey_salt).hexdigest()
    mpwd = hashlib.sha512(hpwd + str(timestamp) + hasec).hexdigest()
    return mpwd

def insert_notes_PP(body, headers, zviceID):
    return invoke_rest('PUT', BASE_URL + 'ztag/notes_PP/' + zviceID, body, headers)

def insert_notes(body, headers):
    return invoke_rest('POST', BASE_URL + 'zvice/insertnotes', body, headers)

def invoke_rest(request_type, rest_url, payload=None, headers=None):
    count = 1
    while True:
            try:
                    api_url = rest_url
                    if request_type == 'GET':
                            r = requests.get(api_url)

                            to_ret = {'code':r.status_code, 'reply':r.text}
                            print r.code()
                            return to_ret
                    elif request_type == 'POST':
                            r = requests.post(api_url, data=payload, headers=headers)
                            to_ret = {'code':r.status_code, 'reply':r.text}
                            return to_ret
                    elif request_type == 'PUT':
                            r = requests.put(api_url, data=payload, headers=headers)
                            to_ret = {'code':r.status_code, 'reply':r.text}
                            return to_ret
                    else:
                            return "Invalid request type ", request_type
            except Exception, e:
                print "Error in invoking " + request_type + ", " + api_url + ", Reattempting " + str(count)
                count = count + 1
                time.sleep (50.0 / 1000.0); #Sleep 50 milli sec
                    #return "Exception:", e, " in getting the API call"




def feed_data(headers, headers1):

#    filename=raw_input("please enter the name of file")
    filename = 'tmpfile.tsv'
    zbotID = 'FQZTG43QMH767'  # Has to be modified for millenium
    file_fd = open(filename,'r')
    token=list(file_fd)
    b=list()
                # REF. NO.(0)    ACADYEAR(1)    STUDNAME(2)    CLASS(3)    DIVISIONNAME(4)    ROLL NO(5) BUS(6)    DOB(7)    
                #BLOOD GRP(8)    HOUSE(9)    ADDRESS(10)    PHONE1(11)    PHONE2(12)    EMAIL(13)    PHOTOPATH(14)    TWIGMETAG(15)
    for i in range(len(token)):
        b.append(token[i].split("\t"))
    for i in range(0,len(token)):
        if len(b[i][0])>0:
            
            tagEncID = b[i][15].rstrip()
            title = b[i][2] + ' [' + b[i][0] + ']'
            desc = b[i][3] + b[i][4] + "\nBus Route:" + b[i][6]
            loc = 'Millenium'
            if os.path.exists(b[i][0] + "_thumb.JPEG"):
                fileName = b[i][0] + "_thumb.JPEG"
            else:
                fileName = b[i][0] + ".JPEG"

             # with open(fileName, "rb") as f:
             #     data = f.read()
                 # media = data.encode("base64")
            media = "";
            media_size = len(media)  

            data = {'zvicetype':'ITAG', 'zviceloc': loc, 'zviceinfo': desc , 'zvicelink': 'NEW', 'lat': 'lat', 'long': 'long', 'zbotid': zbotID, 'title': title, 'tagprofile' : 0, 'media_type': 'image/jpg', 'media_ext': 'jpg', 'media': media, 'media_size': media_size}

            result_json = registerZvice(headers, data, tagEncID)
            code = result_json['code']
            reply = result_json['reply']
            if code == 200:
                reply_json = json.loads(reply)
                msg = reply_json['message']
                err = reply_json['error']
                if err == False:
                    print tagEncID + " registered successfully!!!!"
                else:
                    print tagEncID + " couldn't be registered, msg:" + msg
                    
            #Add notes (extra details)
            # REF. NO.(0)    ACADYEAR(1)    STUDNAME(2)    CLASS(3)    DIVISIONNAME(4)    ROLL NO(5) BUS(6)    DOB(7)    
            # BLOOD GRP(8)    HOUSE(9)    ADDRESS(10)    PHONE1(11)    PHONE2(12)    EMAIL(13)    PHOTOPATH(14)    TWIGMETAG(15)
            #Status(16)  siblingrefno(17)   isRTE(18)    school_package_id(19)
    
            tagNote = {"NoteHeader": "Academic Year", "Note": b[i][1]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Class", "Note": b[i][3]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Division Name", "Note": b[i][4]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Roll No.", "Note": b[i][5]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Bus", "Note": b[i][6]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Date Of Birth", "Note": b[i][7]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Blood Group", "Note": b[i][8]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "House", "Note": b[i][9]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Address", "Note": b[i][10]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Phone", "Note": b[i][11]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Secondary Phone", "Note": b[i][12]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Email ID", "Note": b[i][13]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Status", "Note": b[i][16]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Sibling ref no.", "Note": b[i][17]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "RTE", "Note": b[i][18]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "School Package ID", "Note": b[i][19]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            #data = json.dumps(data) # => {..., 'generic' : true, ...}
            #data = json.loads(data)
            #print data

def uploadNote(data, headers, tagEncID):
    result_json1 = insert_notes_PP(data, headers, tagEncID)
    reply = result_json1['reply']
    code = result_json1['code']
    print reply
    if code == 200:
        reply_json = json.loads(reply)
        msg = reply_json['message']
        err = reply_json['error']
        if err == False:
            print tagEncID + " Note added successfully!!!!"
        else:
            print tagEncID + " Note couldn't be added, msg:" + msg
            

if __name__ == '__main__':
    jsondata = login_user()
    if jsondata['code'] == 200:
        reply = jsondata['reply']
        json_reply = json.loads(reply)
        loginToken =  json_reply['loginToken']
        authorization = json_reply['AuthKey']
        timestamp = int(time.time())
        mpwd = getMPWD(authorization, timestamp)

        print "============================="
        print "LoginToken:" + loginToken
        print "authorization:" + authorization
        print "timestamp:" + str(timestamp)
        print "mpwd:" + mpwd
        print "============================="

        #headers = {'Content-type': 'application/json;charset=UTF-8', 'Authorization':authorization, 'LoginToken':loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey, 'MPWD': mpwd}
        headers = {'Authorization':authorization, 'LoginToken':loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey, 'MPWD': mpwd}
        headers1 = {'Content-type': 'application/x-www-form-urlencoded','Accept': 'text/plain', 'Authorization':authorization, 'LoginToken':loginToken, 'TimeStamp': str(timestamp), 'AKEY': akey, 'MPWD': mpwd}
        feed_data(headers, headers1)
