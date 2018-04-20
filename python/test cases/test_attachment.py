import logon as LL
import common as CM
import base64
from os import walk


SERVER = "http://35.154.64.11/"
version = "v5/"
BASE_URL = SERVER + version

zviceID = "876MD568TAUH2"    ####  Business ID

email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)


fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/minal/test_2.txt"
# f = []
# for (dirpath, dirnames, filenames) in walk(fname):
#     f.extend(filenames)
#     break


for a in jsondata['data']['elements']:
    title = "code test"
    if title == a['title']:
        print "go to next"
        for ac in a['actions']:
            title = "Add Attachment"
            if title == ac['title']:
                print "go to next 1"
                method = "POST"
                url = ac['actionUrl']
                print url
                body = {}
                # body['GalleryID'] = 1725
                # for item in f:
                #     filename = fname + "/" + item
                with open(fname, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                encoded_string = encoded_string.encode('utf8')

                # typ = "image/jpg"    ### please write "image" if u write "img" then it will not work
                body = {}
                body['media'] = encoded_string
                body['media_type'] = ""
                body['media_ext'] = "TXT"
                body['media_size'] = 120000
                # body['remove'] = "false"
                body['media_compressed'] = True
                jsonresponse = CM.hit_url_method(body, headers1, method, url)
                print jsonresponse