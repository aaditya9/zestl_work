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
import lib.login1 as LL



def registerZvice(headers, body, zviceID):
    return LL.invoke_rest('PUT', LL.BASE_URL + 'zvice/register/' + zviceID, body, headers)


def insert_notes_PP(body, headers, zviceID):
    return LL.invoke_rest('PUT', LL.BASE_URL + 'ztag/notes_PP/' + zviceID, body, headers)


def updateDetails(headers, body, zviceID):
    return LL.invoke_rest('POST', LL.BASE_URL + 'zvice/interaction/' + zviceID, body, headers)

# the house value is a number - i'll change it to the correct colour
def house_converter(argument):
    switcher = {
        "1": "red",
        "2": "green",
        "3": "blue",
        "4": "yellow",
    }
    return switcher.get(argument, "not assigned") # if the house is not assigned - then use "not assigned" as value.

def feed_data(headers, headers1):

    zbotID = LL.zbotID  # Has to be modified for millenium
    # my file name is the first argument on the command line. this file contains all the data to be uploaded
    file_fd = open(sys.argv[1],'r')
    token=list(file_fd)
    b=list()
                # REF. NO.(0)    ACADYEAR(1)    STUDNAME(2)    CLASS(3)    DIVISIONNAME(4)    ROLL NO(5) BUS(6)    DOB(7)    
                #BLOOD GRP(8)    HOUSE(9)    ADDRESS(10)    PHONE1(11)    PHONE2(12)    EMAIL(13)    PHOTOPATH(14)    TWIGMETAG(15)
                    #Status(16)  siblingrefno(17)   isRTE(18)    school_package_id(19) parent_qrcode(20) DropBus(21) Sex(22)
                    
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
                        if(msg == 'A Zvice with this ID is already registered')
                            data = json.dumps({"moreInfo": {"Address":"","Address2":"","Address1":"","Mobile number":""},"interactionID":"CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG","title": title,"desc": desc})
                            print tagEncID           
                            result_json = updateDetails(headers1, data, tagEncID)
                            print result_json
 

                    
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
            tagNote = {"NoteHeader": "Pickup Bus", "Note": b[i][6]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Date Of Birth", "Note": b[i][7]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Blood Group", "Note": b[i][8]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "House", "Note": house_converter(b[i][9])};
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
#new adds
            tagNote = {"NoteHeader": "Parent QR code", "Note": b[i][20]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Drop bus route number", "Note": b[i][21]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)
            tagNote = {"NoteHeader": "Sex", "Note": b[i][22]};
            data = {'notetype': 'P', 'lat': 'l', 'long': 'long', 'generic': 'Notes', 'tagnotes' : json.dumps(tagNote)}
            uploadNote(data, headers, tagEncID)


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
        headers, headers1 = LL.req_headers()
        print headers
        feed_data(headers, headers1)
