
import requests
from bs4 import BeautifulSoup
import re
import os 

def grades():
    username = os.environ['USER']
    password = os.environ['PASS']

    login_url = " https://parentvue.cobbk12.org/./PXP2_Login_Student.aspx?regenerateSessionId=True"
    gradebook_url = "https://parentvue.cobbk12.org/PXP2_Gradebook.aspx"

    # gather site data
    print("Fetching Site Data . . .")
    try:
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
        result =  str(r.post(login_url, data = login_data, ))
        resultcheck = result.strip()

                
        if resultcheck == "<Response [200]>":
            print("Logged In")
            
        else:
            print("Site Error "+resultcheck)
            
        # pull grades from site
        print("Fetching Grade Data . . .")
        grades = r.get(gradebook_url, )
        site = grades.text
        soup = BeautifulSoup(grades.text, "html.parser")

        grade = []
        for i in range(12):
            try:
                # add grade to list, remove everything but numbers
                grade.append(re.sub('\D', '', str(soup.find_all('span', {"class":"mark"})[i])))
                
            except IndexError:
                print("Invalid Login")
                break

        
        grade = list(filter(None, grade))
        grade = [int(i) for i in grade]
        return grade
    except Exception as e:
        print("Error Occured")
        print(e)

if __name__ == "__main__":
    print(grades())
    
