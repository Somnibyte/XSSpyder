# Unfinished

import mechanize
import scrapy


# Thinking about crawling....
# Will not work
from bs4 import BeautifulSoup
import requests

url = "http://www.pixeljoint.com"
data = requests.get(url).text

page = BeautifulSoup(data,'html.parser')
vistedurls = {}

def crawl(page):
    for link in page.findAll('a'):
        link.get('href')

        print l

# File operations go here
def readFile(filename):
    currentFile = open(filename)
    # print currentFile.read()
    currentFile.close()

def main():
    browser = mechanize.Browser()
    browser.open("http://localhost:8888/new%20design/")



if __name__ == "__main__":
    main()
