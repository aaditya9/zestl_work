import requests
import BeautifulSoup
url='https://en.wikipedia.org/wiki/Helmut_Hasse'
res=requests.get(url)
print "response"

soup = BeautifulSoup(res.text)

