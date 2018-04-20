import csv

csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/prod_recent_activity_all.csv"
outfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/sujoy.csv"
hasHeaders = True
with open(outfile, 'w') as wf:
    with open (csvfile, 'r') as infile:
        data = csv.reader(infile, delimiter=',')
        for row in data:
            # print row[0]
            if row[0] == "3211":
                print "found"

            else:
                for el in row:
                    wf.write(el)
                    wf.write(",")
                wf.write("\n")