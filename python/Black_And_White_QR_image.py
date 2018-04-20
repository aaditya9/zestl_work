
import qrcode
import StringIO
import urllib
import urllib2
import json
from urllib import urlencode
# import base64

BWVersion = True
infile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/user_to_group_MIT.txt"
outdir = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/output_files/qr_codes/MNS_27_JUNE_NEW_Stud_Data/"
urlstring = "www.twig.me/"

imgformat = "jpeg"


tryurl = "http://54.193.79.89/genQR-php.php?"
# count=1&start=1000022800&nfc=1&dfr=1&save=0&showimg=1&type=1&backID=0&prntID=1"

query = {"count" :  1, "start" : 100, "nfc" : 1, "dfr" : 1, "save" : 0, "showimg" : 1, "type" : 1, "backID" : 0, "prntID" : 1}
# outstring = urlencode(query)
# print outstring
# # response = urllib2.urlopen(tryurl)
# urllib.urlretrieve(tryurl, "local-filename.jpg")

# print "done"
with open(infile, 'r') as f:
    for line in f:
        line = line.strip()
        imagefile = outdir + line + "." + imgformat
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

            decurl = "http://twig.me/v1/push/dectest/" + line
            response = urllib2.urlopen(decurl)
            html = response.read()
            decTag = json.loads(html)['decTagID']
            query['start'] = decTag
            url = tryurl + urlencode(query)
            # print url
            # print imagefile
            urllib.urlretrieve(url, imagefile)
            print "image " + imagefile + " written"