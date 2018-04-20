import logon as LL
import common as CM
import csv
import password as PP
SERVER = "https://twig.me/"
version = "v13/"
BASE_URL = SERVER + version
hasHeader = "Y"
# Bussiness_ID = "X9FYBNR8PUL9A"   # army public school
# Bussiness_ID = "D3PYYBWVZZBJX"  # Indus banglore new business
Bussiness_ID = "B969YSR37AT7G"  # pune indus
# Bussiness_ID = "FYRKVLCSCRF8F"  #Koregaon park indus
# Bussiness_ID = "W8W2BCY3CYMAU"  #Bhosale Nagar indus
# Bussiness_ID = "3TMECHKDYA7CH"  # hydrabad indus

email = "admin@zestl.com"
pwd = PP.pwd
errorFile = "MUL_LINKING.txt"
notename = [None] * 20
noteCol = [None] * 20
noOfNotes = 2

notename[0] = "parent"
noteCol[0] = 1
notename[1] = "papa"
noteCol[1] = 2
# notename[2] = "papa1"
# noteCol[2] = 3
csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/19_feb_parent_linking_data.csv"
# csvfile = "/home/ec2-user/scripts/TwigMeScripts/python/inputs/one.csv"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(Bussiness_ID, headers1, BASE_URL)
with open (csvfile, 'r') as infile:
    with open(errorFile, "a") as ef:
        data = csv.reader(infile, delimiter=',')
        if hasHeader == "Y":
            row1 = data.next()
        counter = 0
        for row in data:
            counter += 1
            print counter
            zviceID = CM.force_decode(row[0].strip())
            print "Working for this Zvice ID :- " + zviceID
            a = []
            for i in range(0, noOfNotes):
                if noteCol[i] ==-1:
                    note = ""
                else:
                    note = row[noteCol[i]].strip()
                    a.append(note)
            # a.remove('')
            # print a
            body = {}
            body['RelatedUsers'] = a
            method = "POST"
            # url = "https://twig.me/v8/XBEER2UPJ4KN2/users/" + zviceID + "/relationships"
            url = BASE_URL + Bussiness_ID + "/users/" + zviceID + "/relationships"
            print url
            jasub = CM.hit_url_method(body, headers1, method, url)
            print jasub
            ef.write(zviceID + "  ::  " + jasub + "\n")