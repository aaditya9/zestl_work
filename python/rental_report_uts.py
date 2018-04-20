
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
import re
import sys
import csv
import StringIO
import itertools
# from fuzzywuzzy import fuzz
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from datetime import datetime
from dateutil import tz
import arrow
# from pytz import  timezone
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib

import hashlib\

import lib.login_generic as LL


def sendEmail(recipients, sub, attach):
    # recipients = ['rcpt1@example.com', 'rcpt2@example.com', 'group1@example.com']
    emaillist = [elem.strip().split(',') for elem in recipients]
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = 'sujoy@zestl.com'
    msg['Reply-to'] = 'sujoy@zestl.com'

    msg.preamble = 'Multipart massage.\n'

    part = MIMEText("Hi, \nPlease find attached the report file.\nThis is a system generated email.\n -Team TwigMe")
    msg.attach(part)

    part = MIMEApplication(open(attach, "rb").read())
    part.add_header('Content-Disposition', 'attachment', filename=attach)
    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login("sujoy@zestl.com", "HOTshot09")

    server.sendmail(msg['From'], emaillist, msg.as_string())


def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


email = "archanahp14@gmail.com"
pwd = "zestl123"
ZbotID = "A4CJ2VHTTJS9Y"
BASE_URL = "https://www.twig.me/v1/"

tday = arrow.utcnow()
tday = str(tday)
tday = re.sub(r'(T.*)', '', tday)
print tday

today = tday


# headers, headers1 = LL.req_headers(passkey)
headers, headers1 = LL.req_headers(email, pwd, ZbotID, BASE_URL)


zbotID = ZbotID

url = BASE_URL + "library/rental/" + zbotID + "/report"
# url = BASE_URL + "library/reading/" + zbotID + "/report"
method = "POST"

body = {"StartDate" :  today}
jsonreply = hit_url_method(body, headers1, method, url)

jsonreply = json.loads(jsonreply)
rentedHeader = ["Book Title", "User Title",  "Rent Date Time"]
rented = [rentedHeader]
returned = []

styles = getSampleStyleSheet()
styleN = styles["BodyText"]
#used alignment if required
styleN.alignment = TA_LEFT

styled = ""
isreturned = 1
for item in jsonreply['report_data']:
    # print len(item)
    isreturned = 1
    itemMod = []
    for i in range (0, len(item)):
        print item[i]
        if item[i] == None:
            item[i] = ""
        else:
            if (i == 4 and "Time" not in item[4]) or (i == 5 and "Time" not in item[5] and item[5] != ""):
                # print item[4]
                from_zone = tz.tzutc()
                to_zone = tz.gettz('Asia/Kolkata')
                # to_zone.tzinfo = 'Asia/Kolkata'

                # utc = datetime.utcnow()
                utc = datetime.strptime(item[i], '%Y-%m-%d %H:%M:%S')

                # Tell the datetime object that it's in UTC time zone since
                # datetime objects are 'naive' by default
                utc = utc.replace(tzinfo=from_zone)

                # Convert time zone
                central = utc.astimezone(to_zone)
                item[i] = re.sub(r'(\+.*)','',str(central))
            para = Paragraph(item[i], styleN)
            if i == 0 or i == 2 :
                print "nothing"
            else:
                itemMod.append(para)
    # styled = Paragraph(item, styleN)

    if item[len(item)-1] == "":
        # print "=========Rented out========="
        rented.append(itemMod)
        # print item
    else :
        # print "=========Returned========="
        # print item
        returned.append(itemMod)


doc = SimpleDocTemplate("simple_table.pdf", pagesize=letter)

elements = []

data = returned
data2 = rented



width, height = A4
styles = getSampleStyleSheet()
styleN = styles["BodyText"]
styleN.alignment = TA_LEFT
styleBH = styles["Title"]
styleBH.alignment = TA_CENTER
styleH = styles["Heading1"]
# styleH.alignment = TA_CENTER

def coord(x, y, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y

t3 = Table(data, colWidths=[5.5 * cm,  5.5 * cm, 3* cm, 3 * cm])


t2 = Table(data2, colWidths=[6 * cm,  6 * cm, 4* cm])

t2.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
                       # ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                       # ('VALIGN', (0, 0), (0, -1), 'TOP'),
                       # ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                       # ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       # ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                       # ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                       ]))

t3.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                       ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
                       # ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                       # ('VALIGN', (0, 0), (0, -1), 'TOP'),
                       # ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                       # ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       # ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                       # ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                       ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                       ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                       ]))

elements.append(Paragraph("Books rental report for " + today ,styleBH))
elements.append(Spacer(1,0.4*cm))
elements.append(Paragraph("Books returned today",styleH))
elements.append(Spacer(1,0.2*cm))
elements.append(t3)
elements.append(Spacer(1,0.6*cm))
elements.append(Paragraph("Books rented out today",styleH))
elements.append(Spacer(1,0.2*cm))
elements.append(t2)
# write the document to disk
doc.build(elements)

recipients = ['sujoy@silabtech.com', 'archanahp14@gmail.com']
sub = "reports"
filename = "simple_table.pdf"
sendEmail(recipients, sub, filename)

# print rented, returned

