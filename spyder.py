
# List of click commands we need
	## Command to choose payload file (Save file)
  ##Command to choose target website (Save website)
  ## Crawl entire website
  ## Target specific webpage (it'll find the form)

  ## For crawl and specific page, use a loading thing
import os

def main():
  # XSS_PAYLOADS - ENV VAR FOR PAYLOAD PATH
  # Check if this is the first time the user used this program
	if "XSS_PAYLOADS" not in os.enivron:

    # Prompt the user to type in the path
    XSS_PATH = input("Enter the file path of your xss vectors:")
    while(len(XSS_PATH) == 0):
      XSS_Path = input("Enter the file path of your xss vectors:")

    # Now set the environment variable XSS_PAYLOADS
    os.environ["XSS_PAYLOADS"] = XSS_PATH
  else:
   	# User has used this program before



  




if __name__ == '__main__':
  # run main code here
  main()
