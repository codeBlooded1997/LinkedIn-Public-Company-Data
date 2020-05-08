from bs4 import BeautifulSoup
import os, random, sys, time
from random import randint
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

# Extracting username and password.
file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]

"""
Opening driver and getting the url to Linkedin login page.
"""
# Path to chromedriver.
path_to_chromedriver = '/Users/arian/WorkSpace/dev/scraper/drivers/chromedriver'
# Opening a dirver.
driver = webdriver.Chrome(executable_path=path_to_chromedriver)
# Simulating human user.
time.sleep(randint(3, 5))
# URL to page.
url = 'https://www.linkedin.com/uas/login'
# Getting the url
driver.get(url)

"""
Logs in to the users page.
"""
# Xpath to username input.
xp_username = '//*[@id="username"]'
# Xpath to password input.
xp_password = '//*[@id="password"]'
# Simulating human.
time.sleep(randint(2, 3))
# Sending username.
username_input = driver.find_element_by_xpath(xp_username)
username_input.send_keys(username)
# Simulating human.
time.sleep(randint(2, 3))
# Sending password.
password_input = driver.find_element_by_xpath(xp_password)
password_input.send_keys(password)
# Xpath to submit button.
# Simulating human.
time.sleep(randint(5, 8))
xp_submit = '//*[@id="app__container"]/main/div[2]/form[@class="login__form"]/div[@class="login__form_action_container "]/button'
# Submiting (Clicking on button)
submit_button = driver.find_element_by_xpath(xp_submit)
submit_button.click()

"""
This method navigates to user section.
"""
# ID we are going to visit.
visitingProfileID = '/in/arian-aghnaei-6633471a0/'
# Constructing link
fullLink = 'https://www.linkedin.com' + visitingProfileID
# Directing to profile page using ID
driver.get(fullLink)
#driver.maximize_window()

visited_profiles = []
profilesQueued = []


def getNewProfilesIDs(soup, profilesQueued):
    profilesID = []
    pav = soup.find('section', {
        'class': 'pv-profile-section pv-browsemap-section profile-section artdeco-container-card ember-view'})
    all_links = pav.findAll('a', {'class', 'pv-browsemap-section__member ember-view'})
    for link in all_links:
        user_id = link.get('href')
        if ((user_id not in visited_profiles) and (user_id not in profilesQueued)):
            profilesID.append(user_id)

    return profilesID

profilesQueued = getNewProfilesIDs(BeautifulSoup(driver.page_source), profilesQueued)

"""
Visiting each of extracted users page.
"""
while profilesQueued:
    try:
        # Getting one of users IDs in the list.
        visitingProfileID = profilesQueued.pop()
        # Appeinging user ID to visitedProfile
        visited_profiles.append(visitingProfileID)
        full_link = 'https://www.linkedin.com' + visitingProfileID
        # Getting to users page
        driver.get(full_link)

        # Clicking on the connect button of user's profile.
        xp_connect_button = '//section[@class="pv-top-card artdeco-card ember-view"]/div[2]/div[@class="display-flex"]/div[2]/div/div/span/div/button'
        driver.find_element_by_xpath(xp_connect_button).click()
        time.sleep(2)

        # Inputing message to textarea
        custom_message = "Hello, I have found mutual interest area and I would be more than happy to connect with you. please accept my invitation. Thanks!"
        xp_textbox = '//div[@class="relative"]/textarea'
        elementID = driver.find_element_by_xpath(xp_textbox)
        elementID.send_keys(custom_message)

        # Sending message to user
        xp_send_invitation = '//div[@class="artdeco-modal__actionbar text-align-right ember-view"]/button[2]'
        driver.find_element_by_xpath(xp_send_invitation).click()
        time.sleep(3)

        # Add the ID to the visitedUsersFile
        with open('visitedUsers.txt', 'a') as visitedUserFile:
            visitedUserFile.write(str(visitingProfileID) + '\n')
        visitedUserFile.close()

        # Get new users ID
        soup = BeautifulSoup(driver.page_source)
        try:
            new_users = getNewProfilesIDs(soup, profilesQueued)
            print(new_users)
            print('Extending the list of users...')
            time.sleep(3)
            profilesQueued.extend(new_users)
        except:
            print('Continue.')

        # pause
        print('SLEEPING...')
        print()
        time.sleep(random.uniform(5, 15))  # Otherwise sleep to make sure

        # If we have sent invitations to 100,000 user save the result and break
        if len(profilesQueued) > 100000:
            with open('profilesQueued.txt', 'a') as visitedUsersFile:
                visitedUsersFile.write(str(visitingProfileID) + '\n')
            visitedUsersFile.close()
            print('100,000 Done!!!')
            break
        else:
            print('Messaging to next users')
    except Exception as e:
        print('error')
        print(e)
        try:
            soup = BeautifulSoup(driver.page_source)
            new_users = getNewProfilesIDs(soup, profilesQueued)
            print(new_users)
            time.sleep(8)
            print('Extending the list of users...')
            time.sleep(3)
            profilesQueued.extend(new_users)
        except:
            print('Continue.')