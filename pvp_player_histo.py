"""
Scrape Wow pvp ranking website and extreact class/spec by rank and plot a histo of it
"""
import sys  # contains stderr object for debug output
from lxml import html
import requests


# Changed remote:
# repo name: "git remote set-url origin 'https://RusticusMax@bitbucket.org/RusticusMax/wow_player_histo.git'"
# Variables
# Debug flag.  Set to non zero for debug
DEBUG_OUT = 1
# Number of blank pages (no data) to allow.  1 should really be sufficient
BLANK_PAGE_CNT = 5
# number of histogram bars (X of graph)
HISTO_BAR_COUNT = 25
# Number of players per bucket (max Y)
HISTO_HEIGHT = 20
# Only include data for the top n classes in histogram to reduce noise in graph
HISTO_TOP_X = 5

# So how many players do we need to process
PLAYER_MAX = HISTO_BAR_COUNT * HISTO_HEIGHT

# Dictionary for counting classes
class_list = {'Windwalker Monk': 0,        'Holy Paladin': 0,          'Frost Death Knight': 0,
              'Restoration Druid': 0,      'Survival Hunter': 0,       'Frost Mage': 0,
              'Restoration Shaman': 0,     'Retribution Paladin': 0,   'Shadow Priest': 0,
              'Arms Warrior': 0,           'Elemental Shaman': 0,      'Feral Druid': 0,
              'Balance Druid': 0,          'Destruction Warlock': 0,   'Affliction Warlock': 0,
              'Subtlety Rogue': 0,         'Mistweaver Monk': 0,       'Unholy Death Knight': 0,
              'Assassination Rogue': 0,    'Protection Paladin': 0,    'Discipline Priest': 0,
              'Enhancement Shaman': 0,     'Arcane Mage': 0,           'Demonology Warlock': 0,
              'Guardian Druid': 0,         'Havoc Demon Hunter': 0,    'Fire Mage': 0,
              'Marksmanship Hunter': 0,    'Holy Priest': 0,           'Outlaw Rogue': 0,
              'Beast Mastery Hunter': 0,   'Protection Warrior': 0,    'Blood Death Knight': 0,
              'Vengeance Demon Hunter': 0, 'Fury Warrior': 0,          'Brewmaster Monk': 0,
              'Preservation Evoker': 0,    'Devastation Evoker': 0,
              }

# Buckets for counting
H = HISTO_BAR_COUNT
histo_dict = {'Windwalker Monk': [0] * H,          'Holy Paladin': [0] * H,        'Frost Death Knight': [0] * H,
              'Restoration Druid': [0] * H,        'Survival Hunter': [0] * H,     'Frost Mage': [0] * H,
              'Restoration Shaman': [0] * H,       'Retribution Paladin': [0] * H, 'Shadow Priest': [0] * H,
              'Arms Warrior': [0] * H,             'Elemental Shaman': [0] * H,    'Feral Druid': [0] * H,
              'Balance Druid': [0] * H,            'Destruction Warlock': [0] * H, 'Affliction Warlock': [0] * H,
              'Subtlety Rogue': [0] * H,           'Mistweaver Monk': [0] * H,     'Unholy Death Knight': [0] * H,
              'Assassination Rogue': [0] * H,      'Protection Paladin': [0] * H,  'Discipline Priest': [0] * H,
              'Enhancement Shaman': [0] * H,       'Arcane Mage': [0] * H,         'Demonology Warlock': [0] * H,
              'Guardian Druid': [0] * H,           'Havoc Demon Hunter': [0] * H,  'Fire Mage': [0] * H,
              'Marksmanship Hunter': [0] * H,      'Holy Priest': [0] * H,         'Outlaw Rogue': [0] * H,
              'Beast Mastery Hunter': [0] * H,     'Protection Warrior': [0] * H,  'Blood Death Knight': [0] * H,
              'Vengeance Demon Hunter': [0] * H,   'Fury Warrior': [0] * H,        'Brewmaster Monk': [0] * H,
              'Preservation Evoker': [0] * H,      'Devastation Evoker': [0] * H,
              }

# Module level variable are always treated as constants, tell pylint to ignore const case requirement for the following
# pylint: disable=C0103
# create an array of dictionaries for histogram data
# copy each (so we don't end up with an array of references) class_list dictionary for each histo bar
player_current = 0  # init current player counter so we will know when to stop
page_count = 1  # So we can request the right page of data from web site, since we have to do it a page at a time.
# pylint: enable=C0103

# Read in a page and loop through all entries on the page and update counts
while player_current < PLAYER_MAX:
    # slurp page from internet
    page = requests.get('https://worldofwarcraft.com/en-us/game/pvp/leaderboards/3v3?page=' + str(page_count), timeout=5)
    if page.status_code >= 300:
        print("Error: page returned ", page.status_code, " exiting!")
        sys.exit(1)
    tree = html.fromstring(page.content)

    # extract player name, realm and charater class (stored in level field)
    players = tree.xpath('//div[@class="Character-name"]/text()')
    realms = tree.xpath('//div[@class="Character-realm"]/text()')
    # How does this  extract the actual name, and not also the level number?
    player_class = [x.strip() for x in tree.xpath('//div[@class="Character-level"]/text()')]

    # did we get data?  If not skip. But track number of fail and exit if reached limit (BLANK_PAGE_CNT)
    if len(players) == 0:
        # if we reached the allowed blank page count exit with error
        if BLANK_PAGE_CNT <= 0:
            print("BLANK_PAGE_CNT reached limit.  Exiting")
            sys.exit(1)
        else:
            BLANK_PAGE_CNT -= 1
        break
    # for each element of data on this page process it.
    for i, (i_player, i_player_class, i_realm) in enumerate(zip(players, player_class, realms)):
        if player_current < PLAYER_MAX:
            player_current += 1
            # Clean up realm names for URL (need to deal with unicode(?) and special characters
            safe_realm = i_realm.replace("'", "")
            safe_realm = safe_realm.replace(" ", "")

            # Printing unicode chars can cause exception on console
            if DEBUG_OUT:
                try:
                    print(player_current, players[i], safe_realm, '[' + i_player_class + ']', file=sys.stderr)
                except UnicodeError as e:
                    print()
                    print("Unicode Error on print")
                    sys.exit(2)
                except Exception as e:
                    print("Exception on print", e.args)
                    oops = e
            class_list[i_player_class] += 1
            # inc appropriate histogram bucket
#            histo_buckets[int((player_current - 1) / HISTO_HEIGHT)][i_player_class] += 1
            histo_dict[i_player_class][int((player_current - 1) / HISTO_HEIGHT)] += 1

    page_count += 1

if DEBUG_OUT:
    print("player count", player_current)

# Sort by class counts and print highest to lowest (excluding zero counts)
for class_item in sorted(class_list.keys(), key=lambda class_str: class_list[class_str], reverse=True):
    print(class_list[class_item], ",", class_item)
    if class_list[class_item] < 1:   # Don't bother to output class/spec with zero counts
        break

# Dump histogram data
# creat list of top n classes,  We use it in the loop
histo_top_classes = []
for class_item in sorted(class_list.keys(), key=lambda class_str: class_list[class_str], reverse=True):
    histo_top_classes.append(class_item)
    if len(histo_top_classes) >= HISTO_TOP_X:
        break

# Output header
print("Rank", ',', end='')
for class_item in histo_top_classes:
    print(class_item, ',', end='')
print()  # And a newline to end

# Print actual histogram data
# for each dictionary in the array process that batch of counts
# for i, histo_bar in enumerate(histo_buckets):
#     # Print left legend for bucket ranges (e.g. 0-20, 21-40, etc)
#     print((i * HISTO_HEIGHT) + 1, " ", (i + 1) * HISTO_HEIGHT, ',', end='')
#     for histo_item in histo_top_classes:
#         print(histo_bar[histo_item],  ',', end='')
#     print()     # end of line
#
# print("----------------------------------------")

for i in range(HISTO_BAR_COUNT):
    # Print left legend for bucket ranges (e.g. 0-20, 21-40, etc)
    print((i * HISTO_HEIGHT) + 1, " ", (i + 1) * HISTO_HEIGHT, ',', end='')
    for histo_item in histo_top_classes:
        print(histo_dict[histo_item][i], ',', end='')
    print()  # end of line