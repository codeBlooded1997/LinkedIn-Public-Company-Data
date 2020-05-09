import requests, time, random
from bs4 import BeautifulSoup
from selenium import webdriver
from random import randint



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
time.sleep(random.randint(5, 8))



#link = 'https://www.linkedin.com/in/harneetsingh160993/'
links = ['https://www.linkedin.com/in/darshita-patel-4566b76b/', 'https://www.linkedin.com/in/harneetsingh160993/']

for link in links:
    driver.get(link)

    SCROLL_PAUSE_TIME = 5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(3):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Creating soup object
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    # Navigating to target data section
    general_info_section = soup.find('div', {'class':'ph5 pb5'}).find('div', {'class':'flex-1 mr5'})
    # Exctracting user's name
    name = general_info_section.find('ul', {'class':'pv-top-card--list inline-flex align-items-center'}).findAll('li')[0]
    name = name.text.strip()
    # Extracting user's profile title.
    profile_title = general_info_section.find('h2')
    profile_title = profile_title.text.strip()
    # Extracting user's location
    location = general_info_section.find('ul', {'class':'pv-top-card--list pv-top-card--list-bullet mt1'}).findAll('li')[0]
    location = location.text.strip()
    # Extracting number of connections
    connections = general_info_section.find('ul', {'class':'pv-top-card--list pv-top-card--list-bullet mt1'}).findAll('li')[1]
    connections = connections.text.strip()

    info = []
    info.append(link)
    info.append(name)
    info.append(profile_title)
    info.append(location)
    info.append(connections)

    for item in info:
        print(item)

    """
    Using css selectors to navigate to general data sction.
    """
    src = driver.page_source
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
        duration = experience.find('div', {'class': 'display-flex'}).findAll('h4')[-1].findAll('span')[-1].text.strip()
        company_location = experience.find('h4', {'class': 'pv-entity__location t-14 t-black--light t-normal block'}).findAll('span')[-1].text.strip()
        experience_counter += 1

        print("Job Title: ", job_title)
        print("Company Name: ", company_name)
        print("Employement Type: ", employement_type)
        print("From {} To {}".format(dates.split('–')[0], dates.split('–')[1]))
        print("Duration: ", duration)
        print("Company Location: ", company_location)
        print()



    # Navigating to education data section (Creating hook to ease in locating elements)
    education_list = soup.find('section', {'id': 'education-section'}).find('ul').findAll('li')
    education_counter = 1
    for educatoin in education_list:
        print("Education NO. ", education_counter)
        info_section = educatoin.find('div', {'class': 'pv-entity__summary-info pv-entity__summary-info--background-section'})
        educational_center = info_section.find('div', {'class': 'pv-entity__degree-info'}).find('h3').text.strip()
        degree_name = info_section.find('div', {'class': 'pv-entity__degree-info'}).findAll('p')[0].findAll('span')[-1].text.strip()
        field_of_study = info_section.find('div', {'class': 'pv-entity__degree-info'}).findAll('p')[-1].findAll('span')[-1].text.strip()
        start_date = info_section.find('p', {'class': 'pv-entity__dates t-14 t-black--light t-normal'}).findAll('span')[-1].findAll('time')[0].text.strip()
        end_date = info_section.find('p', {'class': 'pv-entity__dates t-14 t-black--light t-normal'}).findAll('span')[-1].findAll('time')[1].text.strip()
        education_counter += 1

        print("Educated at: ", educational_center)
        print("Defree: ", degree_name)
        print("Field of Study: ", field_of_study)
        print("From {} to {}".format(start_date, end_date))
        print()