import csv
import re
#with open(inputFile, 'r') as ulist:

inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/try1.csv"
outFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/try_out_1.csv"
with open(outFile, "w") as ofile:
    with open(inputFile, "r") as vlist:
        data = csv.reader(vlist, delimiter=',')
        for row in data:
            row[0] = row[0].strip()
            row[0] = re.sub(r'^91(.*)', r'\1', row[0])
            for no in row:
                if re.search(',', no):
                    no = "\"" + no + "\""
                ofile.write(no + ",")
            ofile.write("\n")

