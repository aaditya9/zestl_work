
import qrcode
import StringIO
import csv
import base64

infile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
# outdir = "C:/Users/Minal Thorat/MINAL OFFICE DATA/APS - Army Public School/Qr Images/army_4DEC"
outdir = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/output_files/JCNC/"
urlstring = "https://www.twig.me/"
hasHeader = "Y"
tag = 0
NameCol = 1
with open(infile, 'r') as f:

    data = csv.reader(f, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    for line in data:
        zvice = line[tag]
        name = line[NameCol].strip()
        qrwrite = urlstring + zvice
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qrwrite)
        qr.make(fit=True)

        img = qr.make_image()

        # cp.response.headers['Content-Type'] = "image/png"
        buffer = StringIO.StringIO()
        img.save(buffer, 'PNG')
        # imagefile = outdir + name + "_" + zvice + ".png"
        imagefile = outdir + zvice + ".png"
        with open(imagefile, "wb") as fh:
            fh.write(buffer.getvalue())
# img_str = base64.b64encode(buffer.getvalue())
# print img_str
# print img
# return buffer.getvalue()
# print done