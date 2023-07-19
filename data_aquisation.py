
import time
import random
import codecs
import sys
import re
import pandas as pd
from pandas import concat
import xlsxwriter
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
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidSelectorException

codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

min_delay = 1  # Minimum delay in seconds
max_delay = 10  # Maximum delay in seconds

# Generate a random time delay within the specified range
delay = random.uniform(min_delay, max_delay)

log_email = 'GHavet@havetdigital.fr'
log_pass = 'Havetdigital2023!'

website = 'https://www.linkedin.com/'
path = 'C:/Users/Youcode/Downloads/chromedriver_win32/chromedriver.exe'

service = Service(path)
driver = webdriver.Chrome(service=service)
driver.get(website)

wait = WebDriverWait(driver, 15)

def is_logged(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, '.global-nav__me-photo')
        return True
    except NoSuchElementException:
        return False

while not is_logged(driver):
    try:
        email = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="session_key"]')))
        password = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="session_password"]')))
        print('Logging in...')
        email.send_keys(log_email)
        time.sleep(delay)
        password.send_keys(log_pass)
        time.sleep(delay)
        password.send_keys(Keys.ENTER)
    except (NoSuchElementException, TimeoutException, ElementNotInteractableException):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
        driver.switch_to.window(driver.window_handles[-1])
        driver.get('https://linkedin.com')
        print('Trying page 2...')
        email2 = wait.until(EC.presence_of_element_located((By.XPATH , '//*[@id="session_key"]')))
        password2 = wait.until(EC.presence_of_element_located((By.XPATH , '//*[@id="session_password"]')))
        email2.send_keys(log_email)
        time.sleep(delay)
        password2.send_keys(log_pass)
        time.sleep(delay)
        password2.send_keys(Keys.ENTER)
        continue
    else:
        print('Waiting to solve captcha...')
        time.sleep(10)
        print('Logged in successfully')
        break

df = pd.read_excel('contact.xlsx')
linkedin = df['linkedIn']
profiles_name = []
profiles_job = []
profiles_adresse = []
profile_links = []
count = 0
for url in linkedin:
    count+=1
    profile_data = {}

    driver.get(url)
    try:
        name = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="profile-card-section"]/section[1]/div[1]/div[2]/h1')))
        name_text = name.text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
        profiles_name.append(name_text)
    except (NoSuchElementException, TimeoutException):
        print(f"Name not found for {url}")
        continue
    
    try:
        post = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="profile-card-section"]/section[1]/div[1]/div[3]/span')))
        post_text = post.text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
        profiles_job.append(post_text)
    except (NoSuchElementException, TimeoutException):
        print(f"Job post not found for {url}")
        continue
    
    try:
        adresse = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="profile-card-section"]/section[1]/div[1]/div[4]/div[1]')))
        adresse_text = adresse.text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
        profiles_adresse.append(adresse_text)
    except (NoSuchElementException, TimeoutException):
        print(f"Adresse not found for {url}")
        continue
 
    name_text = name.text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
    post_text = post.text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
    adresse_text = adresse.text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
    
    print(name_text)
    print(post_text)
    print(adresse_text)
    
    profiles_name.append(name_text)
    profiles_job.append(post_text)
    profiles_adresse.append(adresse_text)

    related_links = []
    try:
        display_all = wait.until(EC.presence_of_element_located((By.XPATH , '/html/body/main/div[1]/div[3]/div/div[1]/div/div/section[1]/section[2]/section/div/address/button')))
        display_all.click()
        select_links = wait.until(EC.presence_of_all_elements_located((By.XPATH , '//html/body/div[6]/div/div/div[2]//a')))
        for link in select_links:
            related_links.append(link.get_attribute('href'))
        profile_links.append(related_links)

        print('Social links:')
        print(related_links)
    except (NoSuchElementException, InvalidSelectorException, TimeoutException):
        print('No social links')
        profile_links.append([])

    print(name_text)
    print(post_text)
    time.sleep(delay)

    # Create DataFrame for each profile
    schema = {
        'Prenom': [name_text],
        'Nom': None,
        'email': None,
        'emailPerso': None,
        'linkedIn': [url],
        'phone': None,
        'mobile': None,
        'adresse1': [adresse_text],
        'adresse2': None,
        'code_postal': None,
        'ville': None,
        'pays': None,
        'job': [post_text],
        'dateAnnivairsaire': None,
        'socialAccount': [related_links],
        'source': None,
    }

    df_profile = pd.DataFrame(schema)

    # Append DataFrame to existing DataFrame
    print('##CONCAT###')
    df = pd.concat([df, df_profile], ignore_index=True)
    # if count == 3:
    #     print('3 elements')
    #     break

writer = pd.ExcelWriter('contact_result_table.xlsx', engine='xlsxwriter')
writer.book.encoding = 'utf-8'


# df.to_excel('contact.xlsx', index=False, encoding='utf-8')
df.to_excel(writer, index=False)


print(len(profiles_name))
print(len(profiles_adresse))
print(len(profiles_job))
print(len(profile_links))

writer.close()
