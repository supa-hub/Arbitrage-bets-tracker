"""
#elem = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/section/div[1]/div/div[1]/div/div/div[1]/a/span[2]")))
#driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div/div/section/div[4]/div[2]/div[2]'))
#soppa = BeautifulSoup(driver.page_source, "html.parser")
#elem = driver.find_element_by_xpath("/html/body/div/div/section/div[4]/div[2]/div[2]/div[2]/div[1]/a/span[1]/span/span[2]/span[2]")
#text = soppa.find('span', {'class': 'Details__ParticipantName'})
#print(soppa.prettify)
#print(elem)
"""

from argparse import Namespace
from distutils.fancy_getopt import OptionDummy
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time
from bs4 import BeautifulSoup

import requests

import json


class tracker:
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument('--disable-blink-features=AutomationControlled')
        self.option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36")

        webdriver_path = Path("chromedriver.exe")
        self.driver = webdriver.Chrome(webdriver_path,options=self.option)

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        self.teams_dict = {     
            "website":"",
            "home_team":"",
            "away_team":"",
            "home_odds":"",
            "draw_odds":"",
            "away_odds":"",
            }

        self.teams_dict2 = {
            "home_team":"",
            "away_team":"",
            "home_odds":"",
            "draw_odds":"",
            "away_odds":"",
            }

        with open("names.json","r") as json_file:
            self.names_dict = json.load(json_file)



        

    def get_the_pinnacle_odds(self, links):
        headers = {
            "accept":"application/json",
            "content-type":"application/json",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
            "x-api-key":"CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R"
        }

        r = requests.get("https://guest.api.arcadia.pinnacle.com/0.1/leagues/1842/matchups")
        r2 = requests.get("https://guest.api.arcadia.pinnacle.com/0.1/leagues/1842/markets/straight", headers=headers)

        json_data_matchups = json.loads(r.text)
        json_data_odds = json.loads(r2.text)
        
        list_of_team_names = []
        list_of_teams_dict = []

        self.driver.get(links)
        time.sleep(12)

        team_names_string = "//*[@class='ellipsis event-row-participant style_participant__H8-ku']"

        team_names_string = self.driver.find_elements(by=By.XPATH, value=team_names_string)
                    
        
        y = 0
        teams_dict2 = self.teams_dict.copy()
        for names in team_names_string:           
            
            teams_dict2["website"] = "pinnacle"   #for writing into csv I used this

            if y == 0:
                teams_dict2["home_team"] = names.text
                y += 1
            if y == 1:
                if teams_dict2["home_team"] != names.text:
                    teams_dict2["away_team"] = names.text
                    y += 1

            if y == 2:
                list_of_teams_dict.append(teams_dict2)
                #print(list_of_teams_dict)
                teams_dict2 = self.teams_dict.copy()
                y = 0

        #print(list_of_teams_dict)

        num_for_names = 0
        yy = 0

        odds_string = "//*[@class='style_price__15SlF']"
        elements = self.driver.find_elements(by=By.XPATH, value=odds_string)
        if len(elements) != 0:
            for elems in elements:
                #print(len(elements), "jooo its length")

                if yy == 0:
                    odds_name = "home_odds" 
                    list_of_teams_dict[num_for_names][odds_name] = elems.text
                if yy == 1:
                    odds_name = "draw_odds"
                    list_of_teams_dict[num_for_names][odds_name] = elems.text
                if yy == 2:
                    odds_name = "away_odds" 
                    list_of_teams_dict[num_for_names][odds_name] = elems.text
                    num_for_names += 1
                    yy = -1

                            #print(list_of_teams_dict[num_for_names])
                yy += 1


        

        list_of_teams_dict2 = {"website":"pinnacle", "moneyline":list_of_teams_dict}
        list_of_teams_dict = {"moneyline":list_of_teams_dict}

        return list_of_teams_dict2

    
    def get_the_betway_odds(self,links):


        list_of_teams_dict = []

        self.driver.get(links)
        time.sleep(12)
        teams_string = "//*[@class='teamNameEllipsisContainer']"
        elems = self.driver.find_elements(by=By.XPATH, value=teams_string)
        #elem = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, odd_string)))


        y = 0
        teams_dict2 = self.teams_dict.copy()
        
        for elem in elems:    #loop in which we sort the team names into the home and away team
            teams_dict2["website"] = "betway"
            for names1 in self.names_dict["teams"]:
                if elem.text in names1["names"]:
                    replace_name = names1["replace_name"]

                else:
                    replace_name = elem.text

                if y == 0:

                    teams_dict2["home_team"] = replace_name

                if y == 1:
                    teams_dict2["away_team"] = replace_name
                    list_of_teams_dict.append(teams_dict2)
                    teams_dict2 = self.teams_dict.copy()
                    y = -1
                 
                
            y += 1

        odd_string = "//*[@class='odds']"
        elems = self.driver.find_elements(by=By.XPATH, value=odd_string)
        
        yy = 0
        xx = 0
        for elem2 in elems:

            if yy == 0:
                list_of_teams_dict[xx]["home_odds"] = elem2.text

            if yy == 1:
                list_of_teams_dict[xx]["draw_odds"] = elem2.text

            if yy == 2:
                list_of_teams_dict[xx]["away_odds"] = elem2.text
                yy = -1
                xx += 1

            yy += 1
            
                


        list_of_teams_dict2 = {"website":"betway", "moneyline":list_of_teams_dict}
        #list_of_teams_dict = {"moneyline":list_of_teams_dict}
                
        
        return list_of_teams_dict2


    
    def get_the_888sport_odds(self,links):
        headers  = {
            "origin":"https://www.888sport.com",
            "referer":"https://www.888sport.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
            "cookie":"odds_format=AMERICAN; anon_hash=e56af4dae97fda70c124987d0ed1d6e4; spectate_session=f1171329-9779-475d-a1c6-82b868dea5b3%3Aanon; bbsess=N6-eJ3MkpNheBkSaqlvG2F7wRE6; lang=fin; 888Cookie=lang%3Dfi%26OSR%3D485472%26RefType%3DNoReferrer%26TestData%3D%7B%22country%22%3A%22fin%22%2C%22last-referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22mm_id%22%3A%2242402%22%2C%22orig-lp%22%3A%22https%3A%2F%2Fwww.888sport.com%2Fspt%2F100percent.htm%22%2C%22referrer%22%3A%22NULL%22%2C%22utm_campaign%22%3A%22100082733_1740982_nodescription%22%2C%22utm_content%22%3A%22100082733%22%2C%22utm_medium%22%3A%22casap%22%2C%22utm_source%22%3A%22aff%22%7D"
            }

        list_of_teams_dict = []
        home_team_elems = []
        away_team_elems = []

        home_team_elems2 = [] # another list for the replaced names so every website gives out the same team names
        away_team_elems2 = [] # another list for the replaced names so every website gives out the same team names
        
        odds_elems = []

        self.driver.get(links)
        #time.sleep(12)

        r = requests.get(links,headers=headers)
        soppa = BeautifulSoup(r.content, "lxml")


        odds_elems0 = soppa.find_all("div", class_="preplay-bet-button")
        for odds in odds_elems0:
            odds_elems.append(odds.get("data-decimal-price"))

        home_team_elems0 = soppa.find_all("div", class_="competitor competitor-home")
        print(len(home_team_elems0), "the length")
        #print(home_team_elems0)

        for teams1 in home_team_elems0:    #these loops are for removing the blank spaces in the names
            #print(teams1.text)
            try:
                teams1 = teams1.text.replace("\n                        ","")
                teams1 = teams1.replace("                    ","")
                teams1 = teams1.replace("\n\n","")
                teams1 = teams1.replace("\n","")
                home_team_elems.append(teams1)
            except:
                home_team_elems.append(teams1)   #  adds the home teams into a list 

        away_team_elems0 = soppa.find_all("div", class_="competitor competitor-away")
        for teams1 in away_team_elems0:
            try:
                teams1 = teams1.text.replace("\n                        ","")
                teams1 = teams1.replace("                    ","")
                teams1 = teams1.replace("\n\n","")
                teams1 = teams1.replace("\n","")
                away_team_elems.append(teams1)
            except:
                away_team_elems.append(teams1)   #  adds the away teams into a list 

        #home_team_string = "//*[@class='competitor competitor-home']"
        #away_team_string = "//*[@class='competitor competitor-away']"
        #odd_string = "//*[@class='bb-sport-event__selection']"

        #home_team_elems = self.driver.find_elements(By.XPATH, home_team_string)
        #away_team_elems = self.driver.find_elements(By.XPATH, away_team_string)
        #odds_elems = self.driver.find_elements(By.XPATH, odd_string)

        print(home_team_elems)

        check_if_modified = 0
        check_if_modified1 = 0
        findName = 0
        for team in home_team_elems:    #loops which check if the team is in the list and replace the name
            check_if_modified = 0
            for names1 in self.names_dict["teams"]:
                if team in names1["names"]:
                    home_team_elems2.append(names1["replace_name"])
                    print("true")
                    check_if_modified = 1
                    
                    

            if check_if_modified == 0:   # if the name is not on the list, then it adds the original name into the list
                home_team_elems2.append(team)
            
        print(home_team_elems2)

        for team in away_team_elems:
            check_if_modified = 0
            for names1 in self.names_dict["teams"]:
                if team in names1["names"]:
                    away_team_elems2.append(names1["replace_name"])
                    print("true")
                    check_if_modified1 = 1

            if check_if_modified1 == 0:
                away_team_elems2.append(team)
        
        print(away_team_elems2)

        teams_dict2 = self.teams_dict.copy()
        
        y = 0

        yy = 0
        xx = 0

        print(home_team_elems2, "its home_team_elems2")

        for elem in home_team_elems2:
            teams_dict2["website"] = "888sport"
            teams_dict2["home_team"] = elem
            list_of_teams_dict.append(teams_dict2)
            teams_dict2 = self.teams_dict.copy()

        for elem2 in away_team_elems2:
            list_of_teams_dict[y]["away_team"] = elem2
            y += 1
            
        for elem3 in odds_elems:

            if yy == 0:
                list_of_teams_dict[xx]["home_odds"] = elem3

            if yy == 1:
                 list_of_teams_dict[xx]["draw_odds"] = elem3

            if yy == 2:
                list_of_teams_dict[xx]["away_odds"] = elem3
                yy = -1
                xx += 1

            yy += 1


        list_of_teams_dict2 = {"website":"888sport", "moneyline":list_of_teams_dict}
        #list_of_teams_dict2 = {"moneyline":list_of_teams_dict}


        return list_of_teams_dict2

    def get_the_marathonbet_odds(self,links):
        headers  = {
            "cookie":"panbet.openeventnameseparately=true; panbet.openadditionalmarketsseparately=false; puid=rBkp82Jyvw+wyWamAw8LAg==; LIVE_TRENDS_STYLE=ARROW; panbet.oddstype=Decimal; lang=en; SESSION_KEY=2f2962eaaea94615a102fe6f4783fca7",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        r = requests.get(links, headers=headers)
        print(r, "juuu")

        odds_list = []
        teams_list = []

        teams_list1 = []  #need another list because the first list is to replace the blank spaces, this one is for the dictionary

        list_of_teams_dict = []

        soppa = BeautifulSoup(r.content,"lxml")
        #teams = soppa.find_all(attrs={"data-member-link": True})
        teams = soppa.find_all("div", class_="member-name nowrap")

        for team in teams:
            team1 = team.text.replace("\n\n","")
            teams_list.append(team1)

        check_if_modified = 0  # this is for the team names
        for team2 in teams_list:
            for names1 in self.names_dict["teams"]:
                if team2 in names1["names"]:
                    teams_list1.append(names1["replace_name"])
                    check_if_modified = 1
                    print("true")

            if check_if_modified == 0:
                teams_list1.append(team2)

        

        odds = soppa.find_all(attrs={"data-selection-price": True})
        for odd in odds:
            odds_list.append(odd.text)


        y = 0
        xx = 0
        yy = 0
        teams_dict2 = self.teams_dict.copy()


        for team3 in teams_list1:  #the loop to insert the team names into the dictionaries
            teams_dict2["website"] = "marathonbet"
            
            if y == 0:
                teams_dict2["home_team"] = team3

            if y == 1:
                teams_dict2["away_team"] = team3
                list_of_teams_dict.append(teams_dict2)
                teams_dict2 = self.teams_dict.copy()
                y = -1

            y += 1

        print(len(list_of_teams_dict),"list_of_teams_dict length")
        print(len(odds_list), "odd_list length")


        for elem2 in odds_list:

            if yy == 0:
                list_of_teams_dict[xx]["home_odds"] = elem2

            if yy == 1:
                list_of_teams_dict[xx]["draw_odds"] = elem2

            if yy == 2:
                list_of_teams_dict[xx]["away_odds"] = elem2
                yy = -1
                xx += 1
            
            #print(list_of_teams_dict[xx])

            yy += 1


        list_of_teams_dict2 = {"website":"marathonbet", "moneyline":list_of_teams_dict}


        return list_of_teams_dict2



    def get_the_maxbet_odds(self,links):
        r = requests.get(links)

        print(r, "marathonbet reuquest")

        odds_list = []
        teams_list = []

        list_of_teams_dict = []

        soppa = BeautifulSoup(r.content,"lxml")
        odds = soppa.find_all("div", class_="OM-ValueChanger")

        teams = soppa.find_all("span", class_="Details__ParticipantName")

        z = 0

        for odd in odds:
            if z == 0 or z == 1 or z == 2:
                #print(odd.text, "joo")
                odds_list.append(odd.text)
            if z == 6:
                z= -1

            z += 1

        check_if_modified = 0

        for team in teams:
            check_if_modified = 0
            for names1 in self.names_dict["teams"]:     #makes a loop to check if the name is in the names list and to change it
                if team.text in names1["names"]:
                    teams_list.append(names1["replace_name"])
                    check_if_modified = 1
                    print("true")

            if check_if_modified == 0:   # if the name is not on the list, then it adds the original name into the list
                teams_list.append(team.text)
        
        
        print(teams_list)
                
            #print(team.text, "joo")

        teams_dict2 = self.teams_dict.copy()

        y = 0

        xx = 0
        yy = 0

        for team2 in teams_list:
            teams_dict2["website"] = "maxbet"
            if y == 0:
                teams_dict2["home_team"] = team2
                
            
            if y == 1:
                teams_dict2["away_team"] = team2
                list_of_teams_dict.append(teams_dict2)
                teams_dict2 = self.teams_dict.copy()
                y = -1

            y += 1

        #print(len(odds_list))


        for elem2 in odds_list:

            if yy == 0:
                list_of_teams_dict[xx]["home_odds"] = elem2

            if yy == 1:
                list_of_teams_dict[xx]["draw_odds"] = elem2

            if yy == 2:
                list_of_teams_dict[xx]["away_odds"] = elem2
                yy = -1
                xx += 1

            yy += 1

        list_of_teams_dict2 = {"website":"maxbet", "moneyline":list_of_teams_dict}
        #list_of_teams_dict2 = {"moneyline":list_of_teams_dict}

        return list_of_teams_dict2


    def get_the_marathonbet_odds2(self,links): #not modified yet, still has the maxbet code (there is the marathonbet code started before)
        r = requests.get(links)

        odds_list = []
        teams_list = []

        list_of_teams_dict = []

        soppa = BeautifulSoup(r.content,"lxml")
        odds = soppa.find_all("div", class_="OM-ValueChanger")

        teams = soppa.find_all("span", class_="Details__ParticipantName")

        z = 0

        for odd in odds:
            if z == 0 or z == 1 or z == 2:
                #print(odd.text, "joo")
                odds_list.append(odd.text)
            if z == 6:
                z= -1

            z += 1

        for team in teams:
            #print(team.text, "joo")
            if team.text == "Crystal Palace FC":
                team = "Crystal Palace"
                teams_list.append(team)

            if team.text == "Burnley FC":
                team = "Burnley"
                teams_list.append(team)
            
            if team.text == "Brighton and Hove Albion":
                team = "Brighton & Hove Albion"
                teams_list.append(team)

            if team.text == "Southampton FC":
                team = "Southampton"
                teams_list.append(team)

            if team.text == "Norwich City FC":
                team = "Norwich City"
                teams_list.append(team)

                
            if team.text == "West Ham United":
                team = "West Ham"
                teams_list.append(team)

            if team.text == "Watford FC":
                team = "Watford"
                teams_list.append(team)
            
            if team.text == "Newcastle United FC":
                team = "Newcastle United'"
                teams_list.append(team)

                
            #this is for the german teams
            if team.text == "Vfl Wolfsburg":
                team = "Wolfsburg"
                teams_list.append(team)

            if team.text == "1. FSV Mainz 051.":
                team = "Mainz"
                teams_list.append(team)
            
            if team.text == "TSG 1899 Hoffenheim":
                team = "Hoffenheim"
                teams_list.append(team)

            if team.text == "Bayer 04 leverkusen":
                team = "Bayer leverkusen"
                teams_list.append(team)

            if team.text == "1. Fc Koln":
                team = "Fc Köln"
                teams_list.append(team)

                
            if team.text == "SC Freiburg":
                team = "Freiburg"
                teams_list.append(team)

            if team.text == "1. FC Union Berlin":
                team = "Union Berlin"
                teams_list.append(team)
            
            if team.text == "FC Bayern Munich":
                team = "FC Bayern München"
                teams_list.append(team)

            if team.text == "Fc Augsburg":
                team = "Augsburg"
                teams_list.append(team)
            
            if team.text == "Hertha BSC":
                team = "Hertha BSC Berlin"
                teams_list.append(team)
            
            if team.text == "VfB Stuttgart":
                team = "Stuttgart"
                teams_list.append(team)

            else:
                teams_list.append(team.text)

        teams_dict2 = self.teams_dict.copy()

        y = 0

        xx = 0
        yy = 0

        for team2 in teams_list:
            if y == 0:
                teams_dict2["home_team"] = team2
                
            
            if y == 1:
                teams_dict2["away_team"] = team2
                list_of_teams_dict.append(teams_dict2)
                teams_dict2 = self.teams_dict.copy()
                y = -1

            y += 1

        #print(len(odds_list))


        for elem2 in odds_list:

            if yy == 0:
                list_of_teams_dict[xx]["home_odds"] = elem2

            if yy == 1:
                list_of_teams_dict[xx]["draw_odds"] = elem2

            if yy == 2:
                list_of_teams_dict[xx]["away_odds"] = elem2
                yy = -1
                xx += 1

            yy += 1

        list_of_teams_dict2 = {"website":"marathonbet", "moneyline":list_of_teams_dict}


        return list_of_teams_dict2

            

            


    
    def get_betfair_odds(self):
        self.driver.get("https://www.betfair.com/exchange/plus/")
        time.sleep(10)
        elem = self.driver.find_elements_by_class_name("runners")

        list_of_team_names = []
        list_of_teams_dict = []

        teams_dict = {
            "home_team":"",
            "away_team":"",
            "home_odds":"",
            "draw_odds":"",
            "away_odds":"",
        }
        for elems in elem:
            print(elems.text)
            names = elems.text.split("\n")
            list_of_team_names.append(names[0])
            list_of_team_names.append(names[1])
            print(list_of_team_names)

        y = 0
        for names in list_of_team_names:
            if y == 0:
                teams_dict["home_team"] = names
                y += 1
            if y == 1:
                if teams_dict["home_team"] == names:
                    pass
                else:
                    teams_dict["away_team"] = names
                    y += 1
            
            if y == 2:
                list_of_teams_dict.append(teams_dict)
                print(list_of_teams_dict)
                break





#elem = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/section/div[1]/div/div[1]/div/div/div[1]/a/span[2]")))#.get_attribute("value")



    
    




"""
y = 1
for x in range(10):
    for y in range(2):
        string = "//*[@id='main-wrapper'']/div/div[2]/div/ui-view/div/div/div/div/div[1]/div[3]/div/bf-sports-highlights-coupon/main/div/section/div[2]/bf-coupon-table[1]/div/table/tbody/tr["+str(x)+"]/td[1]/a/event-line/section/ul[1]/li["+str(y+1)+"]"
        elem = driver.find_elements_by_xpath(string)
        for elems in elem:
            print(elems.text)
        print(string)
"""










