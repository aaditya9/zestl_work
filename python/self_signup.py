
import logon as LL
import common as CM

SERVER = "http://35.154.64.11/"  # test
# SERVER = "https://twig.me/" #Production
version = "v7/"
BASE_URL = SERVER + version


# zviceID = "2PNNBUMU6KFFM"    ####  Business ID
zviceID = "63YXHNUGXDX5T"   ####  Test

email = "admin@zestl.com"
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

body = {}
body['IsSelfUserSignupAllowed'] = True
body['SelfUserSignupMaxAllowed'] = 4
body['SelfUserSignupModeration'] = True
method = "POST"
url = "http://35.154.64.11/v7/modify/config/63YXHNUGXDX5T/selfsignup"

jasub = CM.hit_url_method(body, headers1, method, url)
print jasub
