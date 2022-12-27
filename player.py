##
## Class to support extracting player data from URL or name/realm combination.
##

from lxml import html
import requests
import sys  # contains stderr object for debug output

class Player:
    def __init__(self, URL):
        p_page = requests.get(URL)  # slurp page from internet
        print(p_page.status_code, len(p_page.content)) # Need reliable check for successful page slurp
        p_tree = html.fromstring(p_page.content)

        ## Page is just scripts to build page

        p_title = p_tree.xpath('//meta[@name="description"]')
        p_name = p_tree.xpath('//*[@id="character-profile-mount"]/div/div/div[2]/div/div[1]/div[1]/div/div[1]/div[2]/div/a')
        p_spec = p_tree.xpath('//*[@class="CharacterHeader-detail"]/span[3]')
        print(len(p_name), len(p_spec), len(p_title))
        pass