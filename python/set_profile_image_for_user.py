import base64
import logon as LL
import common as CM
import password as PP
import csv
# import os.path
# from pathlib import Path
# file_path = "C:/Users/Minal Thorat/MINAL OFFICE DATA/INDUS_PUNE/IELC_KoregaonPark/Nursery/"
# os.path.exists(file_path)
#
# file_name = "Omer Guttman.png"
# path = "C:/Users/Minal Thorat/MINAL OFFICE DATA/INDUS_PUNE/IELC_KoregaonPark/Nursery/" + file_name
# my_file = Path("C:/Users/Minal Thorat/MINAL OFFICE DATA/INDUS_PUNE/IELC_KoregaonPark/Nursery/" + file_name)
# if my_file.exists():
#     print "found"
# else:print "not found"
#
# result= os.path.isfile(path)
# print result


SERVER = "https://twig.me/" #Production
version = "v13/"
BASE_URL = SERVER + version

# zviceID = "FFPX5326HH87U"





email = "admin@zestl.com"
pwd = PP.pwd

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

# f_name = "ANDRO.jpg"
hasHeader = "Y"
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
with open(inputFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    counter = 0
    for row in data:
        counter += 1
        print counter
        zviceID = row[0]
        f_name = row[1] + ".png"
        try:
            print "working on : " + str(zviceID) + " : " + f_name
            fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/TEST_ATTACHMENT/" + f_name
            fname = "C:/Users/Minal Thorat/MINAL OFFICE DATA/INDUS_PUNE/IELC_KoregaonPark/Nursery/" + f_name
            method = "POST"
            url = BASE_URL + 'zvice/interaction/' + zviceID
            # print url
            with open(fname, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            encoded_string = encoded_string.encode('utf8')

            typ = "image"    ### please write "image" if u write "img" then it will not work
            body = {}
            body['media_name'] = f_name
            body['media'] = encoded_string
            body['media_type'] = typ
            body['media_ext'] = "PNG"
            body['media_size'] = 120000
            body['media_compressed'] = True
            body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"
            jsonresponse = CM.hit_url_method(body, headers1, method, url)
            print jsonresponse
        except:print "Name not found"
