import logon as LL
import common as CM
import password as PP
SERVER = "https://twig.me/"
version = "v9/"
BASE_URL = SERVER + version
# zviceID = "BAVZLCN4TNTGL"

email = "admin@zestl.com"
pwd = PP.pwd
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
body = {}
body['CheckoutID'] = 956
body['OrgZviceID'] = 3000161710
method = "POST"
url = "https://twig.me/v9/payment/success"
jasub = CM.hit_url_method(body, headers1, method, url)
print jasub