from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
from random_username.generate import generate_username
import time, csv
import random

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)

interations = 10  # set number of enteries 

for i in range(interations):
    print('Entry #', i+1)
    with open('log.csv', 'a') as csvfile:
        writerCSV = csv.writer(csvfile)

        name = generate_username()[0]
        email = name+'@slashshots.com'
        phone = '+62'+ str(random_with_N_digits(8))
        postcode = str(random_with_N_digits(6))
        colors = ['Black/ White/Varsity Blue', 'Maize/Red/Navy']
        color = random.choice(colors)
        sizes = [5,5.5,6,6.5,7,7.5,8,8.5,9,95,10,10.5,11,11.5,12]
        size = str(random.choice(sizes))

        driver = webdriver.Chrome()
        url = 'https://singapore.doverstreetmarket.com/new-items/raffle'
        driver.get(url)
        timeout = 20
        try:
            element_present = EC.presence_of_element_located((By.ID, 'fsSubmit3466791'))
            WebDriverWait(driver, timeout).until(element_present)
            print('page loaded ......... ')
            F_name = driver.find_element_by_id("field78092289")
            F_name.send_keys(name)
            time.sleep(1)

            F_email = driver.find_element_by_id("field78092290")
            F_email.send_keys(email)
            time.sleep(1)

            F_phone = driver.find_element_by_id("field78092291")
            F_phone.send_keys(phone)
            time.sleep(1)

            F_postcode = driver.find_element_by_id("field78092292")
            F_postcode.send_keys(postcode)
            time.sleep(1)

            F_color = Select(driver.find_element_by_id("field78092293"))
            F_color.select_by_visible_text(color)
            time.sleep(1)

            F_size = Select(driver.find_element_by_id("field78092294"))
            F_size.select_by_visible_text(size)
            time.sleep(1)
            
            
                
            api_key = '11ab37dcf9129c95f0b78c0a50563739'
            site_key = '6LetKEIUAAAAAPk-uUXqq9E82MG3e40OMt_74gjS'  # grab from form

            client = AnticaptchaClient(api_key)
            task = NoCaptchaTaskProxylessTask(url, site_key)
            job = client.createTask(task)
            print("Waiting to solution by Anticaptcha workers")
            job.join()

            # Receive response
            response = job.get_solution_response()
            print("Received solution", response)

            # Inject response in webpage
            driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % response)
            print('captcha solved')
            # Wait a moment to execute the script (just in case).
            time.sleep(5)
            driver.execute_script('document.getElementById("fsForm3466791").submit()')
        

        except TimeoutException:
            print("Timed out waiting for page to load")

        print('Completed Entry # ', i+1)
        print('______________________________________________')
        time.sleep(10)
        driver.close()
        writerCSV.writerow([name,email,phone,postcode,color,size])
        time.sleep(5)
