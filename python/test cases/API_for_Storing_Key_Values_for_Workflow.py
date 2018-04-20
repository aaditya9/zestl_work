
import logon as LL
import common as CM

SERVER = "http://twig-me.com/" #Production
version = "v11/"
BASE_URL = SERVER + version

# zviceID = "WHGJ7HTVTDFH3"
zviceID = "83H6LVUBRXWZ5"
email = "admin@zestl.com"
pwd = "TwigMeNow"




headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
body = {}
method = "POST"
url = BASE_URL + "workflow/WHGJ7HTVTDFH3/Status Form F5/value/13"
# jasub = CM.hit_url_method(body, headers1, method, url)
# print jasub


# body = {}
# url = BASE_URL + "workflow/WHGJ7HTVTDFH3/Status Form F5"
# method = "GET"
# jasub = CM.hit_url_method(body, headers1, method, url)
# print jasub