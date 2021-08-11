import csv
import re
import bs4
import requests

# first parameter of class is the name of the file which should contain all resulted data > type of .txt


class Main:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    Re_Email = re.compile(r"""([a-zA-z]+
    [a-zA-Z0-9_.-]*
    @
    [a-zA-Z0-9_.-]+
    \.
    [a-zA-Z0-9_.-]+
    )""", re.VERBOSE)

    Re_Phone = re.compile(r"""(
    [(0-9)]+
    [\s\-.]+
    \d{3,4}
    [\s\-.]+
    \d{3,4}
    )""", re.VERBOSE)

    def __init__(self, return_file_txt):
        self.return_file = return_file_txt
        
    def run_scraper(self, csv_file):
        websites_list = self.return_csv_list_websites(csv_file)
        for website in websites_list:
            emails_index, phones_index = self.return_raw_data(website)
            emails_contact, phones_contact = self.return_raw_data([website[0]+"/contact"])
            no_dup_emails = self.remove_duplicates(emails_index+emails_contact)
            no_dup_phones = self.remove_duplicates(phones_index+phones_contact)
            self.write_to_file(website,no_dup_phones, no_dup_emails)

    def return_raw_data(self, website):
        try:
            response = self.get_content(website)
            if response is None:
                return [], []
            else:
                soup = bs4.BeautifulSoup(response.text, features="html.parser")
                emails = self.find_email(soup.text)
                phones = self.find_phone(soup.text)
                return emails, phones
        except Exception:
            return [], []
        
    def return_csv_list_websites(self, file_path):
        file_object = open(file_path)
        csv_object = csv.reader(file_object)
        return list(csv_object)
    
        
    def get_content(self, website):
        try:
            response = requests.get("https://www." + website[0], timeout=2, headers=self.headers)
        except requests.exceptions.SSLError:
            response = requests.get("http://www." + website[0], timeout=2, headers=self.headers)
        except Exception:
            response = None
        return response

    def find_phone(self, page_content):
        found_phones = self.Re_Phone.findall(page_content)
        return found_phones
        
    def find_email(self, page_content):
        found_emails = self.Re_Email.findall(page_content)
        return found_emails

    def write_to_file(self, website_name, phones, emails):
        with open("test.txt", "a") as result:
            result.write("Website name :{} \n".format(website_name[0]))
            result.write("Found phones : {} \n".format(phones))
            result.write("Found emails : {} \n".format(emails))
            result.write("-----------------------------------\n")
            
    def remove_duplicates(self, list):
        no_dup = []
        for item in list:
            if item in no_dup:
                continue
            else:
                no_dup.append(item)
        return no_dup

c = Main("results.txt").run_scraper("sample-websites.csv")
