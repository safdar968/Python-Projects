from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

while True:

    driver = webdriver.Chrome()
    driver.get('https://fake-it.ws/index.php?1553157689&amp;amp;for_country=de')
    timeout = 20
    try:
        element_present = EC.presence_of_element_located((By.ID, 'iban'))
        WebDriverWait(driver, timeout).until(element_present)
        print('done')
        elem = driver.find_elements_by_xpath("//span[@id='iban']")[0].text
        print(elem)
        with open('output.txt', 'a') as f:
            f.write(elem)
            f.write('\n')
            

    except TimeoutException:
        print("Timed out waiting for page to load")

    driver.close()
    time.sleep(5)
