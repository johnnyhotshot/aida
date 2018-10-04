import requests, bs4, time
from selenium import webdriver

# Defining links
playerRosterLink = "http://fantasy.nfl.com/league/1179767/team/3?statCategory=projectedStats"
signInLink = "https://www.nfl.com/login?s=fantasy&returnTo=http%3A%2F%2Ffantasy.nfl.com%2F%3Ficampaign%3Dfty-nav-hp"

positions = [["QB"], ["RB"], ["RB"], ["WR"], ["WR"], ["TE"], ["WR", "RB"], ["BN"], ["BN"], ["BN"], ["BN"], ["BN"], ["BN"]]
field = [["QB"], ["RB"], ["RB"], ["WR"], ["WR"], ["TE"], ["RB", "WR"]]
teamSize = 13
playingSize = 7

soup = bs4.BeautifulSoup(requests.get(playerRosterLink).text, "html.parser")
roster = soup.findAll("table", {"class": "tableType-player"})[0]

"""
    Player Class
     # Attributes:
        name   = Player's name
        pos    = Player's position
        points = Player's projected points

"""
class Player():
    def __init__(self):
        self.name = "NULL"
        self.pos = "NULL"
        self.points = -1

    def __lt__(self, other):
        return self.points < other.points
    
    def __repr__(self):
        return "[" + self.name + "] : " + self.pos + " : " + str(self.points)
        

### --- Creating and Filling Player Object List --- ###

 # Create player object list and populate with empty players
players = []
for i in range(0,teamSize):
    players.append(Player())

 # Give names and positions to player object list
info = roster.findAll("td", {"class": "playerNameAndInfo"})
for i in range(0,teamSize):
    players[i].name = info[i].div.a.text
    players[i].pos = info[i].div.em.text[:2]

 # Give projected points to player object list
projectedPoints = roster.findAll("td", {"class": "projected"})
print(projectedPoints)
for i in range(0,teamSize):
    print(len(players))
    print(len(projectedPoints))
    players[i].points = float(projectedPoints[i].text)
    print(players[i])

### ----------------------------------------------- ###
###
### --- Detecting Lineup Optimizations --- ###

 # Creating list for future swaps, each item is an array of the index for each player in the swap (length of 2)
swaps = []

 # Find lowest scoring field player for each position along with highest scoring bench player, then
  # add to swap list if swap is beneficial and update roster array
for i in range(0,playingSize):
    lowestFieldPts = i
    for j in range(0,playingSize):
        if field[j] == field[i] and players[j].points < players[lowestFieldPts].points:
            lowestFieldPts = j
    highestBenchPts = -1
    for j in range(playingSize,teamSize):
        if players[j].pos in field[i] and (highestBenchPts == -1 or players[j].points > players[highestBenchPts].points):
            highestBenchPts = j
    if highestBenchPts != -1 and players[lowestFieldPts].points < players[highestBenchPts].points:
        swaps.append([lowestFieldPts, highestBenchPts])
        temp = players[lowestFieldPts]
        players[lowestFieldPts] = players[highestBenchPts]
        players[highestBenchPts] = temp


### -------------------------------------- ###
###
### --- Open Browser Window and Make Swaps --- ###

if len(swaps) > 0:
    browser = webdriver.Chrome("D://Python//Drivers//chromedriver_win32//chromedriver.exe")
    passwordFile = open("pass.txt") #It's in plaintext for now, will change in the future

    username = passwordFile.readline().strip()
    password = passwordFile.readline().strip()
    
    browser.get(signInLink)
    
    usernameField = browser.find_element_by_id("fanProfileEmailUsername")
    passwordField = browser.find_element_by_id("fanProfilePassword")
    signInButton = browser.find_element_by_tag_name("button")
        
    usernameField.sendKeys(username)
    passworldField.sendKeys(password)
    signInButton.click()

    print(browser.find_element_by_id("my_league_team"))
    
    browser.quit()

### ------------------------------------------ ###
