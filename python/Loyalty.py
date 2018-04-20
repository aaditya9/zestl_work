import logon as LL
import common as CM

# SERVER = "http://35.154.64.11/"  # test
SERVER = "https://twig.me/" #Production
version = "v8/"
BASE_URL = SERVER + version
email = "admin@zestl.com"
pwd = "Zspladmin99"
zviceID = "FREXRS3G4FJXC"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

body = {}
body['LoyaltyPointsEnabled'] = "YES"
body['LoyaltyPointsConversionPercent'] = 1.1
method = "POST"
# url = "http://35.154.64.11/v8/F7SWPSGKW7AWG/configure/loyalty"
url = "https://twig.me/v8/F7SWPSGKW7AWG/configure/loyalty"
jasub = CM.hit_url_method(body, headers1, method, url)
print jasub