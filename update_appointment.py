import json
from datetime import datetime
import  time
import os
import re
import glob
import pytz

from hl7apy.parser import parse_message

import create_events_aditya as AE

def hl7_message_to_dict(m, use_long_name=True):
    """Convert an HL7 message to a dictionary
    :param m: The HL7 message as returned by :func:`hl7apy.parser.parse_message`
    :param use_long_name: Whether or not to user the long names
                          (e.g. "patient_name" instead of "pid_5")
    :returns: A dictionary representation of the HL7 message
    """
    if m.children:
        d = {}
        for c in m.children:
            name = str(c.name).lower()
            if use_long_name:
                name = str(c.long_name).lower() if c.long_name else name
            dictified = hl7_message_to_dict(c, use_long_name=use_long_name)
            if name in d:
                if not isinstance(d[name], list):
                    d[name] = [d[name]]
                d[name].append(dictified)
            else:
                d[name] = dictified
        return d
    else:
        return m.to_er7()

def hl7_str_to_dict(s, use_long_name=True):
    s = s.replace("\n", "\r")
    m = parse_message(s)
    #print(m)
    return hl7_message_to_dict(m, use_long_name=use_long_name)

def writecsv(d):

    filepath = "/home/adi/Downloads/TwigMeScripts-master/hlt7-json/siu/output/userinfo1.csv"
   # p_id=d['pid']['patient_identifier_list']['id_number']['st']
    app_type = d['sch']['appointment_type']['text']['st']
    app_reason=d['sch']['appointment_reason']['identifier']['st']
    start_date = d['sch']['appointment_timing_quantity']['start_date_time']['time']
#    datetime_object = datetime.strptime(start_date, '%Y%m%d%H%M%S')
    #s1 = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
    rr=time.strftime("%Y-%m-%d %H:%M:%S",
                  time.gmtime(time.mktime(time.strptime(start_date,
                                                        "%Y%m%d%H%M%S"))))
    print(rr)
    result=rr.split(" ")
    s_date=result[0]
    s_time=result[1]
    print(s_date)
    print (s_time)
    #
    end_date=d['sch']['appointment_timing_quantity']['end_date_time']['time']

    rr1=time.strftime("%Y-%m-%d %H:%M:%S",
                  time.gmtime(time.mktime(time.strptime(end_date,
                                                        "%Y%m%d%H%M%S"))))
    result1 = rr1.split(" ")
   # print(result)
    e_date = result1[0]
    e_time = result1[1]
    print(e_date)
    print (e_time)
    #
    LID=d['ail']['location_resource_id']['point_of_care']['is']
    Location=d['ail']['location_resource_id']['room']['is']
    PID=d['aip']['personnel_resource_id']['id_number']['st']
    D_firstname=d['aip']['personnel_resource_id']['family_name']['surname']
    D_lastname=d['aip']['personnel_resource_id']['given_name']['st']
    s_name = d['pid']['patient_name']['family_name']['surname']
    name = d['pid']['patient_name']['given_name']['st']
    date = d['pid']['date_time_of_birth']['time']['dtm']
    #  from datetime import datetime
    datetime_object = datetime.strptime(date, '%Y%m%d')
    s = datetime_object.strftime("%Y/%m/%d")
    print(s)

    p_id=d['pid']['patient_identifier_list']['id_number']['st']
    address = d['pid']['patient_address']['street_address']['street_or_mailing_address']
    #    designation=d['pid']['patient_address']['other_designation']['st']
    phone = d['pid']['phone_number_home']['telephone_number']['st']

    if 'alternate_patient_id_pid' in d['pid']:
        alt_pid = d['pid']['alternate_patient_id_pid']['id_number']['st']
    else:
        alt_pid = ''

    print('One file converted and data upload to userinfo1.csv')

    with open(filepath,"a") as wf:
            wf.write(p_id+","+app_type+","+app_reason+","+s_date+","+s_time+","+e_date+","+e_time+","+LID+","+Location+","+PID+","+D_firstname+","+D_lastname+","+alt_pid+","+s_name+","+name+","+phone+","+address+","+s+"\n")

 #   AE.generate_events(filepath)
    #os.remove(filepath)

# Convert it
def main():
    filepath = "/home/adi/Downloads/TwigMeScripts-master/hlt7-json/siu/output/userinfo1.csv"
    columnTitleRow = "PID,Appointment Type,Appointment Reason,StartDate,Appointment Timing start,End Date,Appointment Timing end,Location Resource ID,Location,Personnel Resource ID," \
                     "Doc F_N,Doc L_N,Alternate ID,Surname,Name,Phone,Address,Date\n"
    with open(filepath, "w")as wf:
        wf.write(columnTitleRow)

    path="/home/adi/Downloads/TwigMeScripts-master/hlt7-json/siu/inputs/"

    dirlist1 = os.listdir("/home/adi/Downloads/TwigMeScripts-master/hlt7-json/siu/inputs")
    print'Before del ~ files',dirlist1

    for  f in os.listdir(path):
            if re.search(r'~',f):
                    os.remove(os.path.join(path,f))

    dirlist = os.listdir("/home/adi/Downloads/TwigMeScripts-master/hlt7-json/siu/inputs")
    print(dirlist)

    print('Start converting hl7 to json and generate userinfo1.csv \n')
    for i in dirlist:
        file=path+i
        print(file)
        with open(file,"r")as rf:

            s = rf.read()                   # read files
            d = hl7_str_to_dict(s)

            outputfiles="/home/adi/Downloads/TwigMeScripts-master/hlt7-json/siu/output/"   # generate opfiles on this path

            finalepath=outputfiles+i
            with open(finalepath,"w") as wf:
                json.dump(d,wf, indent=2)

            writecsv(d)
            # os.remove(file)
            # os.remove(finalepath)

    print 'Now Event will Generate\n'
    AE.generate_events(filepath)
#    os.remove(filepath)


if __name__=='__main__':
    main()
