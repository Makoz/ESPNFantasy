import mechanicalsoup
import argparse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from playerinfo import PlayerInfo
import re
from pprint import pprint

def findteamid(href):
  idx = href.find("teamId=")
  substr = href[idx:]
  ambersand = substr.find("&")
  equal = substr.find("=")
  return (substr[equal+1:ambersand])


parser = argparse.ArgumentParser(description='Login to ESPN Fantasy')
parser.add_argument("username")
parser.add_argument("password")
args = parser.parse_args()

driver = webdriver.Firefox();
driver.get("http://games.espn.go.com/fba/clubhouse?leagueId=27744&teamId=5&seasonId=2016")

WebDriverWait(driver,1000).until(EC.presence_of_all_elements_located((By.XPATH,"(//iframe)")))
frms = driver.find_elements_by_xpath("(//iframe)")
driver.switch_to_frame(frms[2])

#print(driver.page_source)
#password = driver.find_elements_by_xpath("//form[@class='ng-pristine ng-valid ng-valid-pattern ng-valid-required']/section/div/div/label/input[")
password = driver.find_elements_by_xpath("//*[@id='did-ui']/div/div/section/section/form/section/div[2]/div/label/input")
password = password[0]


username = driver.find_elements_by_xpath("//form[@class='ng-pristine ng-valid ng-valid-pattern ng-valid-required']/section/div/div/label/input")
username = username[0]
username.send_keys(args.username)
password.send_keys(args.password)                                                                                  

enter = driver.find_elements_by_xpath("//*[@id='did-ui']/div/div/section/section/form/section/div[3]/button")
enterBtn = enter[0]
enterBtn.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "playerTableFramedForm")))

gameTabs = driver.find_elements_by_xpath("//ul[@id='games-tabs']/*")

scoreBoard = gameTabs[4]
scoreBoard.click()
#WebDriverWait(driver,1000).until(EC.presence_of_all_elements_located((By.XPATH,"(//tr)")))

#scoreBoardMatchups = driver.find_element_by_id('scoreboardMatchups')
#scoreTable = driver.find_element_by_class_name('tableBody')

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

#Get cats of matchups, all cats are same 

tableSubHead = soup.find_all('tr', class_='tableSubHead')
tableSubHead = tableSubHead[0]

listCats = tableSubHead.find_all('th')
catFullName = []
catShortName = []

for cat in listCats:
    if 'title' in cat.attrs:
        catFullName.append(cat['title'])
        catShortName.append(cat.string)

# Get MU stats

players = []

for tag in soup.find_all('tr' , class_='linescoreTeamRow'):
  teamIdHRef = str(tag.a['href'])
  teamId = findteamid(teamIdHRef)
  stats = []
  s = tag.find_all(True, {'class':['precise winning', 'precise']})
  player = PlayerInfo(teamId)
  for i in range(0,len(catFullName)):
    setattr(player, catFullName[i], s[i].text)
  
  players.append(player)

#Find players team 
for i in range(len(players)):
  teamLinks = driver.find_elements_by_xpath('//*[@id="scoreboardMatchups"]/div/table/tbody/tr/td[@class="teamName"]/a')
  link = teamLinks[i]
  link.click()

  html = driver.page_source
  soup = BeautifulSoup(html, 'html.parser')

  teamPlayers = soup.findAll('td', id=re.compile('^playername_'))
 
  for s in teamPlayers:
    l = s.get_text()
    l = l.replace(u'\xa0', u' ')
    players[i].addPlayer(l)

  pprint (vars(players[i]))
  driver.back()

#  players[0].add_player(s.get_text())
# driver.back()

# # teamLinks = driver.find_elements_by_xpath('//*[@id="scoreboardMatchups"]/div/table/tbody/tr/td[@class="teamName"]/a')

# link = teamLinks[1]
# link.click()

# pprint (vars(players[0]))
# #print(teamLinks
# print(teamLinks)
# print(len(teamLinks))
'''
  print(s[0].text)
  print(len(s))
  #for s in tag.a:
  #  print(s)
#  print (tag.text)
#  print("\n")
  print (tag)
  print("\n")


for p in players:
  for k in catFullName:
    print(k + " ||| " + str(getattr(p,k)))
  print("id ||| " + str(getattr(p, "Id")))

'''
driver.close()


