import json
import lib.login1 as LL
import common as CM
import csv

headers, headers1 = LL.req_headers()

zviceID = "WH4ULS9BHSAKZ"


def getBaseStructure(zbotID, headers1):
    url = LL.BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    response = hit_url(RequestBody, headers1, zbotID, url)
#    with open('C:/Users/Minal Thorat/Dropbox/Zestl-scripts/rundir/tmp', 'w') as f:
#        f.write(str(response))
    return json.loads(response)

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def check_appointment():
    jsondata = getBaseStructure(zviceID, headers1)
    # print jsondata
    tagids = []
    for element in jsondata['data']['elements']:
        if element['cardtype'] == "basecard" and element['tagId'] != zviceID:
            tagids.append(element['tagId'])
        # print element['title'] + " : " + element['backgroundImageUrl']

#    print tagids


    #url = "http://35.154.64.11/v7/genericcardsf/" + zviceID  ### test********************
    url="http://35.154.64.119/v13/genericcards/"+zviceID

    body={}
    method = "POST"

    jsonresponse = hit_url_method(body, headers1, method, url)
#    print jsonresponse
#   print "++++++++ ------------- +++++++++++"

    for card in json.loads(jsonresponse)['data']['elements']:
        if "Calendar new" == card['title']:
            calendarID = card['cardID']
            # data=card['actions']
#            print calendarID
            # print(data)
            for a in card['actions']:
                if "Explore" == a['title']:
                        print("inside")
                        actionurl = a['actionUrl']
                        method=a['method']
 #                       print(actionurl)
  #                      print(method)
                        body={}
                        jsonresponse = hit_url_method(body, headers1, method, actionurl)
                        print(jsonresponse)


                        #hardcoded

                        # for info in json.loads(jsonresponse)['data']['elements']:
                        #     data=info['content']
                        #     if '2018-04-07 05:00:00' == json.loads(data)['StartDateTime']:
                        #         print "Found"
                        #     else:
                        #         print('NOt found')
                        #     #
                            #print json.loads(data)['StartDateTime']

                        # taking input from file
                        filepath = "/home/adi/Downloads/TwigMeScripts-master/hlt7-json/siu/output/userinfo1.csv"
                        with open(filepath,"r") as rf:
                            data = csv.reader(rf, delimiter=',')
                            row1 = data.next()
                            for row in data:
                                doc=CM.force_decode(row[10]) + " " + CM.force_decode(row[11])
                                u_start_time=CM.force_decode(row[3]) + " " + CM.force_decode(row[4])#user start time
                                u_end_time = CM.force_decode(row[5]) + " " + CM.force_decode(row[6])#user end time
                                p_start_date =CM.force_decode(row[3])
                                p_start_time = CM.force_decode(row[4])
                                p_end_date = CM.force_decode(row[5])
                                p_end_time=CM.force_decode(row[6])

                            print(u_start_time)
                            print(u_end_time)
                            print(doc)

                        for info in json.loads(jsonresponse)['data']['elements']:
                            data = info['content']
                            start_time=json.loads(data)['StartDateTime']
                            end_time=json.loads(data)['EndDateTime']
                            s_date,s_time=start_time.split(' ')#splits start date and time from server data
                            e_date,e_time=end_time.split(' ')#splits end date and time from server data

                            if ( s_date==p_start_date) and (doc == json.loads(data)['tags']):# if date and doc sould be same
                                print("Here date and doc is same !!")
                                if((p_start_time< s_time and p_end_time <= s_time )or(p_start_time >= e_time and p_end_time >e_time)):
                                                print ('Here date and doc is same but time slot is available !!')
                               #  if (p_end_time < s_time) or (p_start_time > e_time):
                                                Flag=True
                                                return Flag

                                else:
                                    Flag=False
                            else:
                                Flag=True

                        return Flag

                        # for info in json.loads(jsonresponse)['data']['elements']:
                        #     data=info['content']
                        #     print(data)
                        #     if start_time== json.loads(data)['StartDateTime'] and doc == json.loads(data)['tags']:
                        #         print "Found",start_time,doc
                        #         flag=True
                        #         return flag
                        #     else:
                        #         print('NOt found')
                        #         flag=False
                        #
                        # return flag


                        # for info in json.loads(jsonresponse)['data']['elements']:
                        #     data = info['content']
                        #     print(data)
                        #     if start_time == json.loads(data)['StartDateTime'] and doc == json.loads(data)['tag']:
                        #         print "Found , Patient had already booked appointment"
                        #         Flag= True
                        #     else:
                        #         print('NOt found ,  Create a new appointment')
    #                             Flag False

                        #     #
