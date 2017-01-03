# Crawling Complete
# Form Testing Incomplete

import requests
import unicodedata
from tld import get_tld
from bs4 import BeautifulSoup

visitedurls = []
branches = []

def crawl(seed,depth):

    # defines global variables
    global visitedurls
    global branches
    max = 0

    if seed not in visitedurls:
        visitedurls.append(seed)
    else:
        return
    data = requests.get(seed).text
    page = BeautifulSoup(data,'html.parser')
    for link in page.findAll('a'):
        l = link.get('href')
        if l == None:
            continue
        if l[0] == "/" and l not in branches:
            branches.append(l)
            l = seed + l
        else:
            continue
        if l[:4] != 'http' and l[:5] != 'https':
            continue
        if get_tld(seed) != get_tld(l):
            continue
        print(l)
        crawl(l,depth)

def main():

    payloads = [x for x in open("payloads.txt")]
    visitedurls = []
    seed = ""

    if len(payloads) == 0:
        print ("There are no XSS vectors within the payloads.txt file")
        return
    else:

        seed = raw_input("Enter the url of the website you would like to scan for XSS vulnerabilites: (ex: http://www.google.com)")
        depth = raw_input("Enter the magnitude of the depth of the search (ex: 3)")

        crawl(seed,depth)



if __name__ == "__main__":
    main()
