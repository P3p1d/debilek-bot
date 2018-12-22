import urllib.request
from bs4 import BeautifulSoup
breaking = "<br/>"
url="http://vtipy.atropin.cz/1--vtipy--nahodny-vtip"
def vtipek():
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    polivka = str(soup)
    polivka = polivka.split("</p><br/><p>")
    polivka = polivka[1].split("<b>")
    polivka = polivka[1].split("</b>")
    polivka = polivka[0].replace(breaking,"\n")
    return polivka[0:]