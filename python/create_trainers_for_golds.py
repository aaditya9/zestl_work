
import csv
import logon as LL

import mini_parser as MP

if __name__ == "__main__":
    BASE_URL = "https://www.twig.me/v5/"
    email = 'admin@zestl.com'
    pwd = 'Zspladmin99'
    # ZbotID = "B969YSR37AT7G" ## indus
    ZbotID = "8SFBUKFZCALEE" ##gold's
    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

    keyWords = ['admin', 'view', 'comm pref mail', 'comm pref sms', 'title', 'description', 'check mail',
                'check notification', 'zvice', 'hier', 'auto notification', 'card', 'profile image', 'allowed',
                'formcsv', 'user group', 'new']

    infile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/Gold_Trainers_new_struct.csv"
    use_ext_zvice = True
    extZvice = ""

    loopfile =  "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/28DEC_all_Trainers_user_tag.csv"
    hasHeader = "Y"

    with open(loopfile, 'r') as f:
        data = csv.reader(f, delimiter=',')
        if hasHeader == "Y":
            row1 = data.next()
        for row in data:
            extZvice = row[0]
            print "creating for zviceID " + extZvice
            MP.createStructure(keyWords, infile, ZbotID, headers1, BASE_URL, use_ext_zvice, extZvice)
