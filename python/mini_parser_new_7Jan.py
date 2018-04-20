import json
import csv
import re
import common as CM
import logon as LL
import create_text_cards_14_Jan as TC
import base64
import requests


def grpLinks(headers1, ZbotID, BASE_URL):
    usergroups = TC.getAllUserGroups(headers1, ZbotID, BASE_URL)
    shareIcons = {}

    for element in json.loads(usergroups)['data']['elements']:
        if element['title'] != None and element['title'] != "Linked Users" and element['title'] != "All Org Users":
            try:
                st = element['actions'][3]['data']
                st = json.loads(st)
                shareIcons[element['title']] = st['shareText']
            except KeyError:
                print "keyerror on " + element['title']
    return shareIcons

def createCalendarCard(headers1, ZbotID, BASE_URL, pcardID, card):
    r = requests.get("http://twig.me/v1/push/dectest/" + card['zvice'][0])
    tagnum = r.json()['decTagID']
    # r = requests.get("http://twig.me/v1/push/dectest/" + ZbotID)
    # zbotnum = r.json()['decTagID']
    if len(card['description']) > 0:
        desc = card['description'][0]
    else:
        desc = ""
    url = BASE_URL + "zvice/interaction/" + card['zvice'][0]
    method = "POST"
    body = {"Title": card['title'][0], "Description": desc,
            "interactionID": "CommonInteraction_INTERACTION_TYPE_ADD_CALENDAR",
            "ZviceID": tagnum, "categorytype": "Calendar", "LinkType": "CALENDAR",
            "parentCardID": pcardID}
    jsonreply = json.loads(CM.hit_url_method(body, headers1, method, url))
    return jsonreply['cardid']

def createGalleryrCard(headers1, BASE_URL, pcardID, card):
    if len(card['description']) > 0:
        desc = card['description'][0]
    else:
        desc = ""
    url = BASE_URL + card['zvice'][0] + "/gallery"
    method = "POST"
    body = {"Title": card['title'][0], "Description": desc, "parentCardID": pcardID}
    jsonreply = json.loads(CM.hit_url_method(body, headers1, method, url))
    return jsonreply['cardid']

def createLinkCard(headers1, ZbotID, BASE_URL, pcardID, linkgrpname, zviceID):
    shareIcons = grpLinks(headers1, ZbotID, BASE_URL)
    link = shareIcons[linkgrpname]  # print link
    url = BASE_URL + "zvice/interaction/" + zviceID
    method = "POST"
    body = {}
    body['cardData'] = {"title": linkgrpname, "link": link}
    body['cardType'] = "LINK"
    body['opType'] = 1
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
    body['parentCardID'] = str(pcardID)

    jsonreply = json.loads(CM.hit_url_method(body, headers1, method, url))
    # print json.loads(jsonreply)
    return jsonreply['cardid']

def splitFile(infile):
    subp = []
    cards = []
    with open(infile, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        for row in data:
            if re.search(r'\(card\)', row[0], re.IGNORECASE):
                if len(subp) > 0:
                    cards.append(subp)
                subp = []
                subp.append(row[0])
            else:
                subp.append(row[0])
        cards.append(subp)
    return cards

def create_form_contents(cardID, BASE_URL, headers1, card, csvFile, title):
    csvFile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/" + csvFile
    method = "GET"
    hasHeader1 = "Y"
    url = BASE_URL + card['zvice'][0] + "/forms/" + str(cardID)
    body = {}
    j1 = json.loads(CM.hit_url_method(body, headers1, method, url))
    for element in j1['data']['elements']:
        if title in element['title']:
            # print element['title']
            print title + " found"
            print "============================"
            for action in element['actions']:
                # print action
                if 'More Actions' in action['title']:
                    for a in action['actions']:
                        if "Edit" in a['title']:
                            url = a['actionUrl']
                            data = json.loads(a['data'])
                            method = a['method']
                            print " &&&&&&&&&&&&&&&&&&&&&&& "
                            body = {}

                            body["FormDescription"] = data["FormDescription"]
                            body["FormID"] = data["FormID"]

                            body["FormTitle"] = data["FormTitle"]
                            # body["ZviceID"]=  "CVEPKDHYA2FCS"
                            body["ZviceID"] = data["ZviceID"]
                            body["ZbotID"] = data["ZbotID"]
                            body["ModifiedBy"] = data["ModifiedBy"]
                            body["DateModified"] = data["DateModified"]
                            body["CreatedBy"] = data["CreatedBy"]
                            body["DateCreated"] = data["DateCreated"]
                            body["query"] = data["query"]
                            body["Flags"] = data["Flags"]
                            zeroelem = {}
                            # print data['Elements']
                            passthrough = True
                            if passthrough:
                                tempAr = []
                                zeroelem["ElementType"] = "SECTION"
                                zeroelem["SequenceNo"] = 1
                                zeroelem["FieldLabel"] = title
                                elarray = []
                                with open(csvFile, 'r') as my_file:
                                    data1 = csv.reader(my_file, delimiter=',')
                                    if hasHeader1 == "Y":
                                        row1 = data1.next()
                                    seqNo = 1
                                    for row in data1:

                                        elID = row[0]
                                        fldlabel = row[0]
                                        type = row[1]
                                        hint = row[2]
                                        req = row[3]
                                        seqNo += 1
                                        addElement = {}
                                        addElement['ElementID'] = elID
                                        addElement['ElementType'] = type
                                        addElement['FieldLabel'] = fldlabel
                                        addElement['Hint'] = hint
                                        addElement['Required'] = req
                                        addElement['SequenceNo'] = seqNo
                                        if type == "SPINNER" or type == "RADIO_GROUP":
                                            spinelements = row[4].split(";")
                                            addElement['Options'] = spinelements
                                        elarray.append(dict(addElement))

                                zeroelem['Elements'] = elarray
                                tempAr.append(dict(zeroelem))

                            body['Elements'] = tempAr

                            body['DataSource'] = data['DataSource']

                            # print body

                            jsonresponse = CM.hit_url_method(body, headers1, method, url)
                            print " &&&&&&&&&&&&&&&&&&&&&&& "
                            print jsonresponse
    return


def parseFile(keyWords, data):
    card = {}
    for word in keyWords:
        card[word] = []
        for row in data:
            sString = "(" + word + ")"
            if sString in row.lower():
                dd = re.search(r'(.*)\(%s' % sString, row, re.IGNORECASE)
                dd = dd.group(1).strip()
                card[word].append(dd)
    return card

def unpaginate(inp, elements):
    for element in inp:
        if element['cardtype'] == "nextcard":
            url = element['url']
            method = element['method']
            body = json.loads(element['content'])
            jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
            elements = unpaginate(jsondata['data']['elements'], elements)
        else:
            elements.append(element)
    return elements


def returnCorrectLocation(card, headers1, BASE_URL):
    hiers = card['hier'][0].split(';')
    for i in range(len(hiers)):
        hiers[i] = hiers[i].strip()
        # print hiers(i).strip()
    jsondata = CM.getBaseStructure(card['zvice'][0], headers1, BASE_URL)
    if len(hiers) > 0:
        for i in range(len(hiers)):
            print hiers[i]
            elements = []
            elements = unpaginate(jsondata['data']['elements'], elements)
            for element in elements:
                if element['title'].strip() == hiers[i].strip():
                    if "buttoncard" in element['cardtype']:
                        url = element['actions'][0]['actionUrl']
                        method = element['actions'][0]['method']
                        body = {}
                        jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
                        for a in jsondata['data']['elements']:
                            if a['title'].strip() == hiers[i].strip():
                                el = a
                    else:
                        for b in jsondata['data']['elements']:
                            if b['title'].strip() == hiers[i].strip():
                                el = b
                        try:
                            url = element['cturl']
                            method = element['ctmethod']
                            body = json.loads(element['ctjsondata'])
                            jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
                        except:
                            print "No hierarchies"
    return el

def setCardAttributes(card, ZbotID, headers1, cardID):
    if len(card['view']) > 0:
        for vp in card['view']:
            TC.set_card_permissions(vp, cardID, card['zvice'][0], "VIEW", headers1, ZbotID)
    if len(card['admin']) > 0:
        for vp in card['admin']:
            TC.set_card_permissions(vp, cardID, card['zvice'][0], "ADMIN", headers1, ZbotID)
    if len(card['comm pref mail']) > 0:
        for vp in card['comm pref mail']:
            TC.set_card_permissions(vp, cardID, card['zvice'][0], "MAIL", headers1, ZbotID)
    if len(card['comm pref sms']) > 0:
        for vp in card['comm pref sms']:
            TC.set_card_permissions(vp, cardID, card['zvice'][0], "SMS", headers1, ZbotID)
    if len(card['allowed']) > 0:
        for vp in card['allowed']:
            TC.set_card_permissions(vp, cardID, card['zvice'][0], "ALLOWED_USERS", headers1, ZbotID)
    if len(card['auto notification']) > 0:
        body = {'cardType': 'GenericCard', 'cardID': cardID, 'policyType': 'AUTO_UPDATE_CARD_MAIL', 'policyVal': "true"}
        method = "POST"
        url = 'https://twig.me/v5/cards/policy/' + card['zvice'][0]
        CM.hit_url_method(body, headers1, method, url)
    if len(card['profile image']) > 0:
        url = BASE_URL + "cards/" + str(cardID) + "/bgimage/" + card['zvice'][0]
        method = "POST"
        imgFile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/tempimages/" + \
                  card['profile image'][0]
        with open(imgFile, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        encoded_string = encoded_string.encode('utf8')
        # print encoded_string\
        typ = "img/jpg"
        body = {}
        body['media'] = encoded_string
        body['media_type'] = typ
        body['media_ext'] = "jpg"
        body['media_size'] = 120000
        body['media_name'] = card['profile image'][0]
        body['remove'] = 'false'
        print CM.hit_url_method(body, headers1, method, url)
        print "done"
    return

def create_form(card, zbotID, parentUID):
    method = "POST"
    r = requests.get("http://twig.me/v1/push/dectest/" + card['zvice'][0])
    tagnum = r.json()['decTagID']
    r = requests.get("http://twig.me/v1/push/dectest/" + zbotID)
    zbotnum = r.json()['decTagID']
    if len(card['description']) > 0:
        desc = card['description'][0]
    else:
        desc = ""
    body = {"FormID": "", "FormDescription": desc, "FormTitle": card['title'][0],
            "ZviceID": tagnum, "ZbotID": zbotnum, "LinkType": "FORM", "LinkID": "",
            "parentCardID": parentUID}
    url = 'https://twig.me/v5/EUNXYEQF7TGHR/forms'
    jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
    return jsondata['cardid']

def fetchCard(card, parent, BASE_URL, headers1):
    if parent == "":
        j2 = CM.getBaseStructure(card['zvice'][0], headers1, BASE_URL)
        for element in j2['data']['elements']:
            if element['title'].strip() == card['title'][0].strip():
                return element['cardID']
    else:
        url = BASE_URL + "genericcards/" + card['zvice'][0]
        body = {'parentCardID': parent}
        method = "POST"
        jsondata = json.loads(CM.hit_url_method(body, headers1, method, url))
        for element in jsondata['data']['elements']:
            if element['title'].strip() == card['title'][0].strip():
                return element['cardID']

def createStructure(keyWords, infile, ZbotID, headers1, BASE_URL, use_ext_zvice, extZvice):

        cards = splitFile(infile)

        for structure in cards:

            card = parseFile(keyWords, structure)
            try:
                print "working on card " +  card['title'][0]
            except:
                print "working on card with no title - possible link card "
            if use_ext_zvice:
                card['zvice'][0] = extZvice

            if card['hier'][0] != "":
                pcardID = returnCorrectLocation(card, headers1, BASE_URL)['cardID']
            else:
                pcardID = ""
            if re.search("text", card['card'][0], re.IGNORECASE):
                if len(card['new']) > 0:
                    if len (card['description']) > 0:
                        cardID = TC.create_txt_card(card['title'][0], card['description'][0], card['zvice'][0], headers1, pcardID)
                    else:
                        cardID = TC.create_txt_card(card['title'][0], "", card['zvice'][0], headers1, pcardID)
                else:
                    cardID = fetchCard(card, pcardID, BASE_URL, headers1)
                    # print ""
                    setCardAttributes(card, ZbotID, headers1, cardID)
            if re.search("form", card['card'][0], re.IGNORECASE):
                if len(card['new']) > 0:
                    if len(card['description']) > 0:
                        cardID = create_form(card, ZbotID, pcardID)
                    else:
                        cardID = create_form(card, ZbotID, pcardID)
                        # print ""
                else:
                    cardID = fetchCard(card, pcardID, BASE_URL, headers1)
                if len(card['formcsv']) > 0:
                    create_form_contents(cardID, BASE_URL, headers1, card, card['formcsv'][0], card['title'][0])
                setCardAttributes(card, ZbotID, headers1, cardID)
            if re.search("link", card['card'][0], re.IGNORECASE):
                if len(card['new']) > 0:
                    if len(card['user group']) > 0:
                        cardID = createLinkCard(headers1, ZbotID, BASE_URL, pcardID, card['user group'][0], card['zvice'][0])
                else:
                    cardID = fetchCard(card, pcardID, BASE_URL, headers1)
                setCardAttributes(card, ZbotID, headers1, cardID)
            if re.search("calendar", card['card'][0], re.IGNORECASE):
                if len(card['new']) > 0:
                    cardID = createCalendarCard(headers1, ZbotID, BASE_URL, pcardID, card['title'][0], card['zvice'][0])
                else:
                    cardID = fetchCard(card, pcardID, BASE_URL, headers1)
                setCardAttributes(card, ZbotID, headers1, cardID)

            if re.search("gallery", card['card'][0], re.IGNORECASE):
                if len(card['new']) > 0:
                    # print "not supported"
                    cardID = createGalleryrCard(headers1, BASE_URL, pcardID, card)
                else:
                    cardID = fetchCard(card, pcardID, BASE_URL, headers1)
                setCardAttributes(card, ZbotID, headers1, cardID)

            if re.search("forum", card['card'][0], re.IGNORECASE):
                if len(card['new']) > 0:
                    print "not supported"
                    # cardID = createCalendarCard(headers1, ZbotID, BASE_URL, pcardID, card['title'][0], card['zvice'][0])
                else:
                    cardID = fetchCard(card, pcardID, BASE_URL, headers1)
                setCardAttributes(card, ZbotID, headers1, cardID)
        return
            ### write the card here

if __name__ == "__main__":

    BASE_URL = "https://www.twig.me/v5/"
    email = 'admin@zestl.com'
    pwd = 'Zspladmin99'
    ZbotID = "B969YSR37AT7G" ## indus
    # ZbotID = "8SFBUKFZCALEE" ##gold's
    # ZbotID = "BP35PXQDYZ3F6"  # Saptapadi
    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

    keyWords = ['admin', 'view', 'comm pref mail', 'comm pref sms', 'title', 'description', 'check mail', 'check notification', 'zvice', 'hier', 'auto notification', 'card', 'profile image', 'allowed', 'formcsv', 'user group', 'new']

    # infile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/CardStructure_Saptapadi.csv"
    infile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/MYP_HW_Structure.csv"
    use_ext_zvice = False
    extZvice = False

    createStructure(keyWords, infile, ZbotID, headers1, BASE_URL, use_ext_zvice, extZvice)


