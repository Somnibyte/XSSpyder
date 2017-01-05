# XSS (Cross Site Scripting) Vulnerablity Scanner
# WORK IN PROGRESS

import requests
from tld import get_tld
from bs4 import BeautifulSoup
from tqdm import tqdm

# Holds all urls that the crawler has found
visitedurls = []
# Holds all website paths that the cralwer has found
branches = []

dummy_email = "spydertest@superduperfakesuperfakeexampleemailthingy.com"
dummy_name = "dummyname"

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
    for link in tqdm(page.findAll('a')):
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

# Returns the payload for the POST request
def process_forms(payload_file, form):
    post_payload = {}

    # Get all of the tags associated with forms
    inputs = form.findAll('input')
    textareas = form.findAll('textarea')
    tags = inputs+textareas

    # Turn input data into POST payload
    for input in tqdm(tags):
        for scripts in payload_file:

            payload_text = None

            if input.get('name').encode('ascii','ignore') == 'email':
                payload_text = dummy_email
            else:
                payload_text = scripts

            keyValuePair = {input.get('name').encode('ascii','ignore'):payload_text}
            post_payload.update(keyValuePair)

    return post_payload


def verify(payload_file):
    # Loop through each wepage

    for url in visitedurls:

        # Sends a get requests for website and returns the html in text form
        data = requests.get(url).text

        # Creates a BeautifulSoup Object
        page = BeautifulSoup(data,'html.parser')

        # Find all the forms within the page
        forms = page.findAll('form')

        for form in forms:
            # Process each individual form to obtain the POST payload
            POST_payload = process_forms(payload_file, form)

            # Get the action attribute of the form
            action = form.get('action')

            # Send the POST request

            # Check if the action attribute is a full URL or a single file
            request_url = None
            if url in action:
                request_url = action
            else:
                request_url = url+action

            r = requests.post(request_url, data=POST_payload)
            print(r.text)

            # Check if the XSS payload was found in the body of the response
            if "<script>alert(\"XSS\")</script>" in r.text:
                print("------------------------------------")
                print("XSS Vulnerablity found on URL: {}".format(url))
                print("With FORM -> [{}]".format(form))
                print("------------------------------------")

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
        option = raw_input("Would you like to test 1 URL? [Type yes or no] >")
        seed = raw_input("Enter the url of the website you would like to scan for XSS vulnerabilites: (ex: http://www.google.com) >")
        if option.lower() == 'yes':
            visitedurls.append(seed)
            verify(payloads)
        else:
            maxdepth = raw_input("Enter the magnitude of the depth of the search (ex: 3) >")
            crawl(seed,int(maxdepth),currentdepth)
            print(visitedurls)
            verify(payloads)


if __name__ == "__main__":
    main()
