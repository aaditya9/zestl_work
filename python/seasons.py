import csv

infile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/FAQGST.csv"
outfile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/answers.csv"

inbuf = []
itemfound = False

with open(outfile, 'w') as wf:
    with open(infile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            for row in data:
                for item in inbuf:
                    if row[3] == item:
                        itemfound = True
                if itemfound:
                    print "doing nothing"
                    itemfound = False
                else:
                    wf.write("Text(Card)\n")
                    wf.write("\"" + row[3] + "(Title)\"\n")
                    wf.write("(New)\n")
                    wf.write("\"" + row[4] + "(Description)\"\n")
                    wf.write("ELMCFNGLEVXYP(Zvice)\n")
                    wf.write(row[0] + ";" + row[1] + ";" + row[2] + "(Hier)\n")
                    # wf.write(row[0] + "(Hier)\n")
                    # inbuf.append(row[1])




