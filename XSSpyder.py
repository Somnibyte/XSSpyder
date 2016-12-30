import os
import scrapy


def main():
    # First run check
    if "XSS_PAYLOADS" not in os.environ:
        # Prompt the user to enter the payload path
        XSS_PAYLOADS = raw_input("Enter the file path of your xss vectors: ")

        while (len(XSS_PAYLOADS) == 0):
            XSS_PAYLOADS = raw_input("Enter the filepath of your xss vectors: ")

        # Now set the environment variable 'XSS_PAYLOADS'
        os.environ["XSS_PAYLOADS"] = XSS_PAYLOADS
    else:
        # User has used this program before
        # Checks to see if user would like to edit the filepath of payload
        editpath = raw_input("Would you like edit the payload path? [Y OR N] ")

        # Edits filepath of payload
        if editpath == 'Y':
            editpath = raw_input("Enter the new filepath")
            os.environ["XSS_PAYLOADS"] = editpath
            print("Filepath has been edited to {}!").format(editpath)
        print("Payload path initialized!")


if __name__ == "__main__":
    main()
