
import logon as LL
import common as CM
import json

SERVER = "http://twig-me.com/" #Production
version = "v13/"
BASE_URL = SERVER + version
zviceID = "WHGJ7HTVTDFH3"
email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

body = {}
method = "GET"
url = BASE_URL + zviceID + "/formdetails/" + str(12)
jasub = CM.hit_url_method(body, headers1, method, url)
jasub = json.loads(jasub)
print jasub