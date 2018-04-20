import csv
import re

infile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/RetailersData2017.csv"
outfile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/RetailersOut2017.csv"

with open(outfile, 'w') as wf:
    with open(infile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            for row in data:
                wf.write("Text(Card)\n")
                wf.write(row[0] + "(Title)\n"
                wf.write("New\n")
                wf.write("Floor : " + row[2] " ; Contact : " + row[3] + "(Description)\n")
                wf.write("(Zvice)\n")
                wf.write("Deals; " + row[1] + "(Hier)\n")




