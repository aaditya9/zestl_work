import csv

infile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/Indus_tags.csv"
outfile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/resign_indus.csv"
oldfile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/Resignations.csv"

inbuf = []
itemfound = False
everyone = {}

with open(outfile, 'w') as wf:
    with open(infile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            for row in data:
                everyone[row[5]] = row[2]
    print everyone
    with open(oldfile, 'r') as rf:
            data = csv.reader(rf, delimiter=',')
            for row in data:
                writestring = ""
                for i in range(0, len(row)):
                    writestring = writestring + "\"" + row[i] + "\""  + ","
                try:
                    wf.write(everyone[row[1]])
                    wf.write(",")
                    wf.write(writestring)
                    wf.write("\n")
                except:
                    try:
                        see = "Mr. " + row[1]
                        wf.write(everyone[see])
                        wf.write(",")
                        wf.write(writestring)
                        wf.write("\n")
                    except:
                        try:
                            see = "Ms. " + row[1]
                            wf.write(everyone[see])
                            wf.write(",")
                            wf.write(writestring)
                            wf.write("\n")
                        except:
                            try:
                                see = "Deactivated Ms. " + row[1]
                                wf.write(everyone[see])
                                wf.write(",")
                                wf.write(writestring)
                                wf.write("\n")
                            except:
                                try:
                                    see = "Deactivated Mr. " + row[1]
                                    wf.write(everyone[see])
                                    wf.write(",")
                                    wf.write(writestring)
                                    wf.write("\n")
                                except:
                                    try:
                                        see = "Capt. " + row[1]
                                        wf.write(everyone[see])
                                        wf.write(",")
                                        wf.write(writestring)
                                        wf.write("\n")
                                    except:
                                        try:
                                            see = "Deactivated Capt. " + row[1]
                                            wf.write(everyone[see])
                                            wf.write(",")
                                            wf.write(writestring)
                                            wf.write("\n")
                                        except:
                                            print "not found"
                                            wf.write(",")
                                            wf.write(writestring)
                                            wf.write("\n")

                #
                #
                # for item in inbuf:
                #     if row[3] == item:
                #         itemfound = True
                # if itemfound:
                #     print "doing nothing"
                #     itemfound = False
                # else:
                #     wf.write("Text(Card)\n")
                #     wf.write("\"" + row[3] + "(Title)\"\n")
                #     wf.write("(New)\n")
                #     wf.write("\"" + row[4] + "(Description)\"\n")
                #     wf.write("ELMCFNGLEVXYP(Zvice)\n")
                #     wf.write(row[0] + ";" + row[1] + ";" + row[2] + "(Hier)\n")
                #     # wf.write(row[0] + "(Hier)\n")
                #     # inbuf.append(row[1])
                #
                #
                #
                #
