import json
import logon as LL
import common as CM

# BASE_URL = "http://twig-me.com/v11/"  ### dev server
# BASE_URL = "http://35.154.64.119/v13/"  # Test server
BASE_URL = "https://twig.me/v13/"    # prod
# zviceID = "WKMUYXELA9LCC"  # gene path
# zviceID = "AQSYFC5AQY7X8"   # Future retailer
# zviceID = "57J947VG9CCSK"   #Project demo Test server
# zviceID = "9SEUR88JAVLN6"   # haldiram
# zviceID = "XAJVCAMQQQD4D"
zviceID = "7ZSPXCM7THGPK"
email = "admin@zestl.com"
pwd = "TwigMeNow"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

method = "POST"
# url = BASE_URL + "workflow/" + zviceID
# body = {}
# body['title'] = "Minal"
# body['workflowtypeid'] = "1"
# jsonresponse = CM.hit_url_method(body, headers1, method, url)
# print jsonresponse

#******************************* Adds a Workflow Type ********************

url = BASE_URL + "workflow/" + zviceID + "/type"
body = {}
body['title'] = "Type 1"
jsonresponse = CM.hit_url_method(body, headers1, method, url)
print jsonresponse