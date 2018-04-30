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


jsondata = getBaseStructure(zviceID, headers1)
    # print jsondata
tagids = []
for element in jsondata['data']['elements']:
        if element['cardtype'] == "basecard" and element['tagId'] != zviceID:
            tagids.append(element['tagId'])
        # print element['title'] + " : " + element['backgroundImageUrl']
print tagids


    #url = "http://35.154.64.11/v7/genericcardsf/" + zviceID  ### test********************
url="http://35.154.64.119/v13/genericcards/"+zviceID

body={}
method = "POST"

jsonresponse = hit_url_method(body, headers1, method, url)
# print jsonresponse
# print "++++++++ ------------- +++++++++++"

for card in json.loads(jsonresponse)['data']['elements']:
        if "Calendar new" == card['title']:
            calendarID = card['cardID']
            # data=card['actions']
            print calendarID
            # print(data)
            for a in card['actions']:
                if "Explore" == a['title']:
                        print("inside")
                        actionurl = a['actionUrl']
                        method=a['method']
                        print(actionurl)
                        print(method)
                        body={}
                        jsonresponse = hit_url_method(body, headers1, method, actionurl)
                    #    print(jsonresponse)


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
                                U_start_time=CM.force_decode(row[3]) + " " + CM.force_decode(row[4])
                                U_end_time =CM.force_decode(row[5]) + " " + CM.force_decode(row[6])
                                p_start_date = CM.force_decode(row[3])
                                u_s_time=CM.force_decode(row[4])
                                u_e_time=CM.force_decode(row[6])
                            print(doc)
                           # print(start_time)
                      #  u_s_date,u_s_time=U_start_time.split(' ')
                      #  u_e_date,u_e_time=U_end_time.split(' ')
                        list_start=[]
                        list_end=[]
                        p_start_date = CM.force_decode(row[3])
                        u_s_time = CM.force_decode(row[4])
                        u_e_time = CM.force_decode(row[6])

                        for info in json.loads(jsonresponse)['data']['elements']:
                            data=info['content']
                            print(data)
                            start_time = json.loads(data)['StartDateTime']
                            end_time = json.loads(data)['EndDateTime']

                            s_date, s_time = start_time.split(' ')  # splits start date and time from server data
                            e_date, e_time = end_time.split(' ')

                            if (s_date == p_start_date) and (doc == json.loads(data)['tags']):

                                print(start_time)
                                print(end_time)
                                list_start.append(s_time)
                                list_end.append(e_time)

                            else:
                                flag=False


                                      # if((u_s_time<[i] and u_e_time <=[i])):#or (u_s_time >=[j] and u_e_time >[j])):
                                      #           print ''
                                      #           flag1=True
                                      # else:
                                      #     flag1=False
                                      # if (u_s_time >=[j] and u_e_time >[j])==True:
                                      #           flag2=True
                                      # else:
                                      #     flag2=False
                                      #
                                      # if(flag1 or flag2)==True:
                                      #     print(flag1)
                                      #     print(flag2)
                                      #     print('SLot availble')
                                      # else:
                                      #     print('Not available')
                                      # else:
                                      #           print('Not available')
                                      #           flag=False
                                      #

                        print(list_start)
                        print(list_end)

                        for i,j in zip(list_start,list_end):
                                if u_e_time <=i:
                                        flag=True
                                elif j<=u_s_time:
                                        flag=True
                                else:
                                        flag=False

                        print flag
                        result=flag
                        print(result)










                            # if start_time== json.loads(data)['StartDateTime'] and doc == json.loads(data)['tags']:
                            #     print "Found"
                            # else:
                            #     print('NOt found')
                            #

                        # for info in json.loads(jsonresponse)['data']['elements']:
                        #     data = info['content']
                        #     print(data)
                        #     if start_time == json.loads(data)['StartDateTime'] and doc == json.loads(data)['tags']:
                        #         print "Found , Patient had already booked appointment"
                        #     else:

                        #         print('NOt found ,  Create a new appointment')

                        #     #