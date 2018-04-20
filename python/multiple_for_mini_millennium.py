import password as PP
import csv
import logon as LL

import mini_parser as MP

if __name__ == "__main__":
    BASE_URL = "https://www.twig.me/v13/"
    email = 'admin@zestl.com'
    pwd = PP.pwd
    # BASE_URL = "http://52.52.18.8/v8/"  #### stagging
    # email = 'sid@zestl.com'
    # pwd = 'Zestl123'

    ZbotID = "3TMECHKDYA7CH"
    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
    keyWords = ['operator','mail noti', 'admin', 'view', 'comm pref mail', 'comm pref sms', 'title', 'description', 'check mail', 'check notification', 'zvice', 'hier', 'auto notification', 'card', 'profile image', 'allowed', 'formcsv', 'user group', 'new', 'hide', 'grid']

    # infile = "outputs/gall_per__multiple_for_SUJOY.csv"
    # infile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"
    infile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
    use_ext_zvice = True
    extZvice = ""

    # loopfile = "/home/ec2-user/scripts/TwigMeScripts/python/inputs/Jr Kg 1.csv"
    # loopfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/Tracking_card_with_BusIds.csv"
    loopfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"
    # loopfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/user_to_group_MIT.csv"
    hasHeader = "Y"


    with open(loopfile, 'r') as f:
        data = csv.reader(f, delimiter=',')
        if hasHeader == "Y":
            row1 = data.next()
        for row in data:
            extZvice = row[0]
            with open(infile, 'w') as wf:

                wf.write("text(card)\n")
                wf.write("(new)\n")
                wf.write(row[2] + "(Title)\n")
                wf.write("(Zvice)\n")
                wf.write(row[1] + "(hier)\n")
                # wf.write("3 (grid)\n")

                # wf.write("form(card)\n")
                # wf.write("(new)\n")
                # wf.write(row[3] + "(Title)\n")
                # wf.write("(Zvice)\n")
                # wf.write(row[1] + "(hier)\n")
                # wf.write("Form_HW_MYP.csv(formcsv)\n")


                # wf.write("link(card)\n")
                # wf.write("(new)\n")
                # wf.write(row[4] + "(user group)\n")
                # wf.write("(Zvice)\n")
                # wf.write(row[1] + "(hier)\n")
                # wf.write("3 (grid)\n")


                # wf.write(row[3] + "(view)\n")
                # wf.write(row[4] + "(view)\n")
                # wf.write(row[5] + "(view)\n")
                # wf.write(row[6] + "(view)\n")
                # wf.write(row[7] + "(view)\n")
                # wf.write(row[8] + "(view)\n")
                # wf.write(row[9] + "(view)\n")
                # # wf.write(row[10] + "(view)\n")
                # wf.write(row[3] + "(comm pref mail)\n")
                # wf.write(row[4] + "(comm pref mail)\n")
                # wf.write(row[5] + "(comm pref mail)\n")
                # wf.write(row[6] + "(comm pref mail)\n")
                # wf.write(row[7] + "(comm pref mail)\n")
                # wf.write(row[8] + "(comm pref mail)\n")
                # wf.write(row[9] + "(comm pref mail)\n")
                # # wf.write(row[10] + "(comm pref mail)\n")
                # wf.write(row[10] + "(operator)\n")



                # wf.write(row[10] + "(comm pref mail)\n")
                # wf.write(row[7] + "(allowed)\n")
                # wf.write(row[10] + "(Admin)\n")


                # wf.write(row[7] + "(view)\n")
                # wf.write(row[8] + "(view)\n")
                # wf.write(row[9] + "(view)\n")
                # wf.write(row[10] + "(view)\n")
                # wf.write(row[11] + "(view)\n")
                # wf.write(row[12] + "(view)\n")
                # wf.write(row[13] + "(view)\n")
                # wf.write(row[14] + "(view)\n")
                # wf.write(row[15] + "(view)\n")
                # wf.write(row[16] + "(view)\n")
                #
                # wf.write(row[3] + "(comm pref mail)\n")
                # wf.write(row[4] + "(comm pref mail)\n")
                # wf.write(row[5] + "(comm pref mail)\n")
                # wf.write(row[6] + "(comm pref mail)\n")
                # wf.write(row[7] + "(comm pref mail)\n")
                # wf.write(row[8] + "(comm pref mail)\n")
                # wf.write(row[9] + "(comm pref mail)\n")
                # wf.write(row[10] + "(comm pref mail)\n")
                # wf.write(row[11] + "(comm pref mail)\n")
                # wf.write(row[12] + "(comm pref mail)\n")
                # wf.write(row[13] + "(comm pref mail)\n")
                # wf.write(row[14] + "(comm pref mail)\n")
                # wf.write(row[15] + "(comm pref mail)\n")
                # wf.write(row[16] + "(comm pref mail)\n")




                # wf.write(row[10] + "(Admin)\n")
                # wf.write(row[11] + "(Admin)\n")
                # wf.write(row[12] + "(Admin)\n")

                # wf.write("(hide)\n")

                # wf.write("All Org Users(view)\n")
                # wf.write("Principal(view)\n")
                # wf.write("HOS - Middle School(view)\n")
                # wf.write("DP - Co-Ordinator(view)\n")
                # wf.write("IGCSE Co-Ordinator(view)\n")

                # wf.write(row[3] + "(view)\n")
                # wf.write(row[4] + "(view)\n")
                # wf.write(row[5] + "(view)\n")
                # wf.write(row[6] + "(view)\n")
                # wf.write(row[7] + "(view)\n")





                # wf.write("Transport Bus Admin" + "(view)\n")



                # wf.write("App Admins(view)\n")
                # wf.write("HOS - Middle School(view)\n")
                # wf.write("MYP Co-Ordinator(view)\n")
                # wf.write("App Admins(allowed)\n")


                # wf.write("MYP Co-Ordinator(comm pref mail)\n")
                # wf.write("HOS - Middle School(comm pref mail)\n")
                # wf.write("Head of Boarding(comm pref mail)\n")
                # wf.write("House Parents(comm pref mail)\n")



                # wf.write("Form_HW_MYP.csv(formcsv)\n")

                # wf.write("All Org Users(View)\n")


                # wf.write("Linked Users" + "(admin)\n")
                # wf.write(row[2] + "(description)\n")
                #

                # wf.write("BR " + row[3] + " Students" + "(view)\n")
                # wf.write("BR " + row[4] + " Students" + "(view)\n")
                # wf.write("BR " + row[5] + " Students" + "(view)\n")
                # wf.write("BR " + row[6] + " Students" + "(view)\n")

                # wf.write("Transport Bus Admin" + "(operator)\n")

            print "creating for zviceID " + extZvice
            MP.createStructure(keyWords, infile, ZbotID, headers1, BASE_URL, use_ext_zvice, extZvice)