"""
I want to develop a Linkedin_Bot🤖 to scrape Linkedin platform
and if the user had mutual interests with me in experience or
educations send a invitation with customized message and finally
save the scraped data in a CSV format.
"""

import requests, time, random
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from random import randint
from selenium.webdriver.chrome.options import Options

# Extracting username and password.
file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]

# Path to chromedriver.
path_to_chromedriver = '/Users/arian/WorkSpace/dev/scraper/drivers/chromedriver'
Linkedin_Login_Page = 'https://www.linkedin.com/uas/login'


profilesQueued = []
visited_profiles = []


class Linkedin_Bot():

    def __init__(self, csvpath='/Users/arian/Desktop'):
        """
        By creating an instance of this class a chromedriver
        with following options will be started.
        """
        # Creating a headless browser
        opts = Options()
        #opts.headless = True
        self.browser = Chrome(executable_path=path_to_chromedriver) # , options=opts
        # Getting to login page
        self.browser.get(Linkedin_Login_Page)



    def login(self):
        """
        Logging into admins users profile in the
        platform to have permission to explore the website.
        """
        # Xpath to username input.
        xp_username = '//*[@id="username"]'
        # Xpath to password input.
        xp_password = '//*[@id="password"]'
        # Simulating human.
        time.sleep(randint(2, 3))
        # Sending username.
        username_input = self.browser.find_element_by_xpath(xp_username)
        username_input.send_keys(username)
        # Simulating human.
        time.sleep(randint(2, 3))
        # Sending password.
        password_input = self.browser.find_element_by_xpath(xp_password)
        password_input.send_keys(password)
        # Xpath to submit button.
        # Simulating human.
        time.sleep(randint(5, 8))
        xp_submit = '//*[@id="app__container"]/main/div[2]/form[@class="login__form"]/div[@class="login__form_action_container "]/button'
        # Submiting (Clicking on button)
        submit_button = self.browser.find_element_by_xpath(xp_submit)
        submit_button.click()




    def soup_maker(self):
        """
        Makes a soup object of current page in the browser.
        """
        soup = BeautifulSoup(self.browser.page_source)
        return soup




    def getNewProfilesIDs(self, soup, profilesQueued):
        """
        Gets new user IDs and returning list containing IDs
        """
        profilesID = []
        pav = soup.find('section', {'class': 'pv-profile-section pv-browsemap-section profile-section artdeco-container-card ember-view'})
        all_links = pav.findAll('a', {'class', 'pv-browsemap-section__member ember-view'})
        for link in all_links:
            user_id = link.get('href')
            if ((user_id not in visited_profiles) and (user_id not in profilesQueued)):
                profilesID.append(user_id)

        return profilesID



    #def profile_

bot = Linkedin_Bot()
time.sleep(5)

bot.login()
time.sleep(random.randint(3, 5))
