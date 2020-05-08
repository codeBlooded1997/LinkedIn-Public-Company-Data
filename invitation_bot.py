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