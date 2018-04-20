import logon as LL
import common as CM

SERVER = "https://twig.me/"
version = "v8/"
BASE_URL = SERVER + version

zviceID = "8SFKZCV5PFAXV"
email = "admin@zestl.com"
pwd = ""
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

body = {}
method = "POST"
# url = "https://twig.me/v8/org/8SFKZCV5PFAXV/move/card/111/to/tag/8SFKZCV5PFAXV/card/102"  ## Gallery to text
# url = "https://twig.me/v8/org/8SFKZCV5PFAXV/move/card/102/to/tag/4R9NAJP6NKWAR" #text to dept
# url = "https://twig.me/v8/org/8SFKZCV5PFAXV/move/card/103/to/tag/8SFKZCV5PFAXV/card/204"    #Location to forum
# url = "https://twig.me/v8/org/8SFKZCV5PFAXV/move/card/103/to/tag/3CBLVH5NBFGF5" # location to Library
# url = "https://twig.me/v8/org/8SFKZCV5PFAXV/move/card/103/to/tag/AET2H7NELGDHZ" # business to business
url = "https://twig.me/v8/org/8SFKZCV5PFAXV/move/card/102/to/tag/8SFKZCV5PFAXV/card/205"  ## parent text inside child text
jasub = CM.hit_url_method(body, headers1, method, url)
print jasub


