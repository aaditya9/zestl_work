import logon as LL
import common as CM
# import password as PP

SERVER = "http://35.154.64.119/"  # test
# SERVER = "https://twig.me/" #Production
# SERVER = "http://www.twig-me.com/"  # DEV
version = "v9/"
BASE_URL = SERVER + version

zviceID = "57YPSTWDH79WE"

email = "admin@zestl.com"
# pwd = PP.pwd
pwd = "TwigMeNow"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
# //app->post(/geofence/enable/:ZviceID)
body = {}
method = "POST"
url = BASE_URL + "geofence/enable/" + zviceID       #Enable URL

# url = BASE_URL + "geofence/disable/" + zviceID       #Disable URL

jasub = CM.hit_url_method(body, headers1, method, url)
print jasub