
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
import smtplib

# from fuzzywuzzy import fuzz
import hashlib\

import lib.login1 as LL



def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata


def getBaseStructure(zbotID, headers1):
    url = LL.BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    method = "POST"
    response = hit_url_method(RequestBody, headers1, method, url)
    return response

def send_email(user, pwd, recipient, subject, body):

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"







zbotID = LL.zbotID

filename = sys.argv[1]

da1 = {u'Saumya Marfatia 11': u'F4NP4SNYNMRXV,Inactive  DOB- 30/Apr/2015', u'Ayan  kurhekar': u'F9RJGX2B4EKBJ,Library User', u'asmi  thete': u'W54NBPF3843GG,book   star   Renewal  25/6/16', u'Krishna Yavale -16': u'F7RBLBZRZTHX2,Inactive  DOB 11/Mar/2006', u'Ishan Dhavalikar 96': u'7VSJBU8VA7HRU,on  hold   DOB 16/10/2010 Renewal 9/7/2016', u'Shardul Bali -27': u'BFMKDDSSM63Y8,inactive card to be returned', u'Akshar Bhardwaja -7': u'EPCVGMAB2ZNRH,Inactive DOB- 6/Feb/2011', u'Anoushka Paithankar -82': u'AA5E66TEQPUVH,BookStar  DOB 6/2/2011 RENEWAL4/7/2016', u'Hritvi Kogje -79': u'BY6NPS6Y56BWL,BookStar on hold 2 month DOB 29/Jan/2011 Renewal 1/4/2016', u'Ashutosh Joshi -47': u'CDWU8PHHEZLDH,book  star   DOB - 16/Nov /2011  Renewal  6/8/16', u'Ishan Diwan -62': u'2FNU26SE3A3R8,Playful DOB 7/Mar/2009 Ishan  DOB 13/Mar/2012 Shaunak Renewal 4/7 /2016', u'Avanish. Ponde': u'FERN9SEJY8TT7,book star renewal 13/7/16', u'Tejaswini Bidve -78': u'EYLH7EHEA7ZAX,BookStar   DOB :15/Oct/2004 Renewal: 28/4/2016', u'Sanika Kelkar -15': u'DQSDZGAX5JL4X,Book Star on hold DOB -25/Jan/2009', u'sara harari 97': u'CP9JW5HTVA4UB,BookStar  DOB 22/august/2006 Renewal 10/10/2016', u'Aadi Dharwadkar -110': u'7RJKQ8CXZBCG9,BookStar  DOB 12/5/2011 RENEWAL 14/7/2016', u'aarushi  gudepkar     121': u'6S8HQESK7W36V,book  star                                                    DOB 13/3/2006                                         Renewal  5/5/16                                ', u'Sanskruti Joshi -33': u'87DNREHXLB2CS,Book Star   On Hold DOB -10/Jun/2009', u'Shruti Pandit -23': u'BEBZ6DRQQQQUA,Book Star  DOB- 7/Dec/2004 Renewal 30/07/2016', u'hritvik borgaonkar -90': u'EY3ACMZXTZNJN,BookStar  DOB 19/01/2013 Renewal 1/8/2016', u'Siddharth Chakravarty': u'23ET98R9PP58R,Library User', u'Aarya Sarpotdar -46': u'WH8CGFZTCY75P,inactive  DOB -30/May /2007', u'Rujuta Rajadnya -17': u'FZGHYFLKUWWRM,Book Star  DOB- 9/Aug/2007 Renewal 28/4/2016', u'jessica  mayur': u'FMXZ57DSFLYQD,Library User', u'Aryan Chandorkar -5': u'WF7QSCL99AK7B,BookStar  DOB.       23/May/2010  renewal 16/5/2016  on  hold  20   june', u'Devika Wagh -75': u'BGEMW7HW2XHJR,inactive  DOB 11/10/2011', u'Krushna Sahoo -86': u'7E367BZLH3L4X,inactiv  DOB 4/5/2010', u'Purva Oak -106': u'WZEPZ68283DVR,BookStar  DOB 22/04/2005 Renewal 30/07/2016', u'Soham Penurkar': u'WAGHW7TQHD4MZ,book  star    Renewal  6/10/16', u'Prashant Jagadale': u'BVXUYHAR4AXAN,Library User', u'Riya Patwardhan -89': u'78H36TDSJRF6T,BookStar  DOB 1/3/2006 Renewal 1/1/2017', u'Devashree Agate -53': u'9V26AHACCQAE3,BookStar  DOB 14/Oct/2006 Renewal 23/Jan /2016', u'Arjun Neurgaonkar -8': u'EC5QJSKSWB3KE,Book  Star   DOB- 26/Jan/2012 Renewal : 22/07/2016', u'Kaivalya Kelkar 98': u'9YGAMVXQHH55R,inactive DOB 10/8/2012 ', u'Gargi Pingle - 103': u'XRXZSY7FKM56V,BookStar  DOB 29/11/2007 Renewal 25/8/2016', u'Meera  Mathkar  ': u'FU75T8APA9ECH,DOB-02/8/2011   Renewal 19/7/16', u'swara   joshi    129': u'WDEDRV82ZB73G, book star  DOB-27/8/2007                                         Renewal    16/6 /16', u'Ishan Roy': u'FQHZJ37E2STTJ,on  hold  book  star  DOB 27/6/2014                        Renewal  2/6/16', u'Sanaa Bhave -59  ': u'CWRXR6UU4N7E2,BookStar  on hold  2 m DOB 22/Jan/2013 Renewal 29/3/2015', u'Amala Purandare -81': u'A85RH96XHRUFB,BookStar  DOB 9/2/2001 Renewal 4/7/2016', u'Sanvika Chavan -22': u'DWARDVBQ8Q7CD,Book Star  DOB- 6/Jul/2012 Renewal 1/5/2016 ', u'Shardul Salunkhe -36': u'E7LUXF6S94AHB,Book Star  DOB -17/Apr/2006  renewal 6/5/2016', u'Aditya Vanjari -30': u'W4LBXPGKVRR8X,BookStar  DOB -12/Feb/2011 ', u'Ojas Zanpure -10': u'BAVYUZYU4GFSN,Book Star  DOB-17/Mar/2006 Renewal 25/5/2015', u'Revati Divekar - 113': u'96B4RN2BHLEHH,Bookstar Revati 10/8/2003 Shreedhana 5/6/2009 Renewal 12/9/2016', u'Avani Dhongde -44': u'WG5Q26KYSCWME,Inactive  50 rs refund  to be given. Has not returned the card yet  DOB -22/Oct/2008 ', u'Mridu Sharma -20': u'BCMCPJRFV6Y4Q,Book Star ???  DOB- 13/Aug/1988 Renewal 30/Oct/2015', u'amod bapat -104': u'XFM5KNMHE5NG4,BookStar -On Hold  From 29th May DOB 23/12/2004 Renewal 27/4/2016', u'Ananya  patil': u'FLWWN2VXVL7XH, book  star    DOB-24/04/16    Renewal   10/6/16', u'Gargee Nanal -24': u'X7L5TMBN7XBM5,Book Star - on hold DOB - 19/Dec/2002 ', u'Avaneesh Gogate': u'763SM46FNAMS8,bookstar renewal 17/7/2016', u'Abhinav Pandit -38': u'EC28VH6S2QBGW,inactive DOB -07/Jun/2007 card returned', u'Aditi Kudalkar  -64': u'2DXDTH726PAMA,BookStar DOB 24/May/2011 due: 17/3/2016', u'Saukhya Latkar  -94': u'7V67EHB4W5QFD,BookStar  DOB 6/1/2012 Renewal 7/7/2016', u'Sharva Prabhudesai -42': u'8J4KMTPKMR794,Playful  DOB -23/Dec/2004 Renewal 10/7/2016', u'sharvi  kalawade': u'W856KJEVE4WCE,book  star   Renewal  28/6/16', u'Bhargav Godbole - 108': u'995VK3PMK4S32,BookStar  DOB 7/5/2011 Renewal 11/7/2016', u'Avishka Sasisankar - 100': u'CUJBMZ23DRF49,Playful  DOB 17/11/2011 Renewal: 22/4/2016', u'Avishkar Mulay': u'DG6AB2XTZAXAP,Bookstar renewal 18/06/2016', u'twig me test user': u'DU25L6YMWJTUL,Library User', u'Sana Gadre -68': u'C4VBWGKZRM8LS,inactive  DOB 15/august/2005', u'Parimal Khandewale': u'XLJ6LSVNMSN37,Bookstar Renewal 25/6/2016', u'sai  ware': u'W6AZN2TTZE988,book  star                                                    DOB-29/8/2007                                         Renewal  1/7/16', u'Maahi Patel -84': u'A77W4Y5W6Z5GR,BookStar on hold DOB 3/Nov/2008  Renewal 22/4/2016', u'Asya Phal -87': u'7XNTWX2YDGTQG,BookStar  DOB 15/8/2012 Renewal 10/3/2016', u'saee erande -73': u'EJX588QRHXNYW,Inactive  DOB 21/04/2009', u'Shrikar Mudpe -54': u'CK4RUTCF2KQR9,BookStar DOB: 9/May/2014 Renewal 4/7/2016', u'Arjun Pandit -83': u'BPPZHKMBBKLB3,BookStar  DOB 2/July/2013 Renewal 4/7/2016', u'Mrunal Maharanwar': u'FQ6HZPU5QF6P2,inactiv    card    returned', u'\nAnuj Gulavani - 9': u'7SPNGPB373LF5,Book Star    on  ohld  DOB- 28/May/2004 Renewal 1/april/2016', u'pranav gholkar -72': u'CSVWYB4BS2662,book star- on hold DOB 19/January/2008 Renewal 25/1/2016 membership on hold 20 Jan 2016 ', u'SHRI': u'9KEUPKDHNNE6X,library user', u'rishabh  joshi': u'F46ZVYRBWQVRW,inactiv DOB-8/12/2010  card  returned', u'Advika  pande': u'F3CZM4UT8ZES4,book  star  DOB-15/11/2008                      Renewal  2/8/16', u'Shirin Chivate -12': u'FKA5J64X7B54T,Book Star  DOB- 5/Feb/2009 Renewal 26/4/2016', u'Ashutosh Sohani - 131': u'FL62ZFBMBFD39,book star renewal 18/6/2016', u'Samradnyee Joshi - 29': u'X4LN8JNZC2TPE,Book Star  DOB - 11/May/2013 Renewal 3/8/2016', u'Aastha  batheja': u'ETHLSM9PXTLHG,book  star  Renewal 3/7/16', u'Shriyan Gholap -88': u'72KYEUFZRLNT9,BookStar  DOB 6/01/2009 Renewal 18/03/2016', u'Aarav Khangan - 99': u'CS3W9L6Z6QBAX,inactiv   card  returned', u'Aarav  gulavani': u'FEVR6VDAHHVR4,boo  star  DOB 27/7/2014  Renewal  9/8/16', u'Nandita Nagarkar -61': u'9L7TGHBX4GWNG,inactive  dob 4 Jan 2008', u'Swaraj Narkhede -69': u'C93BWDXPFWVJ5,Playful  DOB: 16/Jan/2015 Renewal: 14/08/2016', u'Anushka Sahasrabudhe -45': u'WUYJBUMJRQLES,inactive  DOB - 22/Jan/2005 ', u'Anay  Agarwal -25': u'X725PKZJQEFTD,inactive  DOB  25 /Sep/2009', u'Padmaja Udar -13': u'5FHLHJG5X8QG9,Book Star  DOB-17/Mar/2006 Renewal 26/5/2016', u'riddhi walimbe -77': u'AL55F7XRCN93H,BookStar  DOB 19/09/2004 Renewal 26/5/2016', u'Tanvi  pawar': u'W4VZLUZA45CK8,boo  star   deposit  1400  4  book   Renewal  25/7/16', u'Dhruv / Pralhad gokhale': u'EYTQDN7KN3NQP,  Book  star   DOB-17/4/16                                                Renewal  23/6/16', u'asmi  govilkar': u'4VJGZ354HMK29,book  star                                                    DOB-6/feb                                                   Renewal  30/8/16', u'sahil vaidya -65': u'2CS9TYELSB8JV,Bookstar DOB sahil:- 15/09/2006           ria:- 10/01/2011 Renewal 6/8/2016', u'Hridaan Amit Padve -92': u'8YGQL4VFQBXUQ,All rounder  4 Books or 3 Books and 1toy DOB 9/2/2012 Renewal 6/7/2016', u'Amruta  pawar': u'EQW3GZCHHYSPK,book  star  DOB-4/2/2009       on  hold                   Renewal 2/7/16', u'Tanishka  Hudlikar': u'DLQGZ3SQQPWA6,book  star   Renewal  2/8/16', u'Neeraja  kittur': u'FTKQUQ44696KA,book  star   Renewal  27/7/16', u'Rama  deshpande': u'FU3H2FEHY52SA,book  star   DOB-5/11/2005        Renewal  27/8/16', u'Aarohi Dnyate': u'3G67ZGLTEPV2T,bookstar renewal 2/8/2016', u'jaee  kale     125': u'F895G7APQ7N29,book  star                                                   DOB-3/2/2004                                            Renewal   12/7/16', u'Sukrut Kulkarni -31': u'X4KQVJ5N83N2A,Book Star  DOB - 11/Aug/2008 Renewal 4/8/2016', u'Aayush Daflapurkar -43': u'BAR8SMAW53QB6,Book Star  DOB -1/Dec/2009 Renewal 6/3/2015', u'Darshan Narendra -18': u'BMYFG3BEYU643,Book Star  DOB- 24/Sep/2004 Renewal 28/05/2016', u'Anushka Dandekar -56': u'8TW87KWWMJUPB,BookStar  DOB 19/Oct/     2011 Renewa    28/05/2016', u'Rishab  pillai  151': u'F4ZQ5TNDCKNDM,book  star  DOB-22/10/2006  Renewal  18/6/2016', u'Tejas Kavishwar -35': u'8QC5856Z325LS,Book Star on hold from 24 dec DOB -13/Nov/2009 Renewal 3/Jan/2015', u'Aaradhya Bhat': u'E5VPBPP2LFTTB,Book Star membership on hold from 18 nov DOB- 20/Jan/2012 Renewal 1/11/2015', u'Shivansh Gogawale -50': u'WLW3N4RU27SK9,Book Star  DOB - 07/May/2013 Renewal  25/5/16', u'Arjun Chakravarty ': u'23KBNM7BUFTYR,Book Star', u'Shreesh Natu -91': u'83RPNMD32ZWMS, on  hold  BookStar  DOB 2/jun/1010 Renewal 25/7/2016', u'Rohan  Natekar': u'9NMB48GWNVUMA,book  star   DOB-13/6/2006   Renewal   12/7/16', u'Arpita / Mrunmayee Kulkarni -107': u'84AXLJRTA6J4L,BookStar  DOB arpita 25/3/2005 Mrunmayee 15/7/2009 Renewal: 6/4/2016 suspended for 1 month ', u'Aryan Toro -34': u'8R29F2RKERFC4,Inactive DOB -19/Feb/2008', u'Mrudani Pimpalkhare -60': u'XDHYY6XRLYDCC,BookStar  DOB 24/Mar/2015 Renewal  31/3/2016', u'Aditya Grover -63': u'WRBQ9TS6CPKWW,bookstar  DOB 14/august/2005 Renewal 4/jun /2016   on   hold', u'Samruddhi Joshi -21': u'F8GZR9ZBUW43C, bookstar for a month DOB- 28/May/2004 Renewal 1/6/2016 deposit with us 1100', u'Aahaan Nandimath -66': u'7R34T6GUUZRF2,BookStar  DOB 1/06/2006- Aahaan         20/06/2013-agastya Renewal: 07/june/2016', u'Yashashree Samb -40': u'8RZBZCNV4QXRT,inactive -card not returned DOB -2/sep/2006', u'Arnav Shah -14': u'F583UXX24DS6V,Book Star  DOB- 11/June/2004 Renewal 28/10/2016', u'tanvi kesarkar -76': u'FGQWAVXXCLDQF,BookStar from 12/3/2016  DOB 8/12/2004 Renewal 11/9/2016', u'Advait Naik - 130': u'W9M9FUTCW6ZUG,Bookstar Dob 16/02/2011 renewal 17/7/2016', u'purti  karmarkar': u'F5SSRFNYN5RQ9,book  star     Renewal 22/7/16', u'Adish Patukale - 109': u'9EG69Z9FX2G33,BookStar DOB 25/11/2011 Renewal 11/7/2016', u'Rudra aurangabadkar': u'W3W4AMZAFPK82,inactiv  DOB-11/3/2006 card returned', u'ishan   sonsale 132': u'W9ZRK3FWSNYTR,book  star                                                    DOB-1/3/2009                                              Renewal  19/5/16', u'Ahaan Damle ': u'F88YUUFQMQGZ8,book star                                           DOB-30/11/2010                                              Renewal 15/6/16', u'Aaradhya / Adhyayan Bansod': u'DCJWBLJRREK75,bookstar DOB aaradhya 25/08/05 adhyayan 04/10/11 renewal 19/05/2016', u'sia  bramhankar': u'X6JN3T5YQTP2G,book   star    Renewal  29/7/16', u'Anerie  shah': u'EYJNDK4L4QLHG,Renewal 5/5/16', u'ojas kulkarni _ 105 ': u'XKXP9FYV3SQXL,BookStar   DOB 11/04/2013. Renewal 14/7/16', u'Aditya Dhondse -32': u'BYX355PHCLNK2,Book Star  DOB - 31 / Mar/ 2007 Renewal 4/5/2016', u'Aryan Joshi  95': u'76RRZJ2NH99QR,BookStar on hold  DOB 1/6/2005 Renewal 8/4/2016', u'kabir  karlekar': u'W436N5CGW8AN6,book  star  Renewal  3/7/16', u'sashwat  jaiswal    133': u'W9MS5JC4D9WHV, Book  star                                DOB-19/7       Renewal  20/7/16', u'Soham Karanjkar -6': u'EECG8ATFTTHYF,Book Star   DOB- 23/Aug/2005 Renewal 23/08/2016', u'Kaveri Joshi 102': u'D6E8AAWYJZKQR, inactive  DOB 26/6/2015   card retuned', u'owi bagul -71': u'77YH4ZLZPGUAA,Inactive Refund Given Card Returned DOB 3/July/2006', u'Soham Bharamgonde': u'5TFLX6L78PMD4,Bookstar', u'Reyansh Bhide -51': u'FWQH8Z9Q568SX,Playful  on hold from 17th March Hrugved DOB:20/Feb /2006 Reyansh DOB: 20/Jul/2011 Renewal 20/03 /2016 ', u'manasi   kondejkar': u'W6WH72N9V8FYL,Library User', u'Rishabh  ghate': u'FEJYBNJZKB932,book  star   Renewal 28/7/16', u'Saket   Gadre   124': u'EZDRLVKUXL4MZ,book  star                                                    DOB-4/1/2010                                            Renewal  11/8/16', u'Siya Shejwalkar -57': u'X7XGCBT4XBS7Q,inactive  DOB 8/Jan/2014', u'sonal   mahajan': u'FCSSWA2E7GL9L,book  star Renewal 28/7/16', u'swara  Gurav': u'FLLSC353E9BSG,book  star   Renewal  15/7/16', u'naren chandekar -74': u'EYG6KZMTAVJ6L,BookStar  DOB 18/3/2011 RENEWAL 23/6/2016', u'Riya Kulkarni -80': u'EX2SL3YJK7A93,inactive  DOB 25/Dec/2001', u'Reyansh   palsule': u'FHC4ATXLCNGSD,inactiv   card  returned', u'Nimit Raje -58': u'CMSZZA7D28RGS,BookStar  DOB 13/Mar/2012  Renewal   24/7/16', u'Ishan Nerkar -41': u'8TK4P4ZCXWYGR,Book Star  DOB -29/Jan/2008 Renewal 9/9/2016', u'Mallika Datar -19': u'E2Y2TUB674A34,BookStar  DOB- 7/Sep/2013 Renewal 6/5/2016', u'Satyen Pingale': u'F49J9B3UJND3X,Renewal   4/6/2016', u'Saket Mhaske 101': u'DCH3YGJRASF69,book star DOB 19/01/2011 Due 23/02/2016', u'Siya Mulay -49': u'WEQJFXRWH6Y82,inactive  DOB -23/Jan/2008 Renewal ', u'Asmi Sapale -39': u'8N94E4M3JDGD3,on  hold  Book Star DOB -6/may/2013 Renewal 20/7/2016', u'sanjyot  nanajkar   122': u'C5CBR4XLAVJA3,book  star                                                    DOB-15/3/2008                                          Renewal  7/,6/16', u'Anshita Gadkari -67': u'2FS8L8NYYJQRN,Bookstar DOB-11/Feb/2007  renewal 7/7/2016', u'shalmali  tambe   123': u'EZS5UZX27SXAL,book  star                                                    DOB-10/10/2010                                        Renewal  9/5/16', u'pranav  deshpande  147 ': u'EUGZTV89U7VFN,book   star    DOB -16/10/2009     Renewal 7/6/16', u'Utkarsh Shetty': u'FAUCMQZ2ZPKFC,book  star    Renewal  3/6/16', u'kapil': u'2K5HME8KHAGT7,android Developer', u'Nakshatra Raje -28': u'BG2LDZNEQMBRM,Book Star - on hold DOB - 21/ Jan/ 2009', u'Rama  Shejwalkar -48': u'XBS85PKV2WPUC,Book Star  on hold DOB - 8/Oct /2009 ', u'Prachi Bhatt -52': u'FWEFZZG2HUTU5,BookStar  DOB 21/Oct/2015 Renewal 21/8/2016', u'Abha Ashturkar -70': u'CACASFTZUPG6W,BookStar  DOB 31/Jan/2015 Renewal 10/8/2016', u'Dhruv Manurkar -37': u'E7YYPCG4UZ69B,inactive  DOB -20/Mar/2008', u'Radha Joshi -85': u'9W4JKF29VXX7Q,inactive  DOB 25/Apr/2011', u'shruti srinivasan -93': u'93HNLGQVPELW8,BookStar  DOB 24/12/2005 shruti 21/7l/2011 Siddharth  Renewal 6/7/2016', u'Nidhi Baadkar -55': u'8TMDQDJDV7E2G,BookStar On Hold DOB 28/Sep/2006 Renewal 3/4/2016', u'Nitin M': u'EXYWT3N9NW7CB,Library User'}


#
# {'meera  mathkar - 111': '77VSM4HBGJJS', 'sujoy': 'C88ZNU3AMYMU', 'Ira Deshmukh -3': '6L8RUL88B5MV', 'Tanish Ambekar - 112': 'BRXC7GM3Y6MB'}

for k, v in da1.items():
    v = re.sub(r'\n', r' ', v)
    v = re.sub(r'\n', r' ', v)
    v = re.sub(r'\n', r' ', v)
    re.sub(r'\n', r' ', v)
    re.sub(r'\n', r' ', v)
    k = re.sub(r'\n', r' ', k)
    print k + "," +  v

# da1 = {u'Saumya Marfatia 11': u'Inactive \nDOB- 30/Apr/2015', u'Ayan  kurhekar': u'Library User', u'asmi  thete': u'book   star   Renewal  25/6/16', u'Krishna Yavale -16': u'Inactive \nDOB 11/Mar/2006', u'Ishan Dhavalikar 96': u'on  hold  \nDOB 16/10/2010\nRenewal 9/7/2016', u'Shardul Bali -27': u'inactive card to be returned', u'Akshar Bhardwaja -7': u'Inactive DOB- 6/Feb/2011', u'Anoushka Paithankar -82': u'BookStar \nDOB 6/2/2011\nRENEWAL4/7/2016', u'Hritvi Kogje -79': u'BookStar on hold 2 month DOB 29/Jan/2011\nRenewal 1/4/2016', u'Ashutosh Joshi -47': u'book  star  \nDOB - 16/Nov /2011  Renewal  6/8/16', u'Ishan Diwan -62': u'Playful\nDOB 7/Mar/2009 Ishan \nDOB 13/Mar/2012 Shaunak\nRenewal 4/7 /2016', u'Avanish. Ponde': u'book star renewal 13/7/16', u'Tejaswini Bidve -78': u'BookStar  \nDOB :15/Oct/2004\nRenewal: 28/4/2016', u'Sanika Kelkar -15': u'Book Star on hold\nDOB -25/Jan/2009', u'sara harari 97': u'BookStar \nDOB 22/august/2006\nRenewal 10/10/2016', u'Aadi Dharwadkar -110': u'BookStar \nDOB 12/5/2011\nRENEWAL 14/7/2016', u'aarushi  gudepkar     121': u'book  star                                                    DOB 13/3/2006                                         Renewal  5/5/16                                ', u'Sanskruti Joshi -33': u'Book Star \n On Hold DOB -10/Jun/2009', u'Shruti Pandit -23': u'Book Star \nDOB- 7/Dec/2004\nRenewal 30/07/2016', u'hritvik borgaonkar -90': u'BookStar \nDOB 19/01/2013\nRenewal 1/8/2016', u'Siddharth Chakravarty': u'Library User', u'Aarya Sarpotdar -46': u'inactive \nDOB -30/May /2007', u'Rujuta Rajadnya -17': u'Book Star \nDOB- 9/Aug/2007\nRenewal 28/4/2016', u'jessica  mayur': u'Library User', u'Aryan Chandorkar -5': u'BookStar \nDOB.       23/May/2010 \nrenewal 16/5/2016  on  hold  20   june', u'Devika Wagh -75': u'inactive \nDOB 11/10/2011', u'Krushna Sahoo -86': u'inactiv  DOB 4/5/2010', u'Purva Oak -106': u'BookStar \nDOB 22/04/2005\nRenewal 30/07/2016', u'Soham Penurkar': u'book  star    Renewal  6/10/16', u'Prashant Jagadale': u'Library User', u'Riya Patwardhan -89': u'BookStar \nDOB 1/3/2006\nRenewal 1/1/2017', u'Devashree Agate -53': u'BookStar \nDOB 14/Oct/2006\nRenewal 23/Jan /2016', u'Arjun Neurgaonkar -8': u'Book  Star  \nDOB- 26/Jan/2012\nRenewal : 22/07/2016', u'Kaivalya Kelkar 98': u'inactive DOB 10/8/2012\n', u'Gargi Pingle - 103': u'BookStar \nDOB 29/11/2007\nRenewal 25/8/2016', u'Meera  Mathkar  ': u'DOB-02/8/2011   Renewal 19/7/16', u'swara   joshi    129': u' book star  DOB-27/8/2007                                         Renewal    16/6 /16', u'Ishan Roy': u'on  hold  book  star  DOB 27/6/2014                        Renewal  2/6/16', u'Sanaa Bhave -59  ': u'BookStar  on hold  2 m\nDOB 22/Jan/2013\nRenewal 29/3/2015', u'Amala Purandare -81': u'BookStar \nDOB 9/2/2001\nRenewal 4/7/2016', u'Sanvika Chavan -22': u'Book Star \nDOB- 6/Jul/2012\nRenewal 1/5/2016 ', u'Shardul Salunkhe -36': u'Book Star  DOB -17/Apr/2006\n renewal 6/5/2016', u'Aditya Vanjari -30': u'BookStar \nDOB -12/Feb/2011\n', u'Ojas Zanpure -10': u'Book Star \nDOB-17/Mar/2006\nRenewal 25/5/2015', u'Revati Divekar - 113': u'Bookstar Revati 10/8/2003 Shreedhana 5/6/2009 Renewal 12/9/2016', u'Avani Dhongde -44': u'Inactive  50 rs refund  to be given. Has not returned the card yet \nDOB -22/Oct/2008\n', u'Mridu Sharma -20': u'Book Star ??? \nDOB- 13/Aug/1988\nRenewal 30/Oct/2015', u'amod bapat -104': u'BookStar -On Hold  From 29th May DOB 23/12/2004\nRenewal 27/4/2016', u'Ananya  patil': u' book  star    DOB-24/04/16    Renewal   10/6/16', u'Gargee Nanal -24': u'Book Star - on hold\nDOB - 19/Dec/2002\n', u'Avaneesh Gogate': u'bookstar renewal 17/7/2016', u'Abhinav Pandit -38': u'inactive DOB -07/Jun/2007 card returned', u'Aditi Kudalkar  -64': u'BookStar DOB 24/May/2011\ndue: 17/3/2016', u'Saukhya Latkar  -94': u'BookStar \nDOB 6/1/2012\nRenewal 7/7/2016', u'Sharva Prabhudesai -42': u'Playful \nDOB -23/Dec/2004\nRenewal 10/7/2016', u'sharvi  kalawade': u'book  star   Renewal  28/6/16', u'Bhargav Godbole - 108': u'BookStar \nDOB 7/5/2011\nRenewal 11/7/2016', u'Avishka Sasisankar - 100': u'Playful \nDOB 17/11/2011\nRenewal: 22/4/2016', u'Avishkar Mulay': u'Bookstar renewal 18/06/2016', u'twig me test user': u'Library User', u'Sana Gadre -68': u'inactive \nDOB 15/august/2005', u'Parimal Khandewale': u'Bookstar Renewal 25/6/2016', u'sai  ware': u'book  star                                                    DOB-29/8/2007                                         Renewal  1/7/16', u'Maahi Patel -84': u'BookStar on hold\nDOB 3/Nov/2008\n Renewal 22/4/2016', u'Asya Phal -87': u'BookStar \nDOB 15/8/2012\nRenewal 10/3/2016', u'saee erande -73': u'Inactive \nDOB 21/04/2009', u'Shrikar Mudpe -54': u'BookStar DOB: 9/May/2014 Renewal 4/7/2016', u'Arjun Pandit -83': u'BookStar  DOB 2/July/2013\nRenewal 4/7/2016', u'Mrunal Maharanwar': u'inactiv    card    returned', u'\nAnuj Gulavani - 9': u'Book Star    on  ohld  DOB- 28/May/2004\nRenewal 1/april/2016', u'pranav gholkar -72': u'book star- on hold\nDOB 19/January/2008\nRenewal 25/1/2016\nmembership on hold 20 Jan 2016 ', u'SHRI': u'library user', u'rishabh  joshi': u'inactiv DOB-8/12/2010  card  returned', u'Advika  pande': u'book  star  DOB-15/11/2008                      Renewal  2/8/16', u'Shirin Chivate -12': u'Book Star \nDOB- 5/Feb/2009\nRenewal 26/4/2016', u'Ashutosh Sohani - 131': u'book star renewal 18/6/2016', u'Samradnyee Joshi - 29': u'Book Star \nDOB - 11/May/2013\nRenewal 3/8/2016', u'Aastha  batheja': u'book  star  Renewal 3/7/16', u'Shriyan Gholap -88': u'BookStar \nDOB 6/01/2009\nRenewal 18/03/2016', u'Aarav Khangan - 99': u'inactiv   card  returned', u'Aarav  gulavani': u'boo  star  DOB 27/7/2014  Renewal  9/8/16', u'Nandita Nagarkar -61': u'inactive \ndob 4 Jan 2008', u'Swaraj Narkhede -69': u'Playful \nDOB: 16/Jan/2015\nRenewal: 14/08/2016', u'Anushka Sahasrabudhe -45': u'inactive \nDOB - 22/Jan/2005\n', u'Anay  Agarwal -25': u'inactive \nDOB  25 /Sep/2009', u'Padmaja Udar -13': u'Book Star \nDOB-17/Mar/2006\nRenewal 26/5/2016', u'riddhi walimbe -77': u'BookStar \nDOB 19/09/2004\nRenewal 26/5/2016', u'Tanvi  pawar': u'boo  star   deposit  1400  4  book   Renewal  25/7/16', u'Dhruv / Pralhad gokhale': u'  Book  star   DOB-17/4/16                                                Renewal  23/6/16', u'asmi  govilkar': u'book  star                                                    DOB-6/feb                                                   Renewal  30/8/16', u'sahil vaidya -65': u'Bookstar DOB sahil:- 15/09/2006\n          ria:- 10/01/2011\nRenewal 6/8/2016', u'Hridaan Amit Padve -92': u'All rounder  4 Books or 3 Books and 1toy\nDOB 9/2/2012\nRenewal 6/7/2016', u'Amruta  pawar': u'book  star  DOB-4/2/2009       on  hold                   Renewal 2/7/16', u'Tanishka  Hudlikar': u'book  star   Renewal  2/8/16', u'Neeraja  kittur': u'book  star   Renewal  27/7/16', u'Rama  deshpande': u'book  star   DOB-5/11/2005        Renewal  27/8/16', u'Aarohi Dnyate': u'bookstar renewal 2/8/2016', u'jaee  kale     125': u'book  star                                                   DOB-3/2/2004                                            Renewal   12/7/16', u'Sukrut Kulkarni -31': u'Book Star \nDOB - 11/Aug/2008\nRenewal 4/8/2016', u'Aayush Daflapurkar -43': u'Book Star \nDOB -1/Dec/2009\nRenewal 6/3/2015', u'Darshan Narendra -18': u'Book Star \nDOB- 24/Sep/2004\nRenewal 28/05/2016', u'Anushka Dandekar -56': u'BookStar \nDOB 19/Oct/     2011\nRenewa    28/05/2016', u'Rishab  pillai  151': u'book  star  DOB-22/10/2006  Renewal  18/6/2016', u'Tejas Kavishwar -35': u'Book Star on hold from 24 dec\nDOB -13/Nov/2009\nRenewal 3/Jan/2015', u'Aaradhya Bhat': u'Book Star membership on hold from 18 nov\nDOB- 20/Jan/2012\nRenewal 1/11/2015', u'Shivansh Gogawale -50': u'Book Star \nDOB - 07/May/2013\nRenewal  25/5/16', u'Arjun Chakravarty ': u'Book Star', u'Shreesh Natu -91': u' on  hold  BookStar \nDOB 2/jun/1010\nRenewal 25/7/2016', u'Rohan  Natekar': u'book  star   DOB-13/6/2006   Renewal   12/7/16', u'Arpita / Mrunmayee Kulkarni -107': u'BookStar \nDOB arpita 25/3/2005\nMrunmayee 15/7/2009\nRenewal: 6/4/2016 suspended for 1 month\n', u'Aryan Toro -34': u'Inactive\nDOB -19/Feb/2008', u'Mrudani Pimpalkhare -60': u'BookStar \nDOB 24/Mar/2015\nRenewal  31/3/2016', u'Aditya Grover -63': u'bookstar \nDOB 14/august/2005\nRenewal 4/jun /2016   on   hold', u'Samruddhi Joshi -21': u' bookstar for a month\nDOB- 28/May/2004\nRenewal 1/6/2016 deposit with us 1100', u'Aahaan Nandimath -66': u'BookStar \nDOB 1/06/2006- Aahaan\n        20/06/2013-agastya\nRenewal: 07/june/2016', u'Yashashree Samb -40': u'inactive -card not returned\nDOB -2/sep/2006', u'Arnav Shah -14': u'Book Star \nDOB- 11/June/2004\nRenewal 28/10/2016', u'tanvi kesarkar -76': u'BookStar from 12/3/2016 \nDOB 8/12/2004\nRenewal 11/9/2016', u'Advait Naik - 130': u'Bookstar Dob 16/02/2011 renewal 17/7/2016', u'purti  karmarkar': u'book  star     Renewal 22/7/16', u'Adish Patukale - 109': u'BookStar\nDOB 25/11/2011\nRenewal 11/7/2016', u'Rudra aurangabadkar': u'inactiv  DOB-11/3/2006 card returned', u'ishan   sonsale 132': u'book  star                                                    DOB-1/3/2009                                              Renewal  19/5/16', u'Ahaan Damle ': u'book star                                           DOB-30/11/2010                                              Renewal 15/6/16', u'Aaradhya / Adhyayan Bansod': u'bookstar DOB aaradhya 25/08/05 adhyayan 04/10/11 renewal 19/05/2016', u'sia  bramhankar': u'book   star    Renewal  29/7/16', u'Anerie  shah': u'Renewal 5/5/16', u'ojas kulkarni _ 105 ': u'BookStar  \nDOB 11/04/2013. Renewal 14/7/16', u'Aditya Dhondse -32': u'Book Star \nDOB - 31 / Mar/ 2007\nRenewal 4/5/2016', u'Aryan Joshi  95': u'BookStar on hold \nDOB 1/6/2005\nRenewal 8/4/2016', u'kabir  karlekar': u'book  star  Renewal  3/7/16', u'sashwat  jaiswal    133': u' Book  star                                DOB-19/7       Renewal  20/7/16', u'Soham Karanjkar -6': u'Book Star  \nDOB- 23/Aug/2005\nRenewal 23/08/2016', u'Kaveri Joshi 102': u' inactive  DOB 26/6/2015\n  card retuned', u'owi bagul -71': u'Inactive Refund Given Card Returned DOB 3/July/2006', u'Soham Bharamgonde': u'Bookstar', u'Reyansh Bhide -51': u'Playful\n on hold from 17th March Hrugved DOB:20/Feb /2006\nReyansh DOB: 20/Jul/2011\nRenewal 20/03 /2016 ', u'manasi   kondejkar': u'Library User', u'Rishabh  ghate': u'book  star   Renewal 28/7/16', u'Saket   Gadre   124': u'book  star                                                    DOB-4/1/2010                                            Renewal  11/8/16', u'Siya Shejwalkar -57': u'inactive \nDOB 8/Jan/2014', u'sonal   mahajan': u'book  star Renewal 28/7/16', u'swara  Gurav': u'book  star   Renewal  15/7/16', u'naren chandekar -74': u'BookStar \nDOB 18/3/2011\nRENEWAL 23/6/2016', u'Riya Kulkarni -80': u'inactive \nDOB 25/Dec/2001', u'Reyansh   palsule': u'inactiv   card  returned', u'Nimit Raje -58': u'BookStar  DOB 13/Mar/2012  Renewal   24/7/16', u'Ishan Nerkar -41': u'Book Star \nDOB -29/Jan/2008\nRenewal 9/9/2016', u'Mallika Datar -19': u'BookStar \nDOB- 7/Sep/2013\nRenewal 6/5/2016', u'Satyen Pingale': u'Renewal   4/6/2016', u'Saket Mhaske 101': u'book star\nDOB 19/01/2011\nDue 23/02/2016', u'Siya Mulay -49': u'inactive \nDOB -23/Jan/2008\nRenewal ', u'Asmi Sapale -39': u'on  hold  Book Star\nDOB -6/may/2013\nRenewal 20/7/2016', u'sanjyot  nanajkar   122': u'book  star                                                    DOB-15/3/2008                                          Renewal  7/,6/16', u'Anshita Gadkari -67': u'Bookstar DOB-11/Feb/2007\n renewal 7/7/2016', u'shalmali  tambe   123': u'book  star                                                    DOB-10/10/2010                                        Renewal  9/5/16', u'pranav  deshpande  147 ': u'book   star    DOB -16/10/2009     Renewal 7/6/16', u'Utkarsh Shetty': u'book  star    Renewal  3/6/16', u'kapil': u'android Developer', u'Nakshatra Raje -28': u'Book Star - on hold\nDOB - 21/ Jan/ 2009', u'Rama  Shejwalkar -48': u'Book Star  on hold\nDOB - 8/Oct /2009\n', u'Prachi Bhatt -52': u'BookStar \nDOB 21/Oct/2015\nRenewal 21/8/2016', u'Abha Ashturkar -70': u'BookStar \nDOB 31/Jan/2015 Renewal 10/8/2016', u'Dhruv Manurkar -37': u'inactive \nDOB -20/Mar/2008', u'Radha Joshi -85': u'inactive \nDOB 25/Apr/2011', u'shruti srinivasan -93': u'BookStar \nDOB 24/12/2005 shruti\n21/7l/2011 Siddharth \nRenewal 6/7/2016', u'Nidhi Baadkar -55': u'BookStar On Hold DOB 28/Sep/2006\nRenewal 3/4/2016', u'Nitin M': u'Library User'}


#
# url = LL.BASE_URL + "library/rental/" + zbotID + "/report"
# print url
# method = "POST"
#
# body = {"StartDate" : "2016-07-16" }
# # body = { }
# jsonreply = hit_url_method(body, headers1, method, url)
#
#
# print jsonreply

zviceid = "5BZK29ZZK4XQW"
zviceid = "23KBNM7BUFTYR"
zviceid = "EC5QJSKSWB3KE"
rentalFound = 0

database = {}
errorDetails = {}

headers, headers1 = LL.req_headers()

with open("/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/millennium/script_inputs/usercsv.csv", 'w') as wf:


    with open(filename, 'r') as f:
        data = csv.reader(f, delimiter=',')
        # print data
        for row in data:
            # print row
            zviceid = row[1].strip()

        # ### to find the renter of a book
            jsondata = getBaseStructure(zviceid, headers1)
            # print jsondata['reply']
            jsonreply = json.loads(jsondata['reply'])
            print "=========DATA=========="
            if jsonreply['error']:
                print jsonreply['error']
                print zviceid
                print jsonreply
            # for k, v in jsonreply.items():
            #     print k
            try :
                jsonreply = jsonreply['data']['elements'][0]
                print (jsonreply['title'], jsonreply['content'])
                contents = re.sub(r'\n', r' ', jsonreply['content'])
                database[jsonreply['title']] = zviceid + "," + contents
                wf.write(zviceid + "," + jsonreply['title'] + "," + contents + "\n")
                print database
            except KeyError:
                print "=======Keyerror======="
                print (zviceid, row[0])
                errorDetails[row[0]] = zviceid

        # # print jsondata['reply']
        # # print jsonreply['data']['title']
        # for element in jsonreply['data']['elements']:
        #     if "basecard" in element['cardtype']:
        #         print element['title']
        #     if "Rental Info" in element['title']:
        #         rentalFound = 1
        #         for action in element['actions']:
        #             if "See Renter" in action['title']:
        #                 url = action['actionUrl']
        #                 print url
        #                 method = "POST"
        #                 data = {}
        #                 jsondata = hit_url_method(body, headers1, method, url)
        #                 for element1 in json.loads(jsondata['reply'])['data']['elements']:
        #                     if "basecard" in element1['cardtype']:
        #                         print element1['title']
        # if rentalFound == 0:
        #     print "book not rented out"
        # else :
        #     rentalFound = 0
        #
        ######### end renter of a book


        #
        # url =  "http://twig-me.com/v1/zvice/interaction/23KBNM7BUFTYR"
        # method = "POST"
        # # body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_STATIC_DETAILS"}
        # body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_MODIFY_ZVICESTATIC_INFO", "validupto" : "2016-07-19", "columnid" : "ID_Validity"}
        # jsonreply = hit_url_method(body, headers1, method, url)
        # print jsonreply['reply']

        # url =  "http://twig-me.com/v1/zvice/interaction/23KBNM7BUFTYR"
        # method = "POST"
        # # body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_SHOW_STATIC_DETAILS"}
        # body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_MODIFY_ZVICESTATIC_INFO", "membershiptype" : "Half month", "columnid" : "ID_Type"}
        # jsonreply = hit_url_method(body, headers1, method, url)
        # print jsonreply['reply']


        # url = "http://twig-me.com/v1/zvice/interaction/A4CJ2VHTTJS9Y"
        # method = "POST"
        # body = {"username" : "Arjun", "interactionID" : "CommonInteraction_INTERACTION_TYPE_SEARCH_LIB_USER_PROFILE", "expired" : "false", }
        #
        # jsonreply = hit_url_method(body, headers1, method, url)


        # print jsonreply['reply']

        # url = "http://twig-me.com/v1/zvice/interaction/A4CJ2VHTTJS9Y"
        # method = "POST"
        # body = {"interactionID":"CommonInteraction_INTERACTION_TYPE_GET_USERPROFILE_CARDS","userprofileid":"BPPZHKMBBKLB3"}
        # jsonreply = hit_url_method(body, headers1, method, url)

    #
print "============ error details ==========="
print errorDetails
for k, v in database.items():
    v = re.sub(r'\n', r' ', v)
    v = re.sub(r'\n', r' ', v)
    v = re.sub(r'\n', r' ', v)
    re.sub(r'\n', r' ', v)
    re.sub(r'\n', r' ', v)
    k = re.sub(r'\n', r' ', k)
    print k + "," +  v

# print jsonreply['reply']
user = "sujoy@zestl.com"
pwd = "HOTshot09"
recipient = "archanahp14@gmail.com"
subject = "User data"
# body = jsonreply['reply']
body = database

send_email(user, pwd, recipient, subject, body)