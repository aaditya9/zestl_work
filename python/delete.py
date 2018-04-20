import csv
#with open(inputFile, 'r') as ulist:

inputFile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\VSC_Customers Data _Fresh.csv"
destFile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\userlist_mill.csv"
removeTags = [None] * 50
stringPrint = ""
with open(inputFile, 'r') as vlist:
    data = csv.reader(vlist, delimiter=',')
    i = 0
    for row in data:
        removeTags[i] = row[0]
        i += 1

print removeTags

with open(destFile, 'r') as userlist:
    data = csv.reader(userlist, delimiter=',')
    for row in data:
        flag = 0
        for element in removeTags:
            if element != None:
                if element in row[0]:
                    # print row[0]
                    flag = 1
                    print "found element " + row[0]
                # else:
                #     print row
        if flag == 0:
            # print row
            for element in row:
                stringPrint += element
                stringPrint += ','
            stringPrint += "\n"


print stringPrint
newFile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\userlist2_mill.csv"
with open(newFile, 'w') as a:
    a.write(stringPrint)

