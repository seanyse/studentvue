import requests
from bs4 import BeautifulSoup
import time
import json

    
# initiliaztion
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Accept': 'text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0. 8' ,
        'Accept-Language': 'en-US, en;q=0.5',
        'DNT': '1',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'Accept-Encoding':'identity',
    }

login_url = " https://parentvue.cobbk12.org/./PXP2_Login_Student.aspx?regenerateSessionId=True"
gradebook_url = "https://parentvue.cobbk12.org/PXP2_Gradebook.aspx"

# gather site data

r = requests.Session()
site_data = r.get(login_url,headers=headers)
soup = BeautifulSoup(site_data.text, "html.parser")
viewstate = soup.find('input', {"id":"__VIEWSTATE"}).get('value')
viewstategen = soup.find('input', {"id":"__VIEWSTATEGENERATOR"}).get('value')
eventvalid = soup.find('input', {"id":"__EVENTVALIDATION"}).get('value')


# print(viewstate)
# print(viewstategen)
# print(eventvalid)

# create post request , login
login_data = {
    "ctl00$MainContent$username": "username here",
    "ctl00$MainContent$password": "password here",
    "ctl00$MainContent$Submit1": "Login",
    "__VIEWSTATE": viewstate,
    "__VIEWSTATEGENERATOR": viewstategen,
    "__EVENTVALIDATION": eventvalid

}


r = requests.Session()
result =  r.post(login_url, data = login_data, headers=headers)
result = str(result)
resultcheck = result.strip()

while True:
    if resultcheck == "<Response [500]>":
        print("Fetching Site Data . . .")
        r = requests.Session()
        site_data = r.get(login_url,headers=headers)
        soup = BeautifulSoup(site_data.text, "html.parser")
        viewstate = soup.find('input', {"id":"__VIEWSTATE"}).get('value')
        viewstategen = soup.find('input', {"id":"__VIEWSTATEGENERATOR"}).get('value')
        eventvalid = soup.find('input', {"id":"__EVENTVALIDATION"}).get('value')

        login_data = {
            "ctl00$MainContent$username": "1207279",
            "ctl00$MainContent$password": "swy6c40915",
            "ctl00$MainContent$Submit1": "Login",
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": viewstategen,
            "__EVENTVALIDATION": eventvalid

        }
        r = requests.Session()
        try:
            result =  r.post(login_url, data = login_data, headers=headers)
            result = str(result)
            resultcheck = result.strip()
        except Exception as e:
            print(e)
        

        print("Failed Login Retrying "+resultcheck)
        

    elif resultcheck == "<Response [200]>":
        print("Logged In")
        break
    else:
        print("Unknown Error "+resultcheck)

# pull grades from site
grades = r.get(gradebook_url, headers=headers)




site = grades.text
print("Fetching Grade Data . . .")


soup = BeautifulSoup(grades.text, "html.parser")
while True:
    try:
        grade1 = soup.find_all('span', {"class":"mark"})[0]
        grade2 = soup.find_all('span', {"class":"mark"})[1]
        grade3 = soup.find_all('span', {"class":"mark"})[2]
        grade4 = soup.find_all('span', {"class":"mark"})[3]
        grade5 = soup.find_all('span', {"class":"mark"})[4]
        grade6 = soup.find_all('span', {"class":"mark"})[5]
        break
    
    except Exception as e:
        print(e)
        time.sleep(5)
        pass

print(grade1)
print(grade2)
print(grade3)
print(grade4)
print(grade5)
print(grade6)


