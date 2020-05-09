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




    def go_to_admin(self):
        """
        This method navigates to admin_user's profile to
        be able to extract the list of suggested users.
        """
        # ID we are going to visit.
        visitingProfileID = '/in/arian-aghnaei-6633471a0/'
        # Constructing link
        fullLink = 'https://www.linkedin.com' + visitingProfileID
        # Directing to profile page using ID
        self.browser.get(fullLink)
        # driver.maximize_window()




    def getNewProfilesIDs(self, profilesQueued):
        """
        Gets new user IDs and returning list containing IDs
        """
        profilesID = []
        soup = BeautifulSoup(self.browser.page_source, 'lxml')
        pav = soup.find('section', {'class': 'pv-profile-section pv-browsemap-section profile-section artdeco-container-card ember-view'})
        all_links = pav.findAll('a', {'class', 'pv-browsemap-section__member ember-view'})
        for link in all_links:
            user_id = link.get('href')
            if ((user_id not in visited_profiles) and (user_id not in profilesQueued)):
                profilesID.append(user_id)

        return profilesID



    def scroll_page(self):
        """
        Using this method the BOT can scroll the page.
        """

        SCROLL_PAUSE_TIME = 5

        # Get scroll height
        last_height = self.browser.execute_script("return document.body.scrollHeight")

        for i in range(3):
            # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height



    def visit_profile(self, profilesQueued):
        """
        This method is going to visit the extracted user's profiles
        """
        # Getting one of users IDs in the list.
        visitingProfileID = profilesQueued.pop()
        # Appending user ID to visitedProfile list.
        visited_profiles.append(visitingProfileID)
        # Construct full url to GET to.
        full_link = 'https://www.linkedin.com' + visitingProfileID
        # Getting to users page
        self.browser.get(full_link)

        self.browser.maximize_window()


    def scrape_general_info(self):
        """
        Creating soup object to scrape user's profile.
        """
        src = self.browser.page_source
        soup = BeautifulSoup(src, 'lxml')

        # Navigating to target data section
        general_info_section = soup.find('div', {'class': 'ph5 pb5'}).find('div', {'class': 'flex-1 mr5'})
        # Exctracting user's name
        name = \
        general_info_section.find('ul', {'class': 'pv-top-card--list inline-flex align-items-center'}).findAll('li')[0]
        name = name.text.strip()
        # Extracting user's profile title.
        profile_title = general_info_section.find('h2')
        profile_title = profile_title.text.strip()
        # Extracting user's location
        location = \
        general_info_section.find('ul', {'class': 'pv-top-card--list pv-top-card--list-bullet mt1'}).findAll('li')[0]
        location = location.text.strip()
        # Extracting number of connections
        connections = \
        general_info_section.find('ul', {'class': 'pv-top-card--list pv-top-card--list-bullet mt1'}).findAll('li')[1]
        connections = connections.text.strip()



bot = Linkedin_Bot()
time.sleep(5)

bot.login()
time.sleep(random.randint(3, 5))

bot.go_to_admin()

profilesQueued = bot.getNewProfilesIDs(profilesQueued)
print(profilesQueued)
