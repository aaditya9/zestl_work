

import json
import csv
import logon as LL
import common as CM
import urllib
import base64
import requests


SERVER = "https://twig.me/"
version = "v13/"
BASE_URL = SERVER + version

# zviceID = "AZ7RZ78HRVCM3"
# zbotID = "D94R5WDH393N4" ##bookspace
zbotID = "8WATL6URGUT42" ## bookspace old

email = "admin@zestl.com"
pwd = "Zspladmin99"


headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

# infile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/try_ner_char_book.csv"
infile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/isbn_debug.csv"
# imgdir = "C:/Users/MInal Thorat/Dropbox/Zestl-share/Test/bookspace/bookcover/"
imgdir = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/minal/bookcover/"

hasHeaders = True

if (CM.parse_files(infile) == "success"):
    # print count
    with open(infile, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        if hasHeaders:
            row1 = data.next()
        for row in data:
            codecs = ['utf8', 'cp1252', 'utf16', 'utf32', 'iso-8859-15']
            for i in codecs:
                try:
                    # return string.decode(i)
                    print "*****************"
                    print i
                    print unicode(row[3], i , 'ignore')
                    print row[3].decode(i, 'ignore')
                    print type(row[3].decode(i, 'ignore'))
                    print row[3].decode(i, 'ignore').encode(i, 'ignore')
                    print type(row[3].decode(i, 'ignore').encode(i, 'ignore'))
                    print row[3].decode(i, 'ignore').encode('utf8', 'ignore')
                    print type(row[3].decode(i, 'ignore').encode('utf8', 'ignore'))
                    # print row[3].decode(i).encode('iso-8859-15')


                except:
                    print "encode error " + i

            title = CM.force_decode(row[3])
            # title = title.encode('utf-8')
            title = title.encode('latin1').decode('utf8')
            print title.encode('latin1').decode('utf8')
            print title
            cat = CM.force_decode(row[3])
            lang = CM.force_decode(row[10])
            isbn = CM.force_decode(row[4])
            author = CM.force_decode(row[6])
            zviceID = CM.force_decode(row[23])
            publisher = CM.force_decode(row[7])
            edition = CM.force_decode(row[13])
            img = CM.force_decode(row[15])


    # print "Stop here"
    # zviceID = "FCYBCJQDGPQNQ"
    # isbn = "9781402734328"
            url =   BASE_URL + "book/isbn/" + isbn
            body = {}
            response = CM.hit_url_method(body, headers1, "GET", url)
            print response
            data = {}
            try:
                res = json.loads(response)
                data = json.loads(res['data'])
            except:
                print "no isbn data returned"
            body = {}
            extradata = {}
            moreInfo = {}
            body['title'] = title
            # try:
            #     body['title'] = data['title']
            # except KeyError:
            #
            #     title = ""

            #     # title = title.decode(encoding = 'UTF-8')
            #     # title = title.encode(encoding='UTF-8', errors='ignore')
            #     body['title'] = title
            try:
                body['zviceinfo'] = data['description']
            except KeyError:
                body['zviceinfo'] = ""

            try:
                extradata['Author'] = data['author']
            except KeyError:
                extradata['Author'] = author
            try:
                extradata['Language'] = data['lang']
            except KeyError:
                # print ""
                extradata['Language'] = lang
            try:
                extradata['ISBN'] = data['isbn']
            except KeyError:
                extradata['ISBN'] = isbn
            try:
                extradata['Edition'] = data['edition']
            except KeyError:
                extradata['Edition'] = edition
            try:
                urlimg = data['imgurl']

                urllib.urlretrieve(urlimg, "00000001.jpg")
                with open("00000001.jpg", "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                encoded_string = encoded_string.encode('utf8')
                # print encoded_string
                # file1 = {}
                body['media'] = encoded_string
                body['media_type'] = "image/jpg"
                body['media_ext'] = "jpg"
                body['media_size'] = 120000
                # body['media_name'] = "1.jpg"
                # body['Caption'] = ""

                # body['file_id'] = json.dumps(file1)

                # method = "POST"

                # jsonresponse = hit_url_method(body, headers1, method, url)

                # print jsonresponse
            except:
                if img != "":
                    imgfile = imgdir + img
                    try:
                        with open(imgfile, "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())
                        encoded_string = encoded_string.encode('utf8')
                        # print encoded_string
                        # file1 = {}
                        body['media'] = encoded_string
                        body['media_type'] = "image/jpg"
                        body['media_ext'] = "jpg"
                        body['media_size'] = 120000
                    except: print "No image"
                # print "no image found"
            try:
                extradata['Publisher'] = data['publisher']
            except KeyError:
                extradata['Publisher'] = ""
            # extradata['Book category'] = cat
            # extradata['Series'] = series
            body['moreInfo'] = extradata
            # body['extradata'] = extradata)
            body['zvicetype'] = "ZTAG"
            body['lat'] = "---"
            body['long'] = "---"
            body['zviceloc'] = "---"
            body['tagprofile'] = 2
            body['zvicelink'] = "NEW"
            body['zbotid'] = zbotID

            body['zviceid'] = zviceID


            url = BASE_URL + "zvice/register"
            method = "PUT"

            response = CM.hit_url_method(body, headers1, method, url)
            print response
            print "============"
