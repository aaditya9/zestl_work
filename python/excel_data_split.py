import csv
import re

def readStructure(fname):
    baseset = 0
    cardType = {}
    numcards = 0
    cardfound = 0
    cardDetails = {}
    cardstarted = 0
    endCard = 0
    rownum = 0
    # cardType1 = {}
    # cardDetails1 = {}

    with open(fname, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        column = {}
        # for j in range (5):
        #     column[j] = []
        nullElement = ""

        for row in data:
            # lengthrow = len(row)
            # print lengthrow
            for j in range(len(row)):
                try:
                    column[j].append(row[j])
                except:
                    column[j] = []
                    column[j].append(row[j])
                    # column[j+1] = ""
            j = len(row)
            try:
                column[j].append(nullElement)
            except:
                column[j] = []
                column[j].append(nullElement)
    return column


infile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\etrial_jan.csv"

columns = readStructure(infile)

print columns
events = {}
dateFormatter = "2017-01-"

for index in columns:
    print columns[index]
    column = columns[index]
    dayStart = 0
    eventName = ""
    k = 0

    for j in column:
        if re.match(r'\d+', j):
            if dayStart == 1:
                dayStart = 0
                print key1
                print eventName
                events[key1] = eventName
                eventName = ""
                k += 1
            dayStart = 1
            key1 = dateFormatter + j

        elif dayStart == 1:
            # if re.match("", j):
            #     k += 1
            #     print key1
            #     print eventName
            #     events[key1] = eventName

            if re.search(r'\w+', j):
                eventName += j + " "

        print eventName
    print key1
    events[key1] = eventName
    key1 = "hack1"

    print "################################"

print columns
print events
stringPrint = ""
for k, v in events.items():
    if v == "":
        print "blank"
    else:
        stringPrint +=  k + "," + v + "\n"
inputFile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\copy10.csv"
with open(inputFile, 'w') as datalist:
    datalist.write(stringPrint)
print stringPrint
#
# print " *********************************** "
# for k, v in events.items():
#     print v
