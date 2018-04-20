import csv

csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/prod_recent_activity_all.csv"
outfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/sort_by_date.csv"
hasHeaders = True
with open(outfile, 'w') as wf:
    with open (csvfile, 'r') as infile:
        data = csv.reader(infile, delimiter=',')
        access = {}
        for row in data:
            # print(row[0])
            line = ""
            for i in range(1,len(row)):
                line = line + "," + row[i]
            try:
                access[row[3]].append(row[1])
                # access[row[0]].append(line)
            except:
                temparr = []
                temparr.append(row[1])
                access[row[3]] = temparr
                print "failure"
                # var = 1
                # access[row[0]] = var
                # access[row[0]].append(1)
        # for (k,v) in access.items():
        #     wf.write(k + "," + str(v) + "\n")
    for k,v in access.items():
        print k
        print len(v)
        arr1 = set(v) ###**
        print len(list(arr1))   #### ****
        # wf.write(k + "," +str(len(list(arr1))) + "\n")
        wf.write(k + "," + str(len(v)) + "\n")
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

