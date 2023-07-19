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


codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)
# sys.stdout.encoding = 'utf-8'


profiles = {}

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
# input('')
wait = WebDriverWait(driver, 15)
email=wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="session_key"]')))
password = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="session_password"]')))



email.send_keys(log_email)
time.sleep(delay)
password.send_keys(log_pass)
time.sleep(delay)

password.send_keys(Keys.ENTER)

time.sleep(20)
driver.get('https://www.linkedin.com/sales/home')



df = pd.read_excel('dep65.xlsx')

company_names = df['nom_entreprise']




for company in company_names:
    search_bar = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='global-typeahead-search-input']")))
    print(f'searching for {company}-:: ')

    search_bar.send_keys(company)
    time.sleep(2)
    search_bar.send_keys(Keys.ENTER)
    
    time.sleep(4)
    try:
        time.sleep(3)
        next_page = driver.find_element(By.CSS_SELECTOR , '.artdeco-pagination__button.artdeco-pagination__button--next.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view')
    except NoSuchElementException:
        next_page = None    
    time.sleep(2)
    print(next_page)
   
    
    
    page_counter = 1
    while  next_page is not None:
        time.sleep(delay)
        
        page_counter += 1
        select_all = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/div[2]/div[1]/div[2]/div/div[1]/label/span")))
        save_list =  wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/main/div[1]/div[2]/div[1]/div[2]/div/div[3]/button/span")))
       
        try:
            print('####SELECT ALL####')
            select_all.click()
            print('#### SAVE ALL###')
            # time.sleep(2)

            save_list.click()
            # time.sleep(3)
        except ElementClickInterceptedException:
            time.sleep(4)
            print('#### reSELECT ALL####')
            select_all.click()
            print('#### reSAVE ALL###')
            # time.sleep(2)
            save_list.click()
        dropdown_menu = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'save-to-list-dropdown__content-container') and contains(@class, 'artdeco-dropdown__content') and contains(@class, 'artdeco-dropdown--is-dropdown-element') and contains(@class, 'artdeco-dropdown__content--justification-left') and contains(@class, 'artdeco-dropdown__content--placement-bottom') and contains(@class, 'ember-view')]/div[contains(@class, 'artdeco-dropdown__content-inner')]")))
    
    
        dropdown_html = dropdown_menu.get_attribute('innerHTML')
        
        #translate the bellow  string into french  
        if 'Aucun prospect ne correspond à votre recherche' in dropdown_html:
            break
        # if page_counter == 4:
            # break

        time.sleep(3) 
        
        if company[:10].strip() in dropdown_html.strip():
            # print(str(company))
            print('existed list')
            add_to_list = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='" + str(company.strip()) + "']" )))
            add_to_list.click()
            time.sleep(delay)
            print('########### NEXT PAGE ########')
            time.sleep(delay)
            try:
                next_page.click()
            except StaleElementReferenceException:
                current_link = driver.current_url
                next_link = current_link.replace(re.search(r"page=\d+", current_link).group(), f"page={page_counter}")
                driver.get(next_link)  
            
            
        else:
            print('new list')
            add_to_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR , '.button--unstyled.save-to-list-dropdown-v2__create-list-cta')))
            add_to_list.click()
            create_new_list = driver.find_element(By.CSS_SELECTOR , '.text-input__input')
            create_new_list.send_keys(str(company))
            submit = driver.find_element(By.CSS_SELECTOR , '.artdeco-button.artdeco-button--2.artdeco-button--pro.artdeco-button--primary.ember-view.ml2')
            time.sleep(delay)
            submit.click()
            
            print('########### NEXT PAGE ########')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                next_page.click()
            except StaleElementReferenceException:
                current_link = driver.current_url
                next_link = current_link.replace(re.search(r"page=\d+", current_link).group(), f"page={page_counter}")
                driver.get(next_link) 
                         


        #########
    else:
        select_all = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[1]/div[2]/div[1]/div[2]/div/div[1]/label/span")))
        save_list =  wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/div[1]/div[2]/div[1]/div[2]/div/div[3]/button/span")))
        print('####SELECT ALL####')
        select_all.click()
        print('#### SAVE ALL###')
        save_list.click()
        time.sleep(2)
        dropdown_menu = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'save-to-list-dropdown__content-container') and contains(@class, 'artdeco-dropdown__content') and contains(@class, 'artdeco-dropdown--is-dropdown-element') and contains(@class, 'artdeco-dropdown__content--justification-left') and contains(@class, 'artdeco-dropdown__content--placement-bottom') and contains(@class, 'ember-view')]/div[contains(@class, 'artdeco-dropdown__content-inner')]")))
        dropdown_html = dropdown_menu.get_attribute('innerHTML')
        if str(company) in dropdown_html:
            print(str(company))
            add_to_list = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='" + str(company) + "']" )))
            add_to_list.click()
            print('existed list')
            time.sleep(delay)
            print('NO PAGINATION')
            
        else:
            add_to_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR , '.button--unstyled.save-to-list-dropdown-v2__create-list-cta')))
            add_to_list.click()
            create_new_list = driver.find_element(By.CSS_SELECTOR , '.text-input__input')
            create_new_list.send_keys(str(company))
            submit = driver.find_element(By.CSS_SELECTOR , '.artdeco-button.artdeco-button--2.artdeco-button--pro.artdeco-button--primary.ember-view.ml2')
            time.sleep(delay)
            submit.click()
            print('new list')
            print('NO PAGINATION')
        

# .artdeco-dropdown__content-inner
    # input('')

    driver.get('https://www.linkedin.com/sales/home')
    time.sleep(delay)






