import json
from datetime import datetime
import  time
import os
import re
import glob
from hl7apy.parser import parse_message
import add_user_aditya as UD
import login1 as LL


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



   # filepath = "/home/adi/Downloads/TwigMeScripts-master/hlt7-json/output/userinfo.csv"
    filepath=LL.adt_opt

 #   p_si = d['pid']['set_id_pid']['si']['si']
 #   id = d['pid']['patient_identifier_list']['id_number']['st']
  #   s_name = d['pid']['patient_name']['family_name']['surname']
  #   name = d['pid']['patient_name']['given_name']['st']
  # #  date = d['pid']['date_time_of_birth']['time']['dtm']
  #  from datetime import datetime
  #   datetime_object = datetime.strptime(date, '%Y%m%d')
  #   s = datetime_object.strftime("%Y/%m/%d")
   # sd = datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
 #   gender = d['pid']['administrative_sex']['is']['is']
 #   race=d['pid']['race']['identifier']['st']
#   address = d['pid']['patient_address']['street_address']['street_or_mailing_address']
#    designation=d['pid']['patient_address']['other_designation']['st']
#    city = d['pid']['patient_address']['city']['st']
#     state = d['pid']['patient_address']['state_or_province']['st']
#     zip = d['pid']['patient_address']['zip_or_postal_code']['st']
#    phone = d['pid']['phone_number_home']['telephone_number']['st']
#    lang = d['pid']['primary_language']['identifier']['st']
 #   m_status = d['pid']['marital_status']['identifier']['st']
  #  e_id=d['pid']['ethnic_group']['identifier']['st']
 #   e_text = d['pid']['ethnic_group']['text']['st']
#    e_name = d['pid']['ethnic_group']['name_of_coding_system']['id']

    try:
	d['pid']['set_id_pid']['si']['si']
	p_si = d['pid']['set_id_pid']['si']['si']
    except:
	p_si =''


    try:
	d['pid']['patient_identifier_list']['id_number']['st']
	id = d['pid']['patient_identifier_list']['id_number']['st']
    
    except:
	id = ''


    try:
	d['pid']['administrative_sex']['is']['is']
	gender = d['pid']['administrative_sex']['is']['is']
    except:
	gender = ''


    try:
	  d['pid']['primary_language']['identifier']['st']
	  lang = d['pid']['primary_language']['identifier']['st']
    except:
	  lang = ''


    try:
	d['pid']['marital_status']['identifier']['st']
	m_status = d['pid']['marital_status']['identifier']['st']
    except:
	m_status = ''

    try:
	  d['pid']['ethnic_group']['text']['st']
	  e_text = d['pid']['ethnic_group']['text']['st'] 
    except:
	   e_text = ''

    if d['pid']['phone_number_home'] != '':
        phone = d['pid']['phone_number_home']['telephone_number']['st']
    else:
        phone=''

    # if  d['pid'] ['patient_name'] !="":
    #     s_name = d['pid']['patient_name']['family_name']['surname']
    #     name = d['pid']['patient_name']['given_name']['st']
    # else:
    #     s_name=''
    #     name=''

    try :
        d['pid']['patient_name']['family_name']
        s_name = d['pid']['patient_name']['family_name']['surname']
    except:
        s_name=''

    try:
       d['pid']['patient_name']['given_name']
       name = d['pid']['patient_name']['given_name']['st']
    except:
        name=''

    try:
	  d['pid']['ethnic_group']['name_of_coding_system']['id']
	  e_name = d['pid']['ethnic_group']['name_of_coding_system']['id']
    except:
  	  e_name = ''

   # print('Patient address',['pid']['patient_address'])

    # if d['pid']['patient_address']['street_address']['street_or_mailing_address'] == "":
    #     address = ''
    # else:
    #     address = d['pid']['patient_address']['street_address']['street_or_mailing_address']

    try:
        d['pid']['patient_address']['street_address']
        address = d['pid']['patient_address']['street_address']['street_or_mailing_address']

        #city = d['pid']['patient_address']['city']['st']
    except:
        address=''
    # else:
    #     address = d['pid']['patient_address']['street_address']['street_or_mailing_address']



    try:
        d['pid']['patient_address']['city']
        city = d['pid']['patient_address']['city']['st']
        #city = d['pid']['patient_address']['city']['st']
    except:
         city=''


    try:
        d['pid']['patient_address']['state_or_province']
        state = d['pid']['patient_address']['state_or_province']['st']
        #city = d['pid']['patient_address']['city']['st']
    except:
        state=''



    try:
        d['pid']['patient_address']['zip_or_postal_code']
        zip = d['pid']['patient_address']['zip_or_postal_code']['st']
        # city = d['pid']['patient_address']['city']['st']
    except:
        zip = ''

    try:
        d['pid']['patient_address']['city']['st']
        centre= d['pid']['patient_address']['city']['st']
    except:
        centre=''




    #
    # if d['pid']['patient_address']['state_or_province']['st'] == "":
    #     state = " "
    # else:
    #     state = d['pid']['patient_address']['state_or_province']['st']
    #
    # if d['pid']['patient_address'] == "":
    #     zip = ''
    # else:
    #     zip = d['pid']['patient_address']['zip_or_postal_code']['st']
    #
    #

    # if 'patient_address' in d['pid']:
    #     address = d['pid']['patient_address']['street_address']['street_or_mailing_address']
    #     city = d['pid']['patient_address']['city']['st']
    #     state = d['pid']['patient_address']['state_or_province']['st']
    #     zip = d['pid']['patient_address']['zip_or_postal_code']['st']
    # else:
    #     address=''
    #     city=''
    #     state=''
    #     zip=''
    #

    if 'date_time_of_birth' in d ['pid']:
        date = d['pid']['date_time_of_birth']['time']['dtm']
        datetime_object = datetime.strptime(date, '%Y%m%d')
        s = datetime_object.strftime("%Y/%m/%d")
    else:
        date=''
        s=''

    if 'alternate_patient_id_pid' in d['pid'] :
        alt_pid = d['pid']['alternate_patient_id_pid']['id_number']['st']
    else:
         alt_pid=''

    if 'race' in d['pid']:
        race=d['pid']['race']['identifier']['st']
    else:
        race=''

    if 'identifier' in d['pid']:
        e_id = d['pid']['ethnic_group']['identifier']['st']
    else:
        e_id=""



    with open(filepath,"w") as wf:
            wf.write(p_si+","+id+","+alt_pid+","+s_name+","+name+","+s+","+gender+","+race+","+address+" "+city+" "+state+" "+zip+","+phone+","+lang+","+m_status+","+e_id+","+e_text+","+e_name+","+centre+"\n")

    print('Now called to add_user_func file')
    UD.adduser_main(filepath)

#    os.remove(filepath)

# Convert it
def main():
    #filepath = "/home/adi/Downloads/TwigMeScripts-master/hlt7-json/output/userinfo.csv"
    filepath=LL.adt_opt



    path=LL.adt_inp
    newpath=path[:-1]
    dirlist1 = os.listdir(newpath)
    print(dirlist1)

    for f in os.listdir(path):
        if re.search(r'~', f):
            os.remove(os.path.join(path, f))

    dirlist = os.listdir(newpath)
    print(dirlist)

    for i in dirlist:
        if re.search(r'~',i):
            dirlist.remove(i)

    print(dirlist)

    for i in dirlist:
        file=path+i
        print(file)
        with open(file,"r")as rf:

            s = rf.read()                   # read files
            d = hl7_str_to_dict(s)

            #outputfiles="/home/adi/Downloads/TwigMeScripts-master/hlt7-json/output/"   # generate opfiles on this path
            outputfiles=LL.adt_outfiles
            finalepath=outputfiles+i
            with open(finalepath,"w") as wf:
                json.dump(d,wf, indent=2)

            writecsv(d)
        #    os.remove(file)
        #    os.remove(finalepath)

#    UD.adduser_main(filepath)
    for i in dirlist:
        file = path + i
       # os.remove(file)

    outputfiles = LL.adt_outfiles

    for i in dirlist:
        finalepath = outputfiles + i
      #  os.remove(finalepath)

   # os.remove(filepath)


if __name__=='__main__':
    main()

