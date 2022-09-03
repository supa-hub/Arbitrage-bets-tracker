from betting_tracker import tracker
import time


links_for_pinnacle = ["https://www.pinnacle.com/fi/soccer/germany-bundesliga/matchups#period:0", 
        "https://www.pinnacle.com/fi/soccer/england-premier-league/matchups#period:0", 
        "https://www.pinnacle.com/fi/soccer/italy-serie-a/matchups#period:0", 
        "https://www.pinnacle.com/soccer/uefa-nations-league-a/matchups/",
        "https://www.pinnacle.com/soccer/uefa-nations-league-b/matchups/",
        "https://www.pinnacle.com/soccer/uefa-nations-league-c/matchups/",
        "https://www.pinnacle.com/soccer/uefa-nations-league-d/matchups/"

        ]

links_for_betway = ["https://betway.com/en/sports/grp/soccer/england/premier-league",
        "https://betway.com/en/sports/grp/soccer/germany/bundesliga",
        "https://betway.com/en/sports/grp/soccer/international/uefa-nations-league"
]

links_for_888sport = ["https://spectate-web.888sport.com/spectate/football/coupon/english-premier-league",
        "https://www.888sport.com/fi/football/germany/bundesliga/",
        "https://spectate-web.888sport.com/spectate/football/events/europe/uefa-nations-league-a",
        "https://spectate-web.888sport.com/spectate/football/events/europe/uefa-nations-league-b"
        ]


links_for_maxbet = ["https://sports2.maxbet.ro/en/tournament-location/football/1/england/77/premier-league-2022-2023/172350176981209088/upcoming", 
        "https://sports2.maxbet.ro/en/tournament-location/football/1/germany/54/bundesliga/172350346522316800/upcoming",
        "https://sports2.maxbet.ro/en/tournament-location/football/1/europe/67/uefa-nations-league-2022-2023/168574061078695936/upcoming"
        ]

links_for_marathonbet = ["https://www.marathonbet.com/en/popular/Football/England/Premier+League+-+21520",
        "https://www.marathonbet.com/ind/betting/Football/Germany/Bundesliga+-+22436?menu=9607060",
        "https://www.marathonbet.com/en/betting/Football/Internationals/UEFA+Nations+League/League+A/Group+Stage+-+6402504",
        "https://www.marathonbet.com/en/betting/Football/Internationals/UEFA+Nations+League/League+B/Group+Stage+-+6402505",
        "https://www.marathonbet.com/en/betting/Football/Internationals/UEFA+Nations+League/League+C/Group+Stage+-+6402506",
        "https://www.marathonbet.com/en/betting/Football/Internationals/UEFA+Nations+League/League+D/Group+Stage+-+6402507",
        ]

list_of_all_teams = []

list_of_pinnacle_teams = []
list_of_betway_teams = []
list_of_888sport_teams = []
list_of_maxbet_teams = []

tracker = tracker()

def main():

    best_odds_dict = {
        "home_team":"",
        "away_team":"",
        "home_team_website": "",
        "draw_option_website": "",
        "away_team_website":"",
        "home_odds":"0",
        "draw_odds":"0",
        "away_odds":"0"
        }
       
    time.sleep(5)


    x = tracker.get_the_pinnacle_odds(links_for_pinnacle[0])
    list_of_all_teams.append(x)
    #list_of_pinnacle_teams.append(x)
    x = tracker.get_the_pinnacle_odds(links_for_pinnacle[1])
    list_of_all_teams.append(x)
    #list_of_pinnacle_teams.append(x)
    #x = tracker.get_the_pinnacle_odds(links_for_pinnacle[2])
    #list_of_all_teams.append(x)
    #list_of_pinnacle_teams.append(x)
    #x = tracker.get_the_pinnacle_odds(links_for_pinnacle[3])
    #list_of_all_teams.append(x)
    #x = tracker.get_the_pinnacle_odds(links_for_pinnacle[4])
    #list_of_all_teams.append(x)
    #x = tracker.get_the_pinnacle_odds(links_for_pinnacle[5])
    #list_of_all_teams.append(x)
    #x = tracker.get_the_pinnacle_odds(links_for_pinnacle[6])
    #list_of_all_teams.append(x)
    #list_of_pinnacle_teams.append(x)

    x = tracker.get_the_betway_odds(links_for_betway[0])
    list_of_all_teams.append(x)
    x = tracker.get_the_betway_odds(links_for_betway[1])
    list_of_all_teams.append(x)
    #list_of_betway_teams.append(x)

    x = tracker.get_the_888sport_odds(links_for_888sport[0])
    list_of_all_teams.append(x)
    x = tracker.get_the_888sport_odds(links_for_888sport[1])
    list_of_all_teams.append(x)
    #x = tracker.get_the_888sport_odds(links_for_888sport[2])
    #list_of_all_teams.append(x)
    #list_of_888sport_teams.append(x)

    x = tracker.get_the_maxbet_odds(links_for_maxbet[0])
    list_of_all_teams.append(x)
    x = tracker.get_the_maxbet_odds(links_for_maxbet[1])
    list_of_all_teams.append(x)
    #list_of_maxbet_teams.append(x)
    #x = tracker.get_the_maxbet_odds(links_for_maxbet[2])
    #list_of_all_teams.append(x)
    #list_of_maxbet_teams.append(x)

    x = tracker.get_the_marathonbet_odds(links_for_marathonbet[0])
    list_of_all_teams.append(x)
    x = tracker.get_the_marathonbet_odds(links_for_marathonbet[1])
    list_of_all_teams.append(x)
    #x = tracker.get_the_marathonbet_odds(links_for_marathonbet[2])
    #list_of_all_teams.append(x)
    #x = tracker.get_the_marathonbet_odds(links_for_marathonbet[3])
    #list_of_all_teams.append(x)
    #x = tracker.get_the_marathonbet_odds(links_for_marathonbet[3])
    #list_of_all_teams.append(x)


    print(list_of_all_teams)
    lists_len = 0


    #for lists in list_of_all_teams:
        #lists_len += len(lists["moneyline"])
    #print(lists_len)

    list_for_best_odds = []



    for list2 in list_of_all_teams:
        best_odds_dict2 = best_odds_dict.copy()
        for list3 in list_of_all_teams:
            if list2["website"] != list3["website"]:   #check if the website is different so it doesnt compare the bets in the same website

                for list4 in list2["moneyline"]:
                    for list5 in list3["moneyline"]:
                        if list4["home_team"] == list5["home_team"] and list4["away_team"] == list5["away_team"]:
                            best_odds_dict2["home_team"] = list4["home_team"]
                            best_odds_dict2["away_team"] = list4["away_team"]
                            try:
                                if float(list4["home_odds"]) >= float(list5["home_odds"]) and float(list4["home_odds"]) >= float(best_odds_dict2["home_odds"]):
                                    best_odds_dict2["home_team_website"] = list2["website"]
                                    best_odds_dict2["home_odds"] = list4["home_odds"]
                                
                                elif float(list4["home_odds"]) <= float(list5["home_odds"]) and float(list5["home_odds"]) >= float(best_odds_dict2["home_odds"]):
                                    best_odds_dict2["home_team_website"] = list3["website"]
                                    best_odds_dict2["home_odds"] = list5["home_odds"]

                                if float(list4["draw_odds"]) >= float(list5["draw_odds"]) and float(list4["draw_odds"]) >= float(best_odds_dict2["draw_odds"]):
                                    best_odds_dict2["draw_option_website"] = list2["website"]
                                    best_odds_dict2["draw_odds"] = list4["draw_odds"]

                                elif float(list4["draw_odds"]) <= float(list5["draw_odds"]) and float(list5["draw_odds"]) >= float(best_odds_dict2["draw_odds"]):
                                    best_odds_dict2["draw_option_website"] = list3["website"]
                                    best_odds_dict2["draw_odds"] = list5["draw_odds"]

                                if float(list4["away_odds"]) >= float(list5["away_odds"]) and float(list4["away_odds"]) >= float(best_odds_dict2["away_odds"]):
                                    best_odds_dict2["away_team_website"] = list2["website"]
                                    best_odds_dict2["away_odds"] = list4["away_odds"]

                                elif float(list4["away_odds"]) <= float(list5["away_odds"]) and float(list5["away_odds"]) >= float(best_odds_dict2["away_odds"]):
                                    best_odds_dict2["away_team_website"] = list3["website"]
                                    best_odds_dict2["away_odds"] = list5["away_odds"]
                            
                            except:
                                pass
                            
                            list_for_best_odds.append(best_odds_dict2)

                        best_odds_dict2 = best_odds_dict.copy()

    #print(list_for_best_odds)
    # 
    for list4 in list_for_best_odds:
        home_team = list4["home_team"]
        away_team = list4["away_team"]
        home_odd = float(list4["home_odds"])
        draw_odd = float(list4["draw_odds"])
        away_odd = float(list4["away_odds"])

        #print(list4)

        #if home_odd or draw_odd or away_odd == 0:
            #pass

        #else:
        try:
            arbitrage_num = 1/home_odd + 1/draw_odd + 1/away_odd
            print(arbitrage_num, "arbitrage num")
        except:
            pass
        

        #print(arbitrage_num)
        try:
            if arbitrage_num <= 1:
                print("Very nice!, the arbitrage num is: ", arbitrage_num)
                print("home: ", home_odd, "draw: ", draw_odd, "away: ",away_odd)
                print("the home team is: ", home_team)
                print("the away team is: ", away_team)
                print("the home team website is: ", list4["home_team_website"], ", the draw option website is: ", list4["draw_option_website"], ", the away team website is: ", list4["away_team_website"])
                print(" ")
                print(" ")
        
        except:
            pass
    






if __name__ == "__main__":
    main()