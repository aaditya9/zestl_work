

import json

import logon as LL
import common as CM



# SERVER = "https://twig.me/"
SERVER = "http://52.52.18.8/"

version = "v11/"
BASE_URL = SERVER + version

zviceID = "9J5EDAR3Y2PZA"

urlAdd = "genericcards/" + zviceID

email = "admin@zestl.com"
pwd = "zsplADMIN999"

url = 'http://52.52.18.8/v11/zvice/detailscard/9J5EDAR3Y2PZA'
# url = 'https://twig.me/v11/zvice/detailscard/9J5EDAR3Y2PZA'
method = "POST"

body = {}

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.hit_url_method(body, headers1, method, url)
jsondata = json.loads(jsondata)

for element in jsondata['data']['elements']:
    if element['genericCardType'] == 'DepartmentsCard' and 'Nursery' not in element['title']:
        print element['title']
        url = element['actions'][1]['actionUrl']
        method = "GET"
        jdata = CM.hit_url_method(body, headers1, method, url)
        jdata = json.loads(jdata)
        for jelement in jdata['data']['elements']:
            if "Activities for" in jelement['title']:
                print jelement['title']
                url = jelement['actions'][0]['actionUrl']
                bdata = jelement['actions'][0]['inputs']
                # v1 = jelement['actions'][0]['inputs'][3]['properties'][1]['value']
                v1 = json.loads(jelement['actions'][0]['inputs'][3]['properties'][1]['value'])
                topjson = jelement['actions'][0]['inputs']
                writer1 = {}

                for ele in v1:
                    arry1 = []
                    if ele['properties'][0]['name'] == "id":
                        name = ele['properties'][0]['value']
                        # val = ele['properties'][1]['value']
                        val = json.loads(ele['properties'][1]['value'])
                        dict1 = {}
                        for e1 in val:
                            n1 = e1['properties'][0]['value']
                            n1 = json.loads(e1['properties'][0]['value'])
                            for val1 in n1:
                                dict1[val1['properties'][0]['value']] = val1['properties'][1]['value']
                            arry1.append(dict1.copy())
                    else:
                        a = 1
                    try:
                        writer1[name] = arry1
                    except:
                        a = 2

                body = writer1

                #
                body = {}
                for inp1 in topjson:
                    key1 = inp1['properties'][0]['value']
                    body[key1] = inp1['properties'][1]['value']

                for i in range(0, len(writer1['GALLERY'])-1):
                    if writer1['GALLERY'][i]['label'] == "Publish":
                        writer1['GALLERY'][i]['operator'] = "false"
                body['ActionPref'] = writer1
                method = "POST"
                jsondata = CM.hit_url_method(body, headers1, method, url)
                jsondata = json.loads(jsondata)
                print jsondata['message']