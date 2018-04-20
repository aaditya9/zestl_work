for a in jsondata['data']['element']:
    cardtype = "basecard"
    if cardtype in a['cardtype']:
        print "success"