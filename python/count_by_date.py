import csv

csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/prod_recent_activity_all.csv"
outfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/sort_by_date_8feb.csv"
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
                access[row[2]].append(row[1])
                # access[row[0]].append(line)
            except:
                temparr = []
                temparr.append(row[1])
                access[row[2]] = temparr
                print "failure"
                # var = 1
                # access[row[0]] = var
                # access[row[0]].append(1)
        # for (k,v) in access.items():
        #     wf.write(k + "," + str(v) + "\n")
    for k,v in access.items():
        print k
        print len(v)
        # print v
        arr1 = v
        v = list(set(arr1))
        csvfile1 = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_per_1.csv"
        with open(csvfile1, 'r') as infile:
            data = csv.reader(infile, delimiter=',')
            v = []
            for row in data:
                v.append(row[0])
        # v = ["1000040999","3000004597","3000022853"]
        wf.write(str(k) + ",")

        for val in v:
        #
            wf.write(str(arr1.count(val)) + ",")
        wf.write("\n")

    #     wf.write(k + "," + str(len(v)) + "\n")
    # print "nothing"