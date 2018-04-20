
import logon as LL
import common as CM
import json
import password as PP
# SERVER = "http://35.154.64.119/"  # test
SERVER = "http://twig-me.com/" #Production
version = "v13/"
BASE_URL = SERVER + version

zviceID = "83H6LVUBRXWZ5"

email = "admin@zestl.com"
pwd = "TwigMeNow"
# pwd = PP.pwd

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
# jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)


method = "GET"
body = {"condition" :
            {"Title" :{"mandatory" : True,"value" : "14 sep pushakar"},"EmailID" :{"mandatory" : True,"value" : "Minal@zestl.com"}} #  here "True" means exact matching


    ,"min_non_mandatory_match" : 0}

url = BASE_URL + zviceID + "/getMatchingBUs?filter=" + json.dumps(body)
# url = "https://twig.me/v8/products/8LS8752NB6U5Y/maxproducts/30"
jasub = CM.hit_url_method(body, headers1, method, url)
print jasub