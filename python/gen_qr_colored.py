
import qrcode
import StringIO
import urllib
import urllib2
import json
from urllib import urlencode
# import base64

BWVersion = False
infile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.txt"
# infile = "/home/ec2-user/scripts/input_files/story_station/story_station.txt"
outdir = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/output_files/army/"
# outdir = "/home/ec2-user/scripts/output_files/qr_codes/story_station/"
urlstring = "https://www.twig.me/"


# tryurl = "http://54.193.79.89/genQR-php.php?"    #### if this gives socket error then server is not working.
tryurl = "http://35.154.64.119/genQR-php.php?"
# count=1&start=1000022800&nfc=1&dfr=1&save=0&showimg=1&type=1&backID=0&prntID=1"

query = {"count" :  1, "start" : 100, "nfc" : 0, "dfr" : 1, "save" : 0, "showimg" : 1, "type" : 1, "backID" : 0, "prntID" : 1}
# outstring = urlencode(query)
# print outstring
# # response = urllib2.urlopen(tryurl)
# urllib.urlretrieve(tryurl, "local-filename.jpg")

# print "done"
with open(infile, 'r') as f:
    for line in f:
        line = line.strip()
        imagefile = outdir + line + ".png"
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
            img.save(buffer, 'PNG')
            imagefile = outdir + line + ".png"
            with open(imagefile, "wb") as fh:
                fh.write(buffer.getvalue())
        else:
            # print "nothing"

            decurl = "http://twig.me/v13/push/dectest/" + line
            response = urllib2.urlopen(decurl)
            html = response.read()
            decTag = json.loads(html)['decTagID']
            query['start'] = decTag
            url = tryurl + urlencode(query)
            # print url
            # print imagefile
            urllib.urlretrieve(url, imagefile)
            print "image " + imagefile + " written"