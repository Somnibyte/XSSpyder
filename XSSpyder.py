import mechanize
import scrapy



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
