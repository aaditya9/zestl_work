import logon as LL
import common as CM

SERVER = "http://twig-me.com/" #Production
version = "v11/"
BASE_URL = SERVER + version
email = "admin@zestl.com"
pwd = "TwigMeNow"
zviceID="WHGJ7HTVTDFH3"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
body = {}
url = BASE_URL + "timezones"
method = "GET"
jasub = CM.hit_url_method(body, headers1, method, url)
print jasub