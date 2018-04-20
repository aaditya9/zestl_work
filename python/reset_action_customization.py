
import logon as LL
import common as CM

SERVER = "https://twig.me/" #Production
version = "v7/"
BASE_URL = SERVER + version

zviceID = "8SFKZCV5PFAXV"
email = "admin@zestl.com"
pwd = "Zspladmin99"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

body = {}
body['CardType'] = "ORG_BASE_CARD"
body['SetCardType'] = None
body['CardID'] = None
method = "POST"
url = "https://twig.me/v8/resetcustomization/actions/8SFKZCV5PFAXV"
jasub = CM.hit_url_method(body, headers1, method, url)
print jasub