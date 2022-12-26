##
## Class to support extracting player data from URL or name/realm combination.
##

from lxml import html
import requests
import sys  # contains stderr object for debug output

class Player:
    def __init__(self, URL):
        p_page = requests.get(URL)  # slurp page from internet
        print(p_page.status_code, len(p_page.content))
        print("find", p_page.content.find('Drblank'.encode('ascii')))
        print("name: ", p_page.content[35:54])
        p_tree = html.fromstring(p_page.content)

        ## roles = tree.xpath('//div[@class="Character-role"]/span')
        p_name = p_tree.xpath('//div[@class="CharacterHeader-nameTitle"]')
        p_spec = p_tree.xpath('//*[@class="CharacterHeader-detail"]/span[3]')
        print(len(p_name), len(p_spec))
        pass