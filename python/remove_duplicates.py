
import re
import csv

csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/FiberFitness_Members_data.csv"
outfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/FiberFitness_Members_data_clean.csv"
hasHeaders = True
with open(outfile, 'w') as wf:
    with open (csvfile, 'r') as infile:
        data = csv.reader(infile, delimiter=',')
        users = [""]
        # if hasHeaders:
        #
        #     row1 = data.next()
        for row in data:
            setflag = False
            for user in users:
                if row[1] == user:
                    print "Duplicate entry"
                    setflag = True
            if setflag == False:
                users.append(row[1])
                for el in row:
                    wf.write(el)
                    wf.write(",")
                wf.write("\n")