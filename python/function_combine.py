# import csv

from datetime import datetime
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def section(day):
    if day <=35:
        member_type = "Monthly"
        print type
        # return member_type

    elif day <= 130:
        member_type = "Quarterly"
        # print "Quaterly"

    elif day <= 220:
        member_type = "Half Yearly"
        # print "Half Yearly"

    elif day <=750:
        member_type = "Yearly"
        # print "yearly"
    else:
        print "error"

    return member_type
