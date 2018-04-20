import logon as LL
import common as CM
import auth as AA

SERVER = "https://twig.me/" #Production
version = "v9/"
BASE_URL = SERVER + version
# zviceID = "8SFKZCV5PFAXV"
zviceID = "BBH2SQEKPUGLW"   #millennium dev department

email = "admin@zestl.com"
pwd = AA.pwd
errorFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/stagging_bus_OUT.csv"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

with open(errorFile, "w") as ef:
    for a in jsondata['data']['elements']:
        if "OUT" in a['title']:
            print a['title']
            print a['cardID']
            ef.write(a['title'])
            ef.write(",")
            ef.write(str(a['cardID']) + "\n")