import logon as LL
import common as CM
import password as PP
# SERVER = "http://35.154.64.11/"  # test
SERVER = "https://twig.me/" #Production
# SERVER = "http://52.52.18.8/" # Staging Server
version = "v8/"
BASE_URL = SERVER + version

zviceID = "44JY2L9DJFZMH"

email = "admin@zestl.com"
# pwd = "TwigMeNow"
pwd = PP.pwd

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
# shopname = ["Cafe Coffee Day","Forever Sports","High Octane","Just Watches","Kodak Photoexpress","Lee Jeans","Metro Shoes","T-Base","Tiny Buttons","Wrangler","Bata","Bombay Dyeing","Cotton Galaxy",
#             "Credo Nax","Lenskart","Optique","Red Ginger / Indian Tadka","Skinn","Samsung Cafe","Altitude","Barista"]
shopname = ["Yoga Session", "Good Initiatives"]
body = {}
body['ShopNames'] = shopname
method = "POST"
# url = "http://35.154.64.11/v6/products/876MD568TAUH2/maxproducts/15"
url = "https://twig.me/v8/44JY2L9DJFZMH/add/shops/loyalty"
jasub = CM.hit_url_method(body, headers1, method, url)
print jasub