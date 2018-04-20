import csv

csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/prod_recent_activity_all.csv"
outfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/abc.csv"
hasHeaders = True
with open(outfile, 'w') as wf:
    with open (csvfile, 'r') as infile:
        data = csv.reader(infile, delimiter=',')
        access = {}
        for row in data:
            print(row[1])
            line = ""
            for i in range(1,len(row)):
                line = line + "," + row[i]
            try:
                access[row[1]] = access[row[1]] + 1
                # access[row[0]].append(line)
            except:
                var = 1
                access[row[1]] = var
                # access[row[0]].append(1)
        for (k,v) in access.items():
            wf.write(k + "," + str(v) + "\n")
    print "nothing"
        # tag = [""]
        # for row in data:
        #     for user in tag:
        #         if row[0] == user:
        #             print "found"
        #             for el in row:
        #                 wf.write(el)
        #                 wf.write(",")
        #             wf.write("\n")

