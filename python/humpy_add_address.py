import csv
import logon as LL
import common as CM
import password as PP

SERVER = "https://twig.me/" #Production
version = "v8/"
BASE_URL = SERVER + version

zviceID = "87ZWFB9AKKCK8"
email = "admin@zestl.com"
pwd = PP.pwd

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
# jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
hasHeader = "Y"
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"

with open(inputFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    counter = 0
    for row in data:
        counter += 1
        print counter
        body = {}
        body['Name'] = CM.force_decode(row[1])
        body['EmailID'] = "update@gmail.com"
        body['MobileNo'] = CM.force_decode(row[2])
        body['AddressLine1'] = CM.force_decode(row[3])
        body['AddressLine2'] = ""
        body['Landmark'] = "Please update landmark"
        body['PinCode'] = "411"
        body['State'] = "Maharashtra"
        body['City'] = "Pune"
        body['Area'] = "Please update"
        method = "POST"
        url = BASE_URL + "address/" + zviceID + "/user/" + CM.force_decode(row[0])
        # url = "https://twig.me/v8/address/8SFKZCV5PFAXV/user/DU8BFMK4WUBZF"
        jasub = CM.hit_url_method(body, headers1, method, url)
        print jasub