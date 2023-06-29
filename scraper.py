from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

URL = "https://webgate.ec.europa.eu/rasff-window/screen/search"
driver.get(URL)

search = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="search"]/div[3]/div[4]/button')))
driver.execute_script('arguments[0].click()', search)

next_page_button = driver.find_element(By.XPATH,'//*[@id="main-content"]/app-search-component/div/app-list-component/div/div[3]/mat-paginator/div/div/div[2]/button[2]')

counter = 1
alerts_list = []

while counter < 12950:
  try:
    alerts = driver.find_elements(By.CLASS_NAME,'nt-list-item')

    for i in alerts:
      alerts_list.append(i.text)

    counter += 25
    driver.execute_script('arguments[0].click()', next_page_button)
    time.sleep(5)
    
  except ElementClickInterceptedException:
    driver.implicitly_wait(10)

driver.quit()

new_alerts_list = [i.replace("\nDetails >>", "").replace("\n", " - ") for i in alerts_list]
final_alerts_list = [i.split(" - ", 7) for i in new_alerts_list]

file = open('RASFF_new.csv', 'w', encoding="utf-8")
writer = csv.writer(file)
head = ["REFERENCE", "PRODUCT CATEGORY", "TYPE", "SUBJECT", "DATE CASE", "NOTIFICATION COUNTRY", "CLASSIFICATION", "RISK DECISION"]
writer.writerow(head)

for i in final_alerts_list:
    writer.writerow(i)

file.close()