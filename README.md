Purpose:

Three separate apps for processing Blizzard player data.  Really needs to be rewritten to use Blizzard APIs where possible

pvp_player_histo.py
- Status: (scraping web) Working
- Purpose: Create a CSV ready list of top pvp players/  Useful for determining which specs are the most popular.
- TO DO:
1) Embed plotting (interactive) directly in app

MP_players.py
- Status: (scraping web) Extracts, but just prints a list.  Also being used as a test jig for player module.
- Purpose: Determine top class/spec for the various M+ dungeon roles.
- TO DO:
1) determine specs (NOT IN M+ data)  Only really important for DPS (tank and healer (except for priest) are obvious.

Player.py
- Status: (scraping web) Only the barest of extraction.  Needs to be rewritten with API, scraping is not optimal for this.
- Purpose: A helper class that provides player detail to applications.
A Class that given a URL or name/realm, will extract all data on a single player, including spec details.
- TO DO: Everything!
