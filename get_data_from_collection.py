import time
import random
import codecs
import sys
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException


codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

min_delay = 1  # Minimum delay in seconds
max_delay = 10  # Maximum delay in seconds

# Generate a random time delay within the specified range
delay = random.uniform(min_delay, max_delay)

log_email = 'GHavet@havetdigital.fr'
log_pass = 'Havetdigital2023!'

website = 'https://www.linkedin.com/?original_referer'
path = 'C:/Users/Youcode/Downloads/chromedriver_win32/chromedriver.exe'

service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get(website)

wait = WebDriverWait(driver, 15)
email = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="session_key"]')))
password = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="session_password"]')))

print('loggedIN')

email.send_keys(log_email)
time.sleep(delay)
password.send_keys(log_pass)
time.sleep(delay)

password.send_keys(Keys.ENTER)

time.sleep(20)

prospects = driver.get("https://www.linkedin.com/sales/lists/people")
time.sleep(6)

companies = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[@class='artdeco-models-table-row ember-view']//td[@class='artdeco-models-table-cell ember-view']//div[@class='flex align-items-center list-hub__name-row']//a")))

print('loop began')

time.sleep(4)
i = 1

prospects_links = []
profiles = []
companies_name = []
for link in companies:
    # company_name = link.text
    # companies_name.append(company_name)   this contains the company names 
    linkedin_list = link.get_attribute('href')
    prospects_links.append(linkedin_list)

print(prospects_links)

for i, link in enumerate(prospects_links, start=1):
    print(i)
    driver.get(link)
    time.sleep(delay)

    try:
        profile_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[@class='artdeco-models-table-row ember-view']//td[@class='artdeco-models-table-cell list-people-detail-header__entity ember-view']//div[@class='white-space-nowrap overflow-hidden text-overflow-ellipsis']//a")))
        
        for pr_link in profile_links:
            profile = pr_link.get_attribute('href')
            print(profile)
            profiles.append(profile)
    
    except (NoSuchElementException, StaleElementReferenceException , TimeoutException):
        print("Element not found. Saving current data to Excel.")
        # break
    
    print(f'company number {i}')

schema = {
    'Prenom': None,
    'Nom': None,
    'email': None,
    'emailPerso': None,
    'linkedIn': profiles,
    'phone': None,
    'mobile': None,
    'adresse1': None,
    'adresse2': None,
    'code_postal': None,
    'ville': None,
    'pays': None,
    'job': None,
    'dateAnnivairsaire': None,
    'socialAccount': None,
    'source': None,
    #'company':companies_name
}

df = pd.DataFrame(schema)

output_file = 'contact.xlsx'

df.to_excel(output_file, index=False)
driver.close()