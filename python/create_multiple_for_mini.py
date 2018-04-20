import password as PP
import csv
import logon as LL

import mini_parser as MP

if __name__ == "__main__":
    BASE_URL = "https://www.twig.me/v8/"
    email = 'admin@zestl.com'
    pwd = PP.pwd
    # email = "manasi@zestl.com"
    # pwd = "zestl123"
    # ZbotID = "B969YSR37AT7G" ## indus
    # ZbotID = "8SFBUKFZCALEE" ##gold's
    # BASE_URL = "http://35.154.64.11/v5/"  ### testtttttttttttt
    # pwd = "TwigMeNow"
    # ZbotID = "876MD568TAUH2" ## minal test
    # ZbotID = "AYX6T62MU62D4"  ## lavasa citizens
    # ZbotID = "82YXAC9BJX686" ## Biggest loosers
    # ZbotID = "XVL5PPENFYRN2" ### Fiber Fitness
    # ZbotID = "8SFKZCV5PFAXV"  ### minal prod
    # ZbotID = "AKSZFSQR8BUPX"    ### Slimwell Fitness studio
    # ZbotID = "EYBC2NFB8BJ4C"    ### Vrushali
    # ZbotID = "8SFBUKFZCALEE"    #Golds
    # ZbotID = "X96LUCRACVS25"    #Sanctum Design
    # ZbotID = "6KX4PVHCYAAJ8" # satara_gold
    ZbotID = "9J5EDAR3Y2PZA"    # Millennium

    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
    keyWords = ['mail noti', 'admin', 'view', 'comm pref mail', 'comm pref sms', 'title', 'description', 'check mail', 'check notification', 'zvice', 'hier', 'auto notification', 'card', 'profile image', 'allowed', 'formcsv', 'user group', 'new', 'hide', 'grid']


    # keyWords = ['admin', 'view', 'comm pref mail', 'comm pref sms', 'title', 'description', 'check mail',
    #             'check notification', 'zvice', 'hier', 'auto notification', 'card', 'profile image', 'allowed',
    #             'formcsv', 'user group', 'new', ]

    # infile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/sac_struct.csv"
    infile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/gall_per_millennium.csv"
    use_ext_zvice = True
    extZvice = ""

    # loopfile =  "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/28DEC_all_Trainers_user_tag.csv"
    loopfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/Jr Kg 1.csv"
    hasHeader = "Y"

    with open(loopfile, 'r') as f:
        data = csv.reader(f, delimiter=',')
        if hasHeader == "Y":
            row1 = data.next()
        for row in data:
            extZvice = row[0]
            print "creating for zviceID " + extZvice
            MP.createStructure(keyWords, infile, ZbotID, headers1, BASE_URL, use_ext_zvice, extZvice)