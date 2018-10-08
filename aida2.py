import requests, bs4, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Defining links
playerRosterLink = "http://fantasy.nfl.com/league/1179767/team/3?statCategory=projectedStats"
playerRosterLinkChange = "http://fantasy.nfl.com/league/1179767/team/3"
signInLink = "https://www.nfl.com/login?s=fantasy&returnTo=http%3A%2F%2Ffantasy.nfl.com%2F%3Ficampaign%3Dfty-nav-hp"
freeAgentsLink = "http://fantasy.nfl.com/league/1179767/players?playerStatus=available&position=O&statCategory=projectedStats"

# Global Constant Variables
positions = [["QB"], ["RB"], ["RB"], ["WR"], ["WR"], ["TE"], ["WR", "RB"], ["BN"], ["BN"], ["BN"], ["BN"], ["BN"], ["BN"]]
field = [["QB"], ["RB"], ["RB"], ["WR"], ["WR"], ["TE"], ["RB", "WR"]]
teamSize = 13
playingSize = 7
agentsToCheck = 25 # Max 25, add multipage support to remove limit


# Create webdriver and options objects to open headless browser with
options = Options()
options.add_argument("--headless")
browser = webdriver.Chrome("chromedriver.exe", chrome_options=options)
browser.set_window_size(1000, 1000)

# Create BeautifulSoup object to read webpages
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
for i in range(0,teamSize):
    players[i].points = float(projectedPoints[i].text)

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
    # Open password file
    passwordFile = open("pass.txt") # Yeah it's in plaintext for now, will change in the future - don't try this at home kids

    # Get username and password
    username = passwordFile.readline().strip()
    password = passwordFile.readline().strip()

    # Open sign-in page
    browser.get(signInLink)

    # Find login fields and sign-in button
    usernameField = browser.find_element_by_id("fanProfileEmailUsername")
    passwordField = browser.find_element_by_id("fanProfilePassword")
    signInButton = browser.find_element_by_xpath("//*[@id='content']/div/div/div[2]/div[1]/div/div[3]/div[2]/main/div/div[2]/div[2]/form/div[3]/button")

    # Fill in username and password and click sign-in button, then navigate to roster page
    usernameField.send_keys(username)
    passwordField.send_keys(password)
    signInButton.click()
    time.sleep(3)
    browser.find_element_by_link_text("TEAM").click()

    # Create list of drag buttons, sort out usable ones, click them in swap order
    dragButtons = browser.find_elements_by_class_name("teamPositionEditDrag")
    playerSelectors = []
    submitButton = browser.find_element_by_class_name("submit")
    
    for button in dragButtons:
        if button.tag_name == "td":
            playerSelectors.append(button)

    for swap in swaps:
        playerSelectors[swap[0]].click()
        playerSelectors[swap[1]].click()
        
    submitButton.click()
    
    browser.quit()


### ------------------------------------------ ###
###
### --- Check Free Agents for Better Players --- ###


 # DON'T FORGET ABOUT PLAYERS WITH BYE

soup = bs4.BeautifulSoup(requests.get(freeAgentsLink).text, "html.parser")
agents = soup.findAll("table", {"class": "tableType-player"})[0].tbody.findAll("tr")

freeAgents = []
for i in range(0,len(agents)):
    freeAgents.append(Player())
    playerInfo = agents[i].findAll("td", {"class": "playerNameAndInfo"})[0].div
    freeAgents[i].name = playerInfo.a.text
    freeAgents[i].pos = playerInfo.em.text[:2]
    freeAgents[i].points = agents[i].findAll("td", {"class": "projected"})[0].span.text
    


### -------------------------------------------- ###
###
### --- Open Browser Window and Get Free Agents --- ###



### ----------------------------------------------- ###

browser.quit()
