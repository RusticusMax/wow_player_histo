"""
Scrape Wow pvp ranking website and extreact class/spec by rank and plot a histo of it
"""
import sys  # contains stderr object for debug output
from lxml import html
import requests
import HistoData
import wow_strings as wow

# Changed remote:
# repo name: "git remote set-url origin 'https://RusticusMax@bitbucket.org/RusticusMax/wow_player_histo.git'"
# Variables
# Debug flag.  Set to non zero for debug
DEBUG_OUT = 1
# Number of blank pages (no data) to allow.  1 should really be sufficient
BLANK_PAGE_CNT = 5
# Index for counter bucket
CNTR = 0
# number of histogram bars (X of graph)
HISTO_BAR_COUNT = 25
# Number of players per bucket (max Y)
HISTO_HEIGHT = 20
# Only include data for the top n classes in histogram to reduce noise in graph
HISTO_TOP_X = 5
# So how many players do we need to process
PLAYER_MAX = HISTO_BAR_COUNT * HISTO_HEIGHT
# Module level variable are always treated as constants, tell pylint to ignore const case requirement for the following
# pylint: disable=C0103
# create an array of dictionaries for histogram data
# copy each (so we don't end up with an array of references) class_dict dictionary for each histo bar
player_current = 0  # init current player counter so we will know when to stop
page_count = 1  # So we can request the right page of data from web site, since we have to do it a page at a time.
# pylint: enable=C0103

# Build dictionary of counters
class_dict = {name: HistoData.HistoData(HISTO_BAR_COUNT) for name in wow.wow_class_spec_names}

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
    # Strip leading spaces
    player_class = [x.strip() for x in tree.xpath('//div[@class="Character-level"]/text()')]

    # did we get data?  If not skip. But track number of fails and exit if reached limit (BLANK_PAGE_CNT)
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
                    print("Unicode Error on print", e.args)
                    sys.exit(2)
            class_dict[i_player_class].inc_cnt()
            # inc appropriate histogram bucket
            class_dict[i_player_class].inc_bucket(int((player_current - 1) / HISTO_HEIGHT))
    page_count += 1

if DEBUG_OUT:
    print("player count", player_current)

# Sort by class counts and print highest to lowest (excluding zero counts)
for class_item in sorted(class_dict.keys(), key=lambda class_str: class_dict[class_str].cnt(), reverse=True):
    print(class_dict[class_item].cnt(), ",", class_item)
    if class_dict[class_item].cnt() < 1:   # Don't bother to output class/spec with zero counts
        break

# Dump histogram data
# creat list of top n classes,  We use it in the loop
histo_top_classes = []
for class_item in sorted(class_dict.keys(), key=lambda class_str: class_dict[class_str].cnt(), reverse=True):
    histo_top_classes.append(class_item)
    if len(histo_top_classes) >= HISTO_TOP_X:
        break

# Output header
print("Rank", ',', end='')
for class_item in histo_top_classes:
    print(class_item, ',', end='')
print()  # And a newline to end

for i in range(HISTO_BAR_COUNT):
    # Print left legend for bucket ranges (e.g. 0-20, 21-40, etc)
    print((i * HISTO_HEIGHT) + 1, " ", (i + 1) * HISTO_HEIGHT, ',', end='')
    # Print counts for this tier for top overall classes
    for histo_item in histo_top_classes:
        print(class_dict[histo_item].bucket(i), ',', end='')
    print()  # end of line
