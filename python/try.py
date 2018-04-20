



# import shelve
import traceback
import signal
import os
import logging
import time
import json
import datetime
import settings as s
import csv
import wfe_parser as WF
# from datetime import datetime,datetime
# from datetime import datetime


# field_dict = {"name":"User Name","email":"Email ID","department":"Department","role":"Role"}

# print s.field_dict['name']

arr = ["Sub Flows","WFEs"]
filename = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/Test_Server_workflow/Haldiram/WFE_subflow_electrical_1.csv"
subflow_name = "Transformer"
val_1 = WF.parse_wfe_list(filename)
print val_1

for elm in val_1['wfes']:
    elm1 = elm.split("_")
    elm_2 = subflow_name + "_" + elm1[1] + "_" + elm1[2]
    print elm_2
    arr.append(elm_2)
# print arr
arr.append("Dept WFEs")
for elm in val_1['deptwfes']:
    arr.append(subflow_name)

print arr

filename = 'C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/' + subflow_name + ".csv"
with open(filename, 'w') as wf:
    for add in arr:
        wf.write(add + "\n")


# with open(filename, 'r') as rf:
#     data = csv.reader(rf, delimiter=',')
#     wfe = {}
#     for row in data:
#         if row == "subflow":
#




#
# def opp(a,b,d,c = None):
#     f = a + b
#     print f
#     print c
#
#
#
# a = 2
# b = 4
# d = 6
#
#
#
# result = opp(a,b,d,c = "minal")
#
#

# abc = "ABCd(mi(n)al)"
#
# abb = abc.split("(")
# print abb
# abb1 = abb[0]
# print abb1
# abb2 = abb[1]
# print abb2


# first_date = "2018-02-15 06:53:41"
# last_date = "2018-02-15 06:41:51"


# val = 123.87656
# val1 = int(val)
# print val1



#
# fmt = '%Y-%m-%d %H:%M:%S'
# d1 = datetime.datetime.strptime(first_date, fmt)
# d2 = datetime.datetime.strptime(last_date, fmt)
# d1_ts = time.mktime(d1.timetuple())
# print d1_ts
# d2_ts = time.mktime(d2.timetuple())
# print d2_ts
#
#
# val = d2_ts - d1_ts
# val = val / 60
# print val
# val = abs(val)
# print val
#
# val1 = 500
# val3 = val1 - val
# print val3
# pid = os.getpid()
# print pid
#
# s_date = '2018-02-23'
# date_1 = datetime.datetime.strptime(s_date, "20%y-%m-%d")
# # print date_1
# days = 20
# end_date = date_1 + datetime.timedelta(days=days)
# print end_date



# start_date = "2010-10-11"
# date_1 = datetime.datetime.strptime(start_date, "20%y-%m-%d")
#
# end_date = date_1 + datetime.timedelta(days=10)
# print end_date


# import csv
# inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
# with open(inputFile, 'r') as f:
#     d_reader = csv.DictReader(f)
#
#     #get fieldnames from DictReader object and store in list
#     headers = d_reader.fieldnames
#
#     for line in d_reader:
#         # print value in MyCol1 for each row
#         print(line['Name'])
#     print(headers)
#     # for sub in headers:
#     #     print sub





# result = {"error":"false","message":"Reading Report generated successfully for 2018-01-29","report_data":[["Book TagID","Book Title","User TagID","User Title","Reading Start Time"],["249WDQ26T2VFV","THE ---- GIRL","9M4QRKKVKVXTF","SAYURI PATIL [MC89]","2018-01-29 03:31:16"],["6PFWS2FWPD24D","9788184773262","E5TMFTWLFEXBB","ARYAA BEDEKAR [MC98]","2018-01-29 03:31:39"],["249JRW4GNET66","HEIDI","9ECBCQ6HC6LCH","RIA MODAK [MA16]","2018-01-29 03:31:56"],["6ZEAG25QP482Z","Diary of a Wimpy Kid","DB8ELTG47XX7P","NUPUR SAPAR [MD29]","2018-01-29 03:32:13"],["AHQJEQDE3EFPY","I'm No Fraidy Cat (Catkid)","DBJLEW7LDRBYN","SONIYA HAROLIKAR [MC71]","2018-01-29 03:32:29"],["2KTTK8DXX42QK","Hakka & Bukka (795)","7XW2CPHMFGFKV","AREEN PARAB [MA58]","2018-01-29 03:33:13"],["3T77BS85C75G8","Rana Kumbha (676)","F88WXRYK27C2X","RANVIRSINGH RAJPUT [LB46]","2018-01-29 03:33:24"],["4G5FX6585LCQN","?","WHKMYC9WLTTDG","DEV NAIK [MB49]","2018-01-29 03:34:49"],["5UCJWTDVNMZJM","My Best Friend Is Invisible (Goosebumps, No 57)","F2T6GTWP2WQB7","ARYAN VAZE [MD49]","2018-01-29 03:35:14"],["7DHUGG53W5ELE","9788184773095","4E6K3XZMDXSM2","RADHIKA KUNTE [MD09]","2018-01-29 03:35:25"],["6MEMULVWAWVQG","Charlie and the great glass elevator","4J2N855U9JJKE","GUNJAN BHAMARE [MC87]","2018-01-29 03:36:09"],["FFXDTFL6NBZ9M","The Secret Island (Secret Series)","FCR8Q3MSMKRLH","SHALMALI SALASKAR [MD06]","2018-01-29 03:36:20"],["5XZE75BH48U2M","Sukanya the Princess Who Married A Sage","63WYHVY32CNRM","RIYA ARANAKE [MB11]","2018-01-29 03:36:31"],["DJJML226BK3FS","You're Plant Food! (Give Yourself Goosebumps, No. 30)","8KZGX92SA2FJA","ADITYA BORAWAKE [MC73]","2018-01-29 03:38:02"],["3R8T5YMLZW22J","The Priceless Gem (672)","FN472C92H2LPF","MOHINI YATNALKAR [MB36]","2018-01-29 03:38:14"],["8EGTURJZY3NLS","Thea Stilton and the Mystery on the Orient Express","5AF4YSLUNANW9","SHARVARI HAJARE [LB24]","2018-01-29 03:39:14"],["4YYH3XVDTME3P","WHY WE ARE WHERE WE ARE","C8KDGR8F7ALV9","GAYATRI JOSHI [MA86]","2018-01-29 03:39:34"],["EFEN52VZ3RJDZ","Funny and Funnier","WV786MF27SC6A","TITIKSHA PAWAR [MA61]","2018-01-29 03:39:44"],["XQ7J8RGFHLBTM","Robinson Crusoe : Om Illustrated Classics","CQK5YPJYDUYBN","SHRAVAN SHINDE [MC46]","2018-01-29 03:41:26"],["6TQG5BTSEM8BD","The Rise of Sivagami (Baahubali: Before the Beginning, Book 1)","3XJSS9LK2VUZS","SHUBHAM KALE [MA53]","2018-01-29 03:41:36"],["6CP5QN6S3JMA9","Puffin Lives : Subhas Chandra Bose - The Great Freedom Fighter, (PB)","XEZUZ9XYRVNAM","VEDANG BHEGADE [MB17]","2018-01-29 03:42:00"],["8HLCWLS3GQ7HJ","9788176553650","AWZQ2T7Y9QWU9","VARAD AGRAWAL [MA15]","2018-01-29 03:48:12"],["6VUH4G4DYB7NC","?","6BQQVJ9NMGP78","SHUBHAM BORHADE [KD76]","2018-01-29 04:15:08"],["FDMDLXN2ZBRPQ","Vasavadatta (674)","E4D2CSNP4VT8B","OWEE JOGDAND [KD59]","2018-01-29 04:15:18"],["X9S7AEVMTNMG5","House of Cards","FR9S2JLMPDDJR","RASHI MALWADKAR [KC82]","2018-01-29 04:15:32"],["EFDWVSS3PDNBH","9788184773095","C8KE9H9FBYEHP","PALASH DIXIT [KC58]","2018-01-29 04:15:42"],["3RP8BUEWFP897","The Prince And The Magician (743)","C9438SNU94F3H","SANIYA PAWGI [KD69]","2018-01-29 04:15:52"],["CTY7W4KMYYD7N","Geronimo Stilton Cavemice #10: My Autosaurus Will Win","2YL7V6B9T9HJ6","RAJVIRSINGH RAJPUT [KA29]","2018-01-29 04:16:04"],["CF8LXY6M8ABXS","Jagannatha Of Puri","3Y9A83Q6DRSS7","NAVYA SHRIKHANDE [KA18]","2018-01-29 04:16:18"],["CZN4BTQ6REHXW","Friends And Foes: Animal Tales From The Mahabharata (609)","4JKW4M7YSM4LC","TANYA TALWALKAR [KD66]","2018-01-29 04:16:35"],["FFC2WV8FB6WN6","Padmini (605)","4FA5U9D5BDXG2","GAYATRI MUZUMDAR [KC17]","2018-01-29 04:16:48"],["D6BS72J3XSBDT","The Secret Diary of the World's Worst Friend","56NBTT35Z3FAG","ARYAN KARVE [KD94]","2018-01-29 04:16:56"],["8EATFA67DE8LL","Asterix and the Falling Sky: Album #33 (Asterix (Orion Paperback))","DLEZ97GZHX8DP","AARUSH BALKUNDI [KC03]","2018-01-29 04:17:11"],["9XFXCBKE6NF2F","866119574","E4UVLW3XM95FT","ANAY KATE [KD68]","2018-01-29 04:17:25"],["7P9MQD3HBT6GJ","Folktales Of Africa","WX955G78TWUCK","RIYAA CHANDAK [JB67]","2018-01-29 04:17:38"],["8SWYKJ6HYSSC8","EVE OF THE EMPEROR PENGUIN","7G73TEPWYESJ3","ANUSHKA SOMWANSHI [KB66]","2018-01-29 04:17:55"],["FECQHHLZASU9J","Dark Day in the Deep Sea","F985FW5B3DT68","ADITI DHONE [JB22]","2018-01-29 04:18:07"],["8R82N94YTWBDL","HAUNTED CASTLE ON HALLMASS EVE","9JKCJ2UYK6TPB","SANIYA JOSHI [KB20]","2018-01-29 04:18:20"],["4LWP2X5USRMNF","ANGEL FIRE","2NAHQGL2XWAT9","PRACHI ASABE [KD53]","2018-01-29 04:18:33"],["E5TMGR7PU4T8P","The Famous Five 6: Five on Kirrin Island Again","22BG9GRADCD77","DHRITI SHAH [KA04]","2018-01-29 04:18:43"],["47VR8E5SYB8TW","Xtreme 3D Space (Mission Xtreme 3D)","5JM6VNVFQJBJR","ANUSHA KARVE [KD95]","2018-01-29 04:18:53"],["FEGS48AXS8XUE","Creepella Von Cacklefur, No. 5: Fright Night (A Geronimo Stilton Adventure)","6ABT9XLS2UC7D","SAMEEHAN NAGARKAR [KA88]","2018-01-29 04:19:03"],["6NVJ7B6TWS6DJ","Mahashweta","3VMDZ6BDTAEJ8","ANVI GAYDHANI [KD17]","2018-01-29 04:19:56"],["D49TULLZXD445","Gone for Good","AW6QTGPGLFKP7","DEV  CHAVAN [KD81]","2018-01-29 04:20:06"],["5SBAB3U9GYFC4","Prince of Dorkness","FP22NAEA8L3UG","VARAD ARKATKAR [KD89]","2018-01-29 04:20:19"],["X9BR9WFMZYRBJ","Lost in Stinkeye Swamp (Give Yourself Goosebumps, No 24)","9YPBED7WNXHYY","AVANI HONAP [MD11]","2018-01-29 04:52:33"],["E7ECTK896S4PA","To Kill a Mockingbird, 50th Anniversary Edition","9F2QDFJUN6G64","SWAPNA KHARE [MA10]","2018-01-29 04:52:44"],["8SC2CPZVWSHL8","THE MYSTERY OF THE SPITEFUL LETTERS","8URBW8UDNYULE","MRUNMAYEE DESHPANDE [LB57]","2018-01-29 04:53:00"],["6DNA6UP6S7UH9","Mah\u00c4\u0081r\u00c4\u0081sh\u00e1\u00b9\u00adr\u00c4\u0081ce Paksh\u00c4\u00ab","4KE77D49SGD2Q","RAJ KARLE [MC36]","2018-01-29 04:53:49"],["6LZC6UYVQZQRU","The 39 Clues","9HQ2QCL5LMURW","EESHAN THATTE [MB95]","2018-01-29 04:53:57"],["68QSHA4QW3UVS","9788179253960","8RR9FAQTLPCNV","OMKAR DESHPANDE [MD22]","2018-01-29 04:54:12"],["FDCM6KXUWGM2Q","One False Note (The 39 Clues, Book 2)","E2KCKUVTU37E9","PAARTH MAHAJAN [MC59]","2018-01-29 04:54:28"],["6LGCUM5JCPSZH","SECRET SEVEN: 04: SECRET SEVEN ON THE TRAIL","EXZ67C6DBXC84","MIHIKA NANGARE [PB41]","2018-01-29 04:54:46"],["CVXWXDLRDJW8P","Five On A Treasure Island","CDK2Q5FKXTFK4","VAIDEHI JALWADI [LB89]","2018-01-29 04:55:40"],["4Q687E7TLVRZ2","The Luminous Life Of - Atal Bihari Vajpayee","FEK3R88BAWVEZ","ANUJ YADAV [MC91]","2018-01-29 04:55:51"],["5QZCJL4VHCVGT","Harry Potter and the Deathly Hallows. Signature Edition (Book 7)","87UP2LZ3U5MPQ","SHAUNAK SAKHADEO-JOSHI [MB10]","2018-01-29 04:56:09"],["CNF3BQ3PJFQ69","Naughtiest Girl is a Monitor","9KHRYZ6D84LDV","RUJUTA PURANDARE [MB59]","2018-01-29 04:56:29"],["7DNX86XE4N966","9788184776188","5SZ99NKY438M3","SAI PATIL [MB77]","2018-01-29 04:56:38"],["CWSFD9N5Z6QMN","The Famous Five 3: Five Run Away Together","XE7A3D4V5GV9G","RUJULA BHAGWAT [MD48]","2018-01-29 04:56:50"],["5URSC5X2YYYZK","It Came from the Internet (Give Yourself Goosebumps, No. 33)","92MXNE3DU5XTH","AADI SARDESAI [MC50]","2018-01-29 04:56:58"],["8CX6CRV2CHVWF","Asterix And The Great Crossing 22","9VLFESE8TUC9F","ARUSH BADHE [MC95]","2018-01-29 04:57:08"],["DJ6JRDJ7SBAZ2","Zapped in Space (Give Yourself Goosebumps, No 23)","D9QQLVVQQSSRF","RANVEER  SINGH RANDHAWA [MB69]","2018-01-29 04:57:18"],["7YPNYDVFHXYBV","POPULAR MECHANICS DO IT YOURSELF","CPN3TDGXTHY4J","KARISHMA CHIDGOPKAR [MA89]","2018-01-29 04:57:34"],["DHVEMER82BB6R","Welcome to Dead House (Goosebumps, No. 1)","WL44LQF5B6U5E","AMAIDHI NANGARE [PB40]","2018-01-29 04:57:47"],["7D2R9S6XS8VH6","Keeping Secrets (Main Street #7)","87UVW7QMJLNVL","RASHMI PHADAKE [MC62]","2018-01-29 04:57:57"],["7F5P7VKKG5ZS4","Keeping Secrets (Main Street #7)","WGA845X8TWEQ8","PRAJAKTA BAPAT [MA08]","2018-01-29 04:58:07"],["DWV5AG37UXD2N","Pippa Morgan's diary","WDXZYX4D6BJLE","NIHARIKA GANU [MC10]","2018-01-29 04:58:17"],["2RHD2FF4986D4","Scholastic Discover More: Planets","2YPCLRJYMC7LV","JAY PENDSE [MA39]","2018-01-29 04:58:30"],["3FMZY2XHVR35Z","Into the Twister of Terror (Give Yourself Goosebumps, No 38)","28G84LF9UJJW8","VED BHAWALKAR [MC29]","2018-01-29 04:58:38"],["44XVGQN29QUW2","Danger Time (Give Yourself Goosebumps)","X2G4BW2B7N8AN","VIRAJ JADHAO [MA55]","2018-01-29 04:58:47"],["829PXKPP7WYWW","Blast of the sun..","5HVGLMJGKAQNS","ARYAN BHOSALE [MB64]","2018-01-29 04:59:08"],["6CYTSUPA5UMZ6","Tiger And The Woodpecker (622)","8LKUJ8LQ38KD3","ANISH PURANIK [MC80]","2018-01-29 04:59:16"],["DJFHK5WJK54GZ","Welcome to HorrorLand: A Survival Guide (Goosebumps Horrorland)","CDP8LQXEAYEE4","SUHANI BADHE [MA31]","2018-01-29 04:59:25"],["47TJB6PMAXKMP","Welcome to HorrorLand: A Survival Guide (Goosebumps Horrorland)","FWJ3HPAVDDEFF","NEHA CHAWARE [MB63]","2018-01-29 04:59:33"],["E2HRGH6DPA8XG","blast off mars","XX8ATCA2VLGV6","ARNAV KARWA [MB48]","2018-01-29 04:59:49"],["XYHPGCE6QR7N5","LIFE Seeing is Believing: Amazing People and Places From Around the World","CFL5RRCVTH8YL","ARNAV GOGATE [MD07]","2018-01-29 05:00:00"],["9W5A3RX38MNW6","07009702247","3AB4GFCV33ZXL","ISHA JADHAV [MC11]","2018-01-29 05:00:12"],["7AUE9HKCL7N6B","Geronimo's valentine","7KHRDQ5J59NYB","POORVA RATHI [MB40]","2018-01-29 05:00:32"],["D5SHGWJA3AUTH","Thick as Thieves: Tales of Friendship","3V4V3EEZRCKCP","AKSHADA THAKARE [MA14]","2018-01-29 05:00:49"],["8EATFA67DE8LL","Asterix and the Falling Sky: Album #33 (Asterix (Orion Paperback))","XNLY6UGHED55T","SHREYAS SANE [MB74]","2018-01-29 05:06:30"],["3FVWADEC75ZFU","Blast Off! Let's Explore Saturn","XX8ATCA2VLGV6","ARNAV KARWA [MB48]","2018-01-29 05:08:42"],["CR4N3QH4KTM4L","Birds of Our Neighbourhood","8RR9FAQTLPCNV","OMKAR DESHPANDE [MD22]","2018-01-29 05:13:37"],["ANPYEQJAN255S","Blast off ! Let's explore Comets & Asteroids","XX8ATCA2VLGV6","ARNAV KARWA [MB48]","2018-01-29 05:18:57"],["6CYTSUPA5UMZ6","Tiger And The Woodpecker (622)","XNLY6UGHED55T","SHREYAS SANE [MB74]","2018-01-29 05:23:18"]]}
# print result
#
# result = json.loads(result)
# for a in result['report_data']:
#     print a











#************** testing for edit form card *********************************
import logon as LL
import common as CM
import json
# import auth as AA
import csv

# SERVER = "https://www.twig.me/"
# SERVER = "http://twig-me.com/"
# version = "v13/"
# BASE_URL = SERVER + version
# zviceID = "83H6LVUBRXWZ5"    ####  minal Business ID
# email = "admin@zestl.com"
# pwd = "TwigMeNow"
# # pwd = AA.pwd
#
# headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

# try:
#     # listen()
#     invalid = True
#     i = 0
#     while invalid:
#         if i < 200:
#             print i
#             logging.exception(i)
#             logging.exception("going inside")
#             time.sleep(500.0 / 1000.0)
#         else:
#             logging.exception("number is greater")
# except:
#     logging.exception("message")



# wid = 890
# wID = wid + 100

# val = ('{:04}'.format(wID))
#
# # val = ('{:04}'.format(54325))
# print str(val)
#


#
# jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
# for a in jsondata['data']['elements']:
#     title = "adding in bulk"
#     if title == a['title']:
#         print "1st level"
#         for action in a['actions']:
#             if 'More actions' in action['title']:
#                 body = {}
#                 url = action['actionUrl']
#                 print url
#                 # url = "https://twig.me/v7/all_actions/8SFKZCV5PFAXV/form/59"
# body = {}
# url = BASE_URL + "all_actions/" + zviceID + "/form/268"
# method = "GET"
# jsonresponse = CM.hit_url_method(body, headers1, method, url)
# print jsonresponse
# for sub in json.loads(jsonresponse)['data']['ondemand_action']:
#     if "Edit" in sub['title']:
#         url = sub['actionUrl']
#         data1 = sub['data']
#         data1 = json.loads(sub['data'])
#         method = sub['method']
#         body = {}
#         body["FormDescription"] = data1["FormDescription"]
#         body["FormID"] = data1["FormID"]
#         body["FormTitle"] = data1["FormTitle"]
#         body["ZviceID"] = data1["ZviceID"]
#         body["ZbotID"] = data1["ZbotID"]
#         body["ModifiedBy"] = data1["ModifiedBy"]
#         body["DateModified"] = data1["DateModified"]
#         body["CreatedBy"] = data1["CreatedBy"]
#         body["DateCreated"] = data1["DateCreated"]
#         body["query"] = data1["query"]
#         body["Flags"] = data1["Flags"]
#         title = data1["FormTitle"]
#         zeroelem = {}
#
#         val = data1['Elements'][0]['Elements']  # This line is for taking existing elements from FORM #
#         for elm in val:
#             if "SPINNER" in elm['ElementType']:
#                 print "found"
#                 spiner = elm['Options']
#                 one = "c"
#                 spiner.append(one)
#                 elm['Options'] = spiner
#                 print spiner
#
#         passthrough = True
#         if passthrough:
#             tempAr = []
#             zeroelem["ElementType"] = "SECTION"
#             zeroelem["SequenceNo"] = 1
#             zeroelem["FieldLabel"] = title
#             print zeroelem["FieldLabel"]
#             elarray = []
#             zeroelem['Elements'] = val
#
#             tempAr.append(dict(zeroelem))
#
#         body['Elements'] = tempAr
#         print body['Elements']
#         body['DataSource'] = data1['DataSource']
#         print body
#         jsonresponse = CM.hit_url_method(body, headers1, method, url)
#         print jsonresponse



#**********************************************************************************************************************************

# pwd = os.path.dirname(__file__)
# logfile = pwd + "/pythontrylogs.log"
# logging.basicConfig(filename=logfile)
#
# def debug(sig, frame):
#     d={'_frame':frame}         # Allow access to frame object.
#     d.update(frame.f_globals)  # Unless shadowed by global
#     d.update(frame.f_locals)
#     message = "Signal received : " + str(sig) + "\n"
#     message += ''.join(traceback.format_stack(frame))
#     logging.error(message)
#
# def listen():
#     signal.signal(signal.SIGTERM, debug)  # Register handler
#     # signal.signal(signal.SIGKILL, debug)  # Register handler
#     signal.signal(signal.SIGSEGV, debug)  # Register handler
#     signal.signal(signal.SIGFPE, debug)  # Register handler
#     signal.signal(signal.SIGABRT, debug)  # Register handler
#     # signal.signal(signal.SIGBUS, debug)  # Register handler
#     signal.signal(signal.SIGILL, debug)  # Register handler
#
#
#

# # inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/my.shelve"
# myShelve = shelve.open('C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv')
# value = myShelve['a']
# value += 1
# myShelve['a'] = value
#
#
#
# #***********************
# testEX = shelve.open()
# testEX['QRCpde'] = 's'
# testEX['f'] = 'F'

# result = "Dear Student, <br> Please send your report<br> Thank you for your attention"
# print result



#*********************

# from selenium import webdriver
# driver = webdriver.Firefox()
# driver.get("https://twig.me/TwigMeWeb/index.html")
# print "going"
# # driver = webdriver.Firefox()
# # driver.get("http://www.python.org")
# # assert "Python" in driver.title
# driver.close()
# number = 65
# print('{:04}'.format(number))
# print('{:04}'.format(10))



# vaal = "minal"
# print '"' + vaal + '"' + "\n" + "thorat"


# import re

# stage = "MKT_WFE1_5A"
# st = stage.split('_')
# st = st[0]
# print st

# a = [
#       {
#         'editable': True,
#         'required': 0,
#         'type': 'CHECK_BOX',
#         'placeholder': '',
#         'label': 'abc'
#       },
#       {
#         'editable': False,
#         'required': 1,
#         'type': 'EDIT_TEXT',
#         'placeholder': 'Plz send me as default value',
#         'label': 'Comment'
#       },
#         {
#             'editable': True,
#             'required': 0,
#             'type': 'CHECK_BOX',
#             'placeholder': '',
#             'label': 'abc'
#         }
#     ]
#
#
# # a = ['a','b','c','a']
# # a = [1,2,3,2]
# b =set((a))
# c = list(b)
# print c
#***********************************************************#
# x = re.search("minal","A cat and rat can't be friends")
# print x

#**********************************************************#
# if (re.search("minal","a cat and rat can't be friends")):
#     print "found"
# else: print "not found"

#***********************************************************#
# inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/reg.txt"
# fh = open(inputFile)
# for line in fh:
#     if re.search(r"J.*Neu",line):
#         print line.rstrip()
# fh.close()
#*************************************************************#

# s1 = "Mayer is a very common  Name"
# s2 = "He is called Meyer but he isn't German."
# # if re.search(r"M[ae][iy]er",s2): print "I found one!"
# if re.match(r"M[ae][iy]er", s1): print"found"
# print "not"
#******************************************************************#

# s1 = "Mayer is a very common  Name"
# s2 = "He is called Meyer but he isn't German."
# # if re.search(r"M[ae][iy]er",s2): print "I found one!"
# if re.match(r"^M[ae][iy]er", s2): print"found"
# else:print "not"
#********************************************************#
# s1 = "55553 Mayr is a very3333333 common  Name 66"
# s2 = "He is called Meyer but he isn't German."
# s = s1 + "\n" + s2
# s = s2 + "\n" + s1
#
# print s
# print re.search(r"^M[ae][iy]er", s1)
# print re.search(r"M[ae][iy]e?r",s1)
# print re.search(r"[0-9]*",s1)

# print re.search(r"^[0-9]+ .*",s1)
# print re.search(r"^[0-9][0-9][0-9] [A-Za-z]+",s1)
# print re.search(r"^[0-9]{4} [A-Za-z]*",s1)
# print re.search(r"^[0-9]{4,5} [A-Z][a-z]{2,}",s1)
#********************************************************#
# if re.search(r"Python\.$","I like Python.\nSome prefer Java or Perl.", re.M): print "found"
# else: print "not"
#*******************************************************#
# mo = re.search("[0-9]+", "Customer number: 232454, Date: February 12, 2011")
# print mo.group()
# print mo.span()
# print mo.span()[0]
# print mo.span()[1]
# print mo
#**********************************************************#
# inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/reg.txt"
# fh = open(inputFile)
# for i in fh:
#      res = re.search(r"<([a-z]+)>(.*)</\1>",i)
#      print res.group() + ": " + res.group()
