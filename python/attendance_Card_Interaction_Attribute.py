
import logon as LL
import common as CM
import password as PP
SERVER = "http://35.154.64.119/"  # test
# SERVER = "https://twig.me/" #Production
version = "v8/"
BASE_URL = SERVER + version

zviceID = "6CPYM6TWS9NSA"

email = "admin@zestl.com"
pwd = "TwigMeNow"
FSCardID = 808
# pwd = PP.pwd

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
res_1 = {}
res_1['display'] = "No of Bottles Delivered"
res_1['type'] = "int"
res_1['id'] = "bottles_delivered"
res_1['attrtype'] = "dropdown"
res_1['allowed_values'] = [1,2,3,4,5]

body = {}
body['display'] = "No of Bottles Returned"
body['type'] = "int"
body['id'] = "bottles_returned"
body['attrtype'] = "dropdown"
body['allowed_values'] = [0,1,2,3,4,5]

res = {}
res['display'] = "Dosa & Idli Combo"
res['type'] = "string"
res['id'] = "dosa_idli_combo"
res['allowed_values'] = ["true" , "false"]
res['attrtype'] = "checkbox"
body = [body,res,res_1]
print body
method = "PUT"
url = BASE_URL + zviceID + "/fastscan/attendance/" + str(FSCardID) + "/commentattrib/config"
jasub = CM.hit_url_method(body, headers1, method, url)
print jasub