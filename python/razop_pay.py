import logon as LL
import common as CM

import password as PP
SERVER = "https://twig.me/"
# SERVER = "http://twig-me.com/"
# SERVER ="http://35.154.64.119/"
version = "v9/"
BASE_URL = SERVER + version
hasHeader = "Y"
zviceID = "3NSA4U2P9CFRK"

email = "admin@zestl.com"
pwd = PP.pwd
# pwd = "TwigMeNow"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
body = {}
method = "POST"
url = "https://twig.me/v9/razor_pay/enable/" + zviceID
# url = "http://twig-me.com/v9/razor_pay/disable/" + zviceID
# url = "http://35.154.64.119/v9/razor_pay/enable/" + zviceID
print url
jasub = CM.hit_url_method(body, headers1, method, url)
print jasub