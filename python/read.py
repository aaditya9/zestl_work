import BeautifulSoup
import urllib

url= 'https://en.wikipedia.org/wiki/Helmut_Hasse'
page = urllib.urlopen(url)
soup = BeautifulSoup(page.read())
