import json

fname = "C:/Users/Minal Thorat/MINAL OFFICE DATA/try.txt"

with open(fname) as json_data:
    d = json.load(json_data)
    print d['desc']