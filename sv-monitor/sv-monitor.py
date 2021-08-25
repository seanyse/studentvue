import requests
from bs4 import BeautifulSoup
import time
import json
from statistics import mean

global webhook_url
global username 
global password

webhook_url = "https://discord.com/api/webhooks/879913833987178496/F4fCgQwiTVKl4FezBvAGF0p1yY5haAUiS_1wY9dpSHrEU1LRBxha_DHTTmkB45XDPzPc"
username = "1207279"
password = "swy6c40915"

def pull_grades():
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
    print("Fetching Site Data . . .")
    r = requests.Session()
    site_data = r.get(login_url,headers=headers)
    soup = BeautifulSoup(site_data.text, "html.parser")
    viewstate = soup.find('input', {"id":"__VIEWSTATE"}).get('value')
    viewstategen = soup.find('input', {"id":"__VIEWSTATEGENERATOR"}).get('value')
    eventvalid = soup.find('input', {"id":"__EVENTVALIDATION"}).get('value')


    # print(viewstate)
    # print(viewstategen)
    # print(eventvalid)

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
    r = requests.Session()
    result =  r.post(login_url, data = login_data, headers=headers)
    result = str(result)
    resultcheck = result.strip()


    while True:
        if resultcheck == "<Response [500]>":
            print("Invalid Site Data, Refreshing . . .")
            r = requests.Session()
            site_data = r.get(login_url,headers=headers)
            soup = BeautifulSoup(site_data.text, "html.parser")
            viewstate = soup.find('input', {"id":"__VIEWSTATE"}).get('value')
            viewstategen = soup.find('input', {"id":"__VIEWSTATEGENERATOR"}).get('value')
            eventvalid = soup.find('input', {"id":"__EVENTVALIDATION"}).get('value')

            
            r = requests.Session()
            try:
                result =  r.post(login_url, data = login_data, headers=headers)
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
    grades = r.get(gradebook_url, headers=headers)
    soup = BeautifulSoup(grades.text, "html.parser")

    while True:
        try:
            grade1 = soup.find_all('span', {"class":"mark"})[0]
            grade2 = soup.find_all('span', {"class":"mark"})[1]
            grade3 = soup.find_all('span', {"class":"mark"})[2]
            grade4 = soup.find_all('span', {"class":"mark"})[3]
            grade5 = soup.find_all('span', {"class":"mark"})[4]
            grade6 = soup.find_all('span', {"class":"mark"})[5]
            print("Grades Fetched")
            break
        
        except IndexError:
            print("Invalid Login")
            break
        
        except Exception as e:
            print(e)
            time.sleep(5)
            pass
    
    grade = str(grade1) + ',' + str(grade2) + ',' + str(grade3) + ',' + str(grade4) + ',' + str(grade5) + ',' + str(grade6) 
    grade = grade.replace('<span class="mark">', "").replace("</span>", "")
    return grade
    
if __name__ == "__main__":
    while True:
        new_grades = pull_grades()
        print(new_grades)
        old_grades = ""

        while True:
            if old_grades == "":
                old_grades = pull_grades()

            elif new_grades != old_grades:
                list_grade = new_grades.split(",")
                average = mean(list_grade)

                # create discord webhook

                discord_payload = {
                    {
                    "content": "null",
                    "embeds": [
                        {
                        "title": "Grade Has Been Updated!",
                        "url": "https://parentvue.cobbk12.org/PXP2_Gradebook.aspx?AGU=0&studentGU=0590CF3A-0F36-446A-9047-7D12B0C374B8",
                        "color": 65386,
                        "fields": [
                            {
                            "name": "Updated Grades:",
                            "value": new_grades,
                            "inline": "true"
                            },
                            {
                            "name": "Average",
                            "value": average,
                            "inline": "true"
                            },
                            {
                            "name": "Increase",
                            "value": "undefined",
                            "inline": "true"
                            },
                            {
                            "name": "Username",
                            "value": username,
                            "inline": "true"
                            },
                            {
                            "name": "Password",
                            "value": password,
                            "inline": "true"
                            }
                        ],
                        "thumbnail": {
                            "url": "https://play-lh.googleusercontent.com/43vg9yqJ6keUxcLmlhILmpAGVG5q1XTpKtkUDMiggTWvzD7j_vi8bdqRI23dWnEy7A"
                        }
                        }
                    ],
                    "username": "StudentVue-Monitor"
                    }
                }
                r = requests.session()
                r.post(url=webhook_url, data=discord_payload)

                old_grades = pull_grades()
                print(old_grades)

            elif new_grades == old_grades:
                print("nothing new detected, sleeping")
                time.sleep(3600)
                old_grades = pull_grades()
                print(old_grades)
            
            else:
                print("someting went wrong")
             


