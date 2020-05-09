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

        print("User Name: ", name)
        print("Profile title: ", profile_title)
        print("Location: ", location)
        print("Connections: ", connections)
        print()

        general_info = {}
        general_info['User Name'] = name
        general_info['Profile Title'] = profile_title
        general_info['Location'] = location
        general_info['Connections'] = connections

        return general_info

    def experience_scraper(self):
        total_experience_info = {}
        src = self.browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        # selecting elements more specificly.
        selector = '#experience-section > ul > li > section > div > div > a.ember-view'
        experience_section = soup.select(selector)
        experience_counter = 1
        for experience in experience_section:
            print("Experience NO. {}".format(experience_counter))
            # Extracting job title.
            job_title = experience.find('h3').text.strip()
            company_name = experience.findAll('p')[-1].text.strip().split('\n')[0]
            employement_type = experience.findAll('p')[-1].text.strip().split('\n')[-1].strip()
            dates = experience.find('div', {'class': 'display-flex'}).findAll('h4')[0].findAll('span')[-1].text.strip()
            duration = experience.find('div', {'class': 'display-flex'}).findAll('h4')[-1].findAll('span')[
                -1].text.strip()
            company_location = \
            experience.find('h4', {'class': 'pv-entity__location t-14 t-black--light t-normal block'}).findAll('span')[
                -1].text.strip()

            print("Job Title: ", job_title)
            print("Company Name: ", company_name)
            print("Employement Type: ", employement_type)
            print("From {} To {}".format(dates.split('–')[0], dates.split('–')[1]))
            print("Duration: ", duration)
            print("Company Location: ", company_location)
            print()

            # Creating a dictionary for saving extracted experience detail that scraped from user profile
            experience_info = {}
            experience_info['Job Title'] = job_title
            experience_info['Company Name'] = company_name
            experience_info['Employement Type'] = employement_type
            experience_info['Dates'] = dates
            experience_info['Duration'] = duration
            experience_info['Company Location'] = company_location
            # Appending job details to bigger dictionary.
            total_experience_info['Experience NO. {}'.format(experience_counter)] = experience_info

            experience_counter += 1

        return total_experience_info


    def education_data_scraper(self):
        total_education_info = {}
        src = self.browser.page_source
        soup = BeautifulSoup(src, 'lxml')
        # Navigating to education data section (Creating hook to ease in locating elements)
        education_list = soup.find('section', {'id': 'education-section'}).find('ul').findAll('li')
        education_counter = 1
        for educatoin in education_list:
            print("Education NO. ", education_counter)
            info_section = educatoin.find('div', {
                'class': 'pv-entity__summary-info pv-entity__summary-info--background-section'})
            educational_center = info_section.find('div', {'class': 'pv-entity__degree-info'}).find('h3').text.strip()
            degree_name = info_section.find('div', {'class': 'pv-entity__degree-info'}).findAll('p')[0].findAll('span')[
                -1].text.strip()
            field_of_study = \
            info_section.find('div', {'class': 'pv-entity__degree-info'}).findAll('p')[-1].findAll('span')[
                -1].text.strip()
            start_date = \
            info_section.find('p', {'class': 'pv-entity__dates t-14 t-black--light t-normal'}).findAll('span')[
                -1].findAll('time')[0].text.strip()
            end_date = \
            info_section.find('p', {'class': 'pv-entity__dates t-14 t-black--light t-normal'}).findAll('span')[
                -1].findAll('time')[1].text.strip()

            print("Educated at: ", educational_center)
            print("Defree: ", degree_name)
            print("Field of Study: ", field_of_study)
            print("From {} to {}".format(start_date, end_date))
            print()

            education_info = {}
            education_info['Educational Center'] = educational_center
            education_info['Degree Name'] = degree_name
            education_info['Filed of Study'] = field_of_study
            education_info['Start Date'] = start_date
            education_info['End Date'] = end_date

            total_education_info['Education NO. {}'.format(education_counter)] = education_info

            education_counter += 1

        return total_education_info


    #def send_invitaion(self):
    #    """
    #    This method will send customized invitation to users.
    #    """


bot = Linkedin_Bot()
time.sleep(5)

bot.login()
time.sleep(random.randint(3, 5))

bot.go_to_admin()

profilesQueued = bot.getNewProfilesIDs(profilesQueued)
print(profilesQueued)

bot.visit_profile(profilesQueued)

info = bot.scrape_general_info()
experience = bot.experience_scraper()
education = bot.education_data_scraper()


print('USER INFO')
print(' '*10, "General Information")
for key, value in info.items():
    print(key, value)

print()
print(' '*10, "Experience Information")
for key, value in experience.items():
    print(key, value)

print()
print(' '*10, "Education Information")
for key, value in education.items():
    print(key, value)