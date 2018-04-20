import json
import datetime
import  time
import os
from hl7apy.parser import parse_message

# Taken from http://hl7apy.org/tutorial/index.html#elements-manipulation

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
    """Convert an HL7 string to a dictionary
    :param s: The input HL7 string
    :param use_long_name: Whether or not to user the long names
                          (e.g. "patient_name" instead of "pid_5")
    :returns: A dictionary representation of the HL7 message
    """
    s = s.replace("\n", "\r")
    m = parse_message(s)
    #print(m)
    return hl7_message_to_dict(m, use_long_name=use_long_name)


def writecsv(d):

    filepath="/home/adi/Desktop/zestl/hlt7-json/output/userinfo.csv"

    columnTitleRow="P_SI,PID,Alternate PID,Surname,Name,Date,Gender,race_id,Address,City,State,Zip,Mobile,Language,Martialstatus,Ethenic id,Ethenic text,Ethenic name_of_coding\n"

    with open(filepath,"w")as wf:
        wf.write(columnTitleRow)
    p_si = d['pid']['set_id_pid']['si']['si']
    id = d['pid']['patient_identifier_list']['id_number']['st']
    s_name = d['pid']['patient_name']['family_name']['surname']
    name = d['pid']['patient_name']['given_name']['st']
    date = d['pid']['date_time_of_birth']['time']['dtm']
   # sd = datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
    gender = d['pid']['administrative_sex']['is']['is']
 #   race=d['pid']['race']['identifier']['st']
    address = d['pid']['patient_address']['street_address']['street_or_mailing_address']
#    designation=d['pid']['patient_address']['other_designation']['st']
    city = d['pid']['patient_address']['city']['st']
    state = d['pid']['patient_address']['state_or_province']['st']
    zip = d['pid']['patient_address']['zip_or_postal_code']['st']
    phone = d['pid']['phone_number_home']['telephone_number']['st']
    lang = d['pid']['primary_language']['identifier']['st']
    m_status = d['pid']['marital_status']['identifier']['st']
  #  e_id=d['pid']['ethnic_group']['identifier']['st']
    e_text = d['pid']['ethnic_group']['text']['st']
    e_name = d['pid']['ethnic_group']['name_of_coding_system']['id']

    if 'alternate_patient_id_pid' in d['pid'] :
        alt_pid = d['pid']['alternate_patient_id_pid']['id_number']['st']
    else:
         alt_pid=''
    #   data=[p_si,id,s_name,name]

    if 'race' in d['pid']:
        race=d['pid']['race']['identifier']['st']
    else:
        race=''

    if 'identifier' in d['pid']:
        e_id = d['pid']['ethnic_group']['identifier']['st']
    else:
        e_id=""

    with open(filepath,"a") as wf:
            wf.write(p_si+","+id+","+alt_pid+","+s_name+","+name+","+date+","+gender+","+race+","+address+","+city+","+state+","+zip+","+phone+","+lang+","+m_status+","+e_id+","+e_text+","+e_name+"\n")

# Convert it
def main():
    with open("inputs/adt-eg1.txt", "r") as rf:
        s = rf.read()

    d = hl7_str_to_dict(s)
    writecsv(d)

    with open("output/adt-eg1.txt","w") as wf:
        json.dump(d,wf, indent=2)

if __name__=='__main__':
    main()
