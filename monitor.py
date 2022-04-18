
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import re
import os 
import time
import statistics
from datetime import datetime

def monitor():
    delay = 300
    

    while True:
        try:
            old_grade = new_grade
            
        except:
            old_grade = grades()

        time.sleep(delay)
        new_grade = grades()

        if (old_grade != new_grade):
            print("Grade Change Detected")
            

            print("Sending Message . . .")
            # gemerate webhook
            webhook_url = os.environ['WEBHOOK'] 
            webhook = DiscordWebhook(url=webhook_url, username="StudentVue-Monitor")

            embed = DiscordEmbed(
                title="Grade Has Been Updated!", description="", color='00ff29'
            )
            
            embed.add_embed_field(name="Grades", value= ' '.join(map(str, new_grade)), inline=True)
            embed.add_embed_field(name="Average", value= str(statistics.mean(new_grade)), inline=True)
            embed.add_embed_field(name="Increase", value= "undefined", inline=True)
            embed.add_embed_field(name="User", value= os.environ['USER'], inline=True)
            embed.add_embed_field(name="Old Average", value= str(statistics.mean(old_grade)), inline=True)

            embed.set_thumbnail(url='https://play-lh.googleusercontent.com/43vg9yqJ6keUxcLmlhILmpAGVG5q1XTpKtkUDMiggTWvzD7j_vi8bdqRI23dWnEy7A')

            embed.set_footer(text="studentvue-monitor")

            embed.set_timestamp()

            webhook.add_embed(embed)
            response = webhook.execute()
            

        time.sleep(delay)

def grades():

    while True:
        try:
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
            for i in range(12):
                try:
                    # add grade to list, remove everything but numbers
                    grade.append(re.sub('\D', '', str(soup.find_all('span', {"class":"mark"})[i])))
                    
                except IndexError:
                    print("Invalid Login")
                    break

            
            grade = list(filter(None, grade))
            grade = [int(i) for i in grade]
            print("Fetched Grade Data")
            print(grade)
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            print("Current Time:", current_time)
            return grade

        except Exception as e:
            print("Error Occured")
            print(e)


if __name__ == "__main__":
    monitor()
    
