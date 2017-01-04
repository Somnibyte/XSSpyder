# XSS (Cross Site Scripting) Vulnerablity Scanner
# WORK IN PROGRESS

import requests
from tld import get_tld
from bs4 import BeautifulSoup

# Holds all urls that the crawler has found
visitedurls = []
# Holds all website paths that the cralwer has found
branches = []


def crawl(seed,maxdepth,currentdepth):

    # defines global variables
    global visitedurls
    global branches
    # Adds a website that has not already been discovered
    if seed not in visitedurls:
        visitedurls.append(seed)
    else:
        return
    # Increments the current depth of the search
    currentdepth = currentdepth + 1
    # Sends a get requests for website and returns the html in text form
    data = requests.get(seed).text
    # Creates a BeautifulSoup Object
    page = BeautifulSoup(data,'html.parser')

    # For each valid link, it will find the links within itself
    for link in page.findAll('a'):
        # Stores the href value
        l = link.get('href')
        # Checks if the href is empty
        if l == None:
            continue
        # Verfies if l stored an href value and whether it has encountred it previously
        if l[0] == "/" and l not in branches:
            branches.append(l)
            l = seed + l
        else:
            continue
        # Verifies whether l starts with http or htttps
        if l[:4] != 'http' and l[:5] != 'https':
            continue
        # Verfies whether l's domain matches the seed's domain
        if get_tld(seed) != get_tld(l):
            continue
        visitedurls.append(l)
        # Prevents going over the desired depth of crawling
        if currentdepth < maxdepth:
            crawl(l,maxdepth,currentdepth)

def verify(payloads):
        for url in visitedurls:
            for payload in payloads:
                data = requests.get(url).text       #generate payloads dicitnary comprehension with special cases of email etc
                page = BeautifulSoup(data,'html.parser')
                for form in page.findAll("input"):

                    print(form)

def main():
    # loads payload file with XSS vectors
    payloads = [x for x in open("payloads.txt")]
    # Counter for maxdepth variable
    currentdepth = 0
    # Holds the target website
    seed = ""

    # Checks to see if the payloads file is empty
    if len(payloads) == 0:
        print ("There are no XSS vectors within the payloads.txt file")
        return
    else:

        seed = raw_input("Enter the url of the website you would like to scan for XSS vulnerabilites: (ex: http://www.google.com)")
        maxdepth = raw_input("Enter the magnitude of the depth of the search (ex: 3)")

        crawl(seed,int(maxdepth),currentdepth)
        print(visitedurls)
        verify(payloads)


if __name__ == "__main__":
    main()
