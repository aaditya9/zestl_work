import json
import csv
import re
import common as CM
import logon as LL
import base64
import requests
import time


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

def createStructure(keyWords, infile, ZbotID, headers1, BASE_URL, use_ext_zvice, extZvice):
    cards = splitFile(infile)

    for structure in cards:

        card = parseFile(keyWords, structure)
        print card
        try:
            print "working on card " + card['title'][0]
        except:
            print "working on card with no title - possible link card "
        if use_ext_zvice:
            card['zvice'][0] = extZvice

        if card['hier'][0] != "":
            pcardID = returnCorrectLocation(card, headers1, BASE_URL)['cardID']
        else:
            pcardID = ""
        cardID = None

        if re.search("text", card['card'][0], re.IGNORECASE):
            cardID = fetchCard(card, pcardID, BASE_URL, headers1)
            print cardID

        if re.search("gallery", card['card'][0], re.IGNORECASE):
            cardID = fetchCard(card, pcardID, BASE_URL, headers1)
            print cardID


if __name__ == "__main__":

    # BASE_URL = "https://www.twig.me/v8/"
    BASE_URL = "http://35.154.64.11/v8/"
    email = 'admin@zestl.com'
    pwd = 'TwigMeNow'
    ZbotID = "876MD568TAUH2"
    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
    keyWords = ['title','card','zvice','hier']
    infile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_users.csv"
    use_ext_zvice = False
    extZvice = ""
    createStructure(keyWords, infile, ZbotID, headers1, BASE_URL, use_ext_zvice, extZvice)