
import qrcode
import StringIO
import urllib
import urllib2
import json
import csv
from urllib import urlencode
# import base64

BWVersion = False
infile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
outdir = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/output_files/JCNC/"
urlstring = "https://www.twig.me/"

imgformat = "png"


# tryurl = "http://54.193.79.89/genQR-php.php?"
tryurl = "http://35.154.64.119/genQR-php.php?"
# count=1&start=1000022800&nfc=1&dfr=1&save=0&showimg=1&type=1&backID=0&prntID=1"

query = {"count" :  1, "start" : 100, "nfc" : 1, "dfr" : 1, "save" : 0, "showimg" : 1, "type" : 7, "backID" : 0, "prntID" : 0, "cust" : "GENERIC-new-type7"}
# outstring = urlencode(query)
# print outstring
# # response = urllib2.urlopen(tryurl)
# urllib.urlretrieve(tryurl, "local-filename.jpg")
hasHeader = "Y"
# print "done"
with open(infile, 'r') as f:
    data = csv.reader(f, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()

    for row in data:
#         email = row[0]
#         password = row[1]
# with open(infile, 'r') as f:
#     for line in f:
        line = row[0].strip()
        name = row[1].strip()
        filename = row[1].strip()
        imagefile = outdir + filename + "." + imgformat
        # imagefile = outdir + line + "_" + name + "." + imgformat

        if BWVersion:
            qrwrite = urlstring + line
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qrwrite)
            qr.make(fit=True)

            img = qr.make_image()

            buffer = StringIO.StringIO()
            img.save(buffer, imgformat.capitalize())
            imagefile = outdir + line + "." + imgformat
            with open(imagefile, "wb") as fh:
                fh.write(buffer.getvalue())
        else:
            # print "nothing"

            decurl = "https://twig.me/v1/push/dectest/" + line
            response = urllib2.urlopen(decurl)
            html = response.read()
            decTag = json.loads(html)['decTagID']
            query['start'] = decTag
            url = tryurl + urlencode(query)
            print url
            print imagefile
            urllib.urlretrieve(url, imagefile)
            print "image " + imagefile + " written"




