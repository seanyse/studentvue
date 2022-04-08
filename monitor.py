
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import re
import os 
import time
import statistics

def monitor():
    delay = 300
    starttime = time.time()

    while True:
        old_grade = grades()

        time.sleep(delay/2 - ((time.time() - starttime) % delay)/2)
        new_grade = grades()

        if (old_grade != new_grade):
            print("Grade Change Detected")
            

            print("Sending Message . . .")
            webhook_url = os.environ['WEBHOOK'] 
            webhook = DiscordWebhook(url=webhook_url, username="StudentVue-Monitor")

            embed = DiscordEmbed(
                title="Grade Has Been Updated!", description="", color='00ff29'
            )
            # Set `inline=False` for the embed field to occupy the whole line
            embed.add_embed_field(name="Grades", value= ' '.join(map(str, new_grade)), inline=True)
            embed.add_embed_field(name="Average", value= statistics.mean(new_grade), inline=True)
            embed.add_embed_field(name="Increase", value= "undefined", inline=True)
            embed.add_embed_field(name="User", value= os.environ['USER'], inline=True)
            # embed.add_embed_field(name="Old Average", value= statistics.mean(old_grade), inline=True)

            embed.set_thumbnail(url='https://play-lh.googleusercontent.com/43vg9yqJ6keUxcLmlhILmpAGVG5q1XTpKtkUDMiggTWvzD7j_vi8bdqRI23dWnEy7A')

            webhook.add_embed(embed)
            response = webhook.execute()
            

        time.sleep(delay/2 - ((time.time() - starttime) % delay)/2)

def grades():
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
    for i in range(5):
        try:
            # add grade to list, remove everything but numbers
            grade.append(re.sub('\D', '', str(soup.find_all('span', {"class":"mark"})[i])))
        
        except IndexError:
            print("Invalid Login")
            break

    print("Fetched Grade Data")
    grade = [int(i) for i in grade]
    return grade


if __name__ == "__main__":
    monitor()
    
