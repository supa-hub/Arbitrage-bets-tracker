from betting_tracker import tracker
import csv


links_for_pinnacle = ["https://www.pinnacle.com/fi/soccer/germany-bundesliga/matchups#period:0", 
        "https://www.pinnacle.com/fi/soccer/england-premier-league/matchups#period:0", 
        "https://www.pinnacle.com/fi/soccer/italy-serie-a/matchups#period:0", 
        "https://www.pinnacle.com/fi/soccer/spain-la-liga/matchups#period:0"
        ]

links_for_betway = ["https://betway.com/en/sports/grp/soccer/england/premier-league",
]

links_for_888sport = ["https://spectate-web.888sport.com/spectate/football/coupon/english-premier-league"]


links_for_maxbet = ["https://sports2.maxbet.ro/en/tournament-location/football/1/england/77/premier-league-2021-2022/140821631034511360/upcoming?currentSession=Anonymousdfc1406e-a72a-4895-82fd-73bedd1c6d73&basePath=https%3A%2F%2Fwww.maxbet.ro%2Fen%2Fonline-betting", 
        "https://sports2.maxbet.ro/en/tournament-location/football/1/germany/54/bundesliga-2021-2022/142087356010254336/upcoming",
        "https://sports2.maxbet.ro/en/tournament-location/football/1/italy/111/serie-a-2021-2022/143620648089997312/upcoming"
        ]

links_for_marathonbet = ["https://www.marathonbet.com/en/popular/Football/England/Premier+League+-+21520"]

list_of_all_teams = []
#x = tracker.get_the_pinnacle_odds(links_for_pinnacle[0])
#list_of_all_teams.append(x)
#x = tracker.get_the_pinnacle_odds(links_for_pinnacle[2])
#list_of_all_teams.append(x)
x = tracker.get_the_pinnacle_odds(links_for_pinnacle[1])
list_of_all_teams.append(x)
x = tracker.get_the_betway_odds(links_for_betway[0])
list_of_all_teams.append(x)
x = tracker.get_the_888sport_odds(links_for_888sport[0])
list_of_all_teams.append(x)
x = tracker.get_the_maxbet_odds(links_for_maxbet[0])
list_of_all_teams.append(x)
#x = tracker.get_the_maxbet_odds(links_for_maxbet[1])
#list_of_all_teams.append(x)

headers = ["website","home_team","away_team","home_odds","draw_odds","away_odds"]
with open("names.csv", "w") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for lists in list_of_all_teams:
        writer.writerows(lists)
    
