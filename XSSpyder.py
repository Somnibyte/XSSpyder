# Incomplete
# Crawling Issues


import requests
import unicodedata
from tld import get_tld
from bs4 import BeautifulSoup

visitedurls = []

def crawl(seed):
    if seed not in visitedurls:
        visitedurls.append(seed)
    else:
        return
    data = requests.get(seed).text
    page = BeautifulSoup(data,'html.parser')
    for link in page.findAll('a'):
        l = link.get('href')
        str_l = unicodedata.normalize('NFKD', l).encode('ascii','ignore')
        if l[0] == "/":
            l = seed + l
            str_l = unicodedata.normalize('NFKD', l).encode('ascii','ignore')
        if str_l[:4] != 'http' and str_l[:5] != 'https':
            continue
        if get_tld(seed) != get_tld(str_l):
            continue
        print(str_l)
        crawl(str_l)

def main():

    payloads = [x for x in open("payloads.txt")]
    visitedurls = []
    seed = ""

    if len(payloads) == 0:
        print ("There are no XSS vectors within the payloads.txt file")
        return
    else:

        seed = raw_input("Enter the url of the website you would like to scan for XSS vulnerabilites: (ex: http://www.google.com)")
        crawl(seed)



if __name__ == "__main__":
    main()
