import csv

inputFile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\New_list_vrushali.csv" #####

destFile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\write_vrushali.csv"


removeTags = [None] * 500
removeTagskv = {}
stringPrint = ""
stringInclude = ""
with open(inputFile, 'r') as vlist:
    data1 = csv.reader(vlist, delimiter=',')
    i = 0
    # for row in data:
    #     print row
    # print "$%%%%%%%%%%%%%%%%%%%%%%%%%%$%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    for row in data1:
        print row
        removeTags[i] = row[0]
        # removeTagskv[row[0]] = row[1]
        i += 1

for item in removeTags:
    if item != None:
        if removeTags.count(item) > 1:
            print item + " : " + str(removeTags.count(item))
print removeTags

with open(destFile, 'r') as userlist:
    data = csv.reader(userlist, delimiter=',')
    for row in data:
        flag = 0
        for element, value in removeTagskv.items():
            if element != None:
                if element in row[0]:
                    # print row[0]
                    flag = 1
                    stringPrint += element + "," + removeTagskv[element] + "\n"

                    print "found element " + element + " : " + row[0]

                # else:
                #     print row
        if flag == 0:
            # print row
            for val in row:
                stringPrint += val
                stringPrint += ','
            stringPrint += "\n"
        elif flag == 1:
            for val in row:
                stringInclude += val
                stringInclude += ','
            stringInclude += "\n"
print stringInclude
print "^^^^^^^^^^^^^^^^^"
print stringPrint
newFile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\g_vrushali1.csv"
with open(newFile, 'w') as a:
    a.write(stringPrint)

includeFile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\g_vrushali11_include.csv"
with open(includeFile, 'w') as a:
    a.write(stringInclude)

