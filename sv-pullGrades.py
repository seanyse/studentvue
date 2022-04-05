import requests
from bs4 import BeautifulSoup
import time
import json
import os 

username = os.environ['USER']
password = os.environ['PASS']

login_url = " https://parentvue.cobbk12.org/./PXP2_Login_Student.aspx?regenerateSessionId=True"
gradebook_url = "https://parentvue.cobbk12.org/PXP2_Gradebook.aspx"

# gather site data
print("Fetching Site Data . . .")
r = requests.Session()
site_data = r.get(login_url)
soup = BeautifulSoup(site_data.text, "html.parser")
viewstate = soup.find('input', {"id":"__VIEWSTATE"}).get('value')
viewstategen = soup.find('input', {"id":"__VIEWSTATEGENERATOR"}).get('value')
eventvalid = soup.find('input', {"id":"__EVENTVALIDATION"}).get('value')


# create post request payload , login
login_data = {
    "__VIEWSTATE": viewstate,
    "__VIEWSTATEGENERATOR": viewstategen,
    "__EVENTVALIDATION": eventvalid,
    "ctl00$MainContent$username": username,
    "ctl00$MainContent$password": password,
    "ctl00$MainContent$Submit1": "Login",
}

print("Attemping Login . . .")
result =  r.post(login_url, data = login_data, )
result = str(result)
resultcheck = result.strip()


while True:
    if resultcheck == "<Response [500]>":
        print("Invalid Site Data, Refreshing . . .")
        r = requests.Session()
        site_data = r.get(login_url,)
        soup = BeautifulSoup(site_data.text, "html.parser")
        viewstate = soup.find('input', {"id":"__VIEWSTATE"}).get('value')
        viewstategen = soup.find('input', {"id":"__VIEWSTATEGENERATOR"}).get('value')
        eventvalid = soup.find('input', {"id":"__EVENTVALIDATION"}).get('value')

        
        r = requests.Session()
        try:
            result =  r.post(login_url, data = login_data,)
            result = str(result)
            resultcheck = result.strip()
        except Exception as e:
            print(e)
        

        
        

    elif resultcheck == "<Response [200]>":
        print("Logged In")
        break
    else:
        print("Unknown Error "+resultcheck)

# pull grades from site
print("Fetching Grade Data . . .")
grades = r.get(gradebook_url, )


site = grades.text



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
    
    except IndexError:
        print("Invalid Login")
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
