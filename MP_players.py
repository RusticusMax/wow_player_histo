##
## Read Mythic Keystone leader board and spit out useful stats
##
## Significant difference from pvp:
## 1) You have to select server and Dungeon
## 2) There is only one page and (always) 100 entries
## 3) A player can show up mlutiple times, potentially in different roles
## 4) re#3 this is per run, not perseason

#todo: Expand sample HTML file to include entire team (row) HTML block
#todo: Find why to select team block (row) and select inside of that.
#todo: Find a reliable way to extract roles
#todo: Work on class to extract character data from url, or name+realm

from lxml import html
import requests
import sys  # contains stderr object for debug output
import player


# Changed remote repo name: "git remote set-url origin 'https://RusticusMax@bitbucket.org/RusticusMax/wow_player_histo.git'"
# Variables
# Debug flag.  Set to non zero for debug
DEBUG_OUT=1
# Number of players to process
TEAM_MAX=100

# Dictionary for counting classes
class_list = { " Windwalker Monk":0,        " Holy Paladin":0,          " Frost Death Knight":0,
               " Restoration Druid":0,      " Survival Hunter":0,       " Frost Mage":0,
               " Restoration Shaman":0,     " Retribution Paladin":0,   " Shadow Priest":0,
               " Arms Warrior":0,           " Elemental Shaman":0,      " Feral Druid":0,
               " Balance Druid":0,          " Destruction Warlock":0,   " Affliction Warlock":0,
               " Subtlety Rogue":0,         " Mistweaver Monk":0,       " Unholy Death Knight":0,
               " Assassination Rogue":0,    " Protection Paladin":0,    " Discipline Priest":0,
               " Enhancement Shaman":0,     " Arcane Mage":0,           " Demonology Warlock":0,
               " Guardian Druid":0,         " Havoc Demon Hunter":0,    " Fire Mage":0,
               " Marksmanship Hunter":0,    " Holy Priest":0,           " Outlaw Rogue":0,
               " Beast Mastery Hunter":0,   " Protection Warrior":0,    " Blood Death Knight":0,
               " Vengeance Demon Hunter":0, " Fury Warrior":0,          " Brewmaster Monk":0,
               " Preservation Evoker":0,    " Devastation Evoker":0,
               }

def extract_role(class_str):
    x = class_str[26:].find(' ')
    return "(" + class_str[26:x+26] + ")"

page = requests.get(
    'https://worldofwarcraft.com/en-us/game/pve/leaderboards/gorefiend/algethar-academy')  # slurp page from internet
tree = html.fromstring(page.content)

#players = tree.xpath('//use[@xlink]')
#roles = tree.xpath('//use') # Get URL of role Icon (count is less than players???)
roles = tree.xpath('//div[@class="Character-role"]/span')
players = tree.xpath('//div[@class="Character-name"]/text()')
realms = tree.xpath('//div[@class="Character-realm"]/text()')
teams = tree.xpath('//div[@class="SortTable-row"]')
tanks = tree.xpath('//*[@id="main"]/div[5]/div[2]/div/div[2]/div/div/div/div[2]/div[*]/div[4]/div/div[*]/a')

print("players, roles, teams")
print(len(players), len(roles), len(teams), len(tanks))
for i in range(0, len(tanks)):
    # print(tanks[i].attrib['class'])
    print(extract_role(tanks[i].attrib['class']))
    # print("((", roles[i].attrib['class'], "))")

test_player = player.Player('https://worldofwarcraft.com/en-us/character/us/bleeding-hollow/drblank')
# print("((", roles[54].attrib['xlink:href'], "))")
# print(players[0])
#
# print("((", roles[55].attrib['xlink:href'], "))")
# print(players[1])

# print("------- All players by team (hopefully)-------")
# for i in range(0, 500, 5):
#     print("")
#     for j in range(0, 5):
#         print(players[i+j], realms[i+j], " -- ", end='')

