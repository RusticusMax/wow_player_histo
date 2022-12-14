##
## Class to support extracting player data from URL or name/realm combination.
##

from lxml import html
import requests
import sys  # contains stderr object for debug output
import time

# pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# pip install python-blizzardapi


class Player:
    def __init__(self, URL):
        op = webdriver.ChromeOptions()
        op.add_argument('--headless')
        driver = webdriver.Chrome('C:\\Program Files (x86)\\Goggle-ChromeDriver\\chromedriver.exe', options=op)
        driver.get(URL)
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "character-profile-mount")))
        # time.sleep(1)
        p_name = driver.find_element_by_xpath('//*[@id="character-profile-mount"]/div/div/div[2]/div/div[1]/div[1]/div/div[1]/div[2]/div/a')
        p_title = driver.find_element_by_xpath('//meta[@name="description"]')
        p_spec = driver.find_element_by_xpath('//*[@class="CharacterHeader-detail"]/span[3]')
        p_ivl = driver.find_element_by_xpath('//*[@id="character-profile-mount"]/div/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/a[2]/div/div[2]')

        pass

        #p_page = requests.get(URL)  # slurp page from internet
        #print(p_page.status_code, len(p_page.content)) # Need reliable check for successful page slurp
        #p_tree = html.fromstring(p_page.content)

        ## Page is just scripts to build page

        #p_title = p_tree.xpath('//meta[@name="description"]')
        #p_name = p_tree.xpath('//*[@id="character-profile-mount"]/div/div/div[2]/div/div[1]/div[1]/div/div[1]/div[2]/div/a')
        #p_spec = p_tree.xpath('//*[@class="CharacterHeader-detail"]/span[3]')
        print(p_name.text, p_spec.text, len(p_title.text), p_ivl.text)
