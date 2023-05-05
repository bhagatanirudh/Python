import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

path = 'D:\Python\chromedriver'
driver = webdriver.Chrome(path)
# driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
website = 'https://internshala.com/'
driver.get(website)
driver.maximize_window()

# logging in the website
driver.find_element("xpath", "//button[@type='button'][normalize-space()='Login']").click()
username = ""  #Username required
driver.find_element("id", "modal_email").send_keys(username)
password = ""  #Password required
driver.find_element("id", "modal_password").send_keys(password)
driver.find_element("xpath", "//button[@id='modal_login_submit']").click()
time.sleep(2)

# hover over interships
actChain = ActionChains(driver)
intern = driver.find_element("xpath", "//a[@id='internships_new_superscript']")
actChain.move_to_element(intern).perform()
time.sleep(2)

# selecting location 
driver.find_element("xpath", "(//span[contains(text(),'Location')])[1]").click()
driver.find_element("xpath", "//a[normalize-space()='Work from Home']").click()
# time.sleep(2)

# Selecting my preference 
try :
    driver.find_element("xpath", '//*[@id="search_form"]/div[1]/label').click()
    time.sleep(3)
except:
  print("An exception occurred.")

# closing pop-up screen
# Required when user is not login to intershala
# driver.find_element("id", "close_popup").click()

# For manual entering job category for preferable job 
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# category = driver.find_element(By.XPATH, "(//input[@value='e.g. Marketing'])[1]")
# category.click()
# category.send_keys("Computer Science")
# category.send_keys(Keys.ENTER)
# wfh = driver.find_element(By.ID, 'work_from_home').get_attribute('checked')
# if(wfh == None):
#     driver.find_element(By.XPATH, "//label[@for='work_from_home']").click()


# Selecting the stipend range as per choice
try:
  slider = driver.find_element("id", "stipend_filter")
  actChain.click_and_hold(slider).move_by_offset(60, 0).release().perform()
  time.sleep(3)
except:
  print("Not able to find element.")

# Extracting data(intership) based upon keyword we want
from selenium.webdriver.common.by import By
import pandas as pd
import pywhatkit as kit
import re
intershipList = []
keyWords = ['Java', 'Selenium', 'Software', 'Testing', 'Programming', 'Coding', 'Competitive', 'Computer Science']
nextpage = driver.find_element("xpath", "//i[@id='navigation-forward' or @class='disabled']")
nextClass = nextpage.get_attribute("class")
while(nextClass != 'disabled'):
    time.sleep(1)
    data = wait(driver, 10).until(EC.presence_of_all_elements_located(("xpath", "//div[contains(@class, 'container-fluid individual_internship')]")))
    for item in data:
        try:
            jobRole = item.find_element(By.TAG_NAME, 'a')
            jobRoleLink = jobRole.get_attribute('href')
            companyName = item.find_element(By.CLASS_NAME, 'company_and_premium').text
            stipend = item.find_element(By.CLASS_NAME, 'stipend').text

            if re.compile('|'.join(keyWords), re.IGNORECASE).search(jobRole.text): 
                intership = {
                    'role' : jobRole.text,
                    'link' : jobRoleLink,
                    'company' : companyName,
                    'stipend' : stipend
                }
                intershipList.append(intership)    
        except:
            print("Exception occurred --- 1")
            
    # go-to next page
    nextpage = driver.find_element("xpath", "//i[@id='navigation-forward' or @class='disabled']")
    nextpage.click()
    nextClass = nextpage.get_attribute("class")
  
df = pd.DataFrame(intershipList)
# print(df.head())
df.to_csv('intership.csv') 

# Sending screenshot and link to user wahtsApp
import pywhatkit as kit
myPhoneNumber = '+918080672181'
for index, intershipRow in df.iterrows():
    driver.get(intershipRow.link)
    screenshotFilepath = "D:\\Intershala project\\screenshot_" + str(index) + ".png"
    driver.save_screenshot(screenshotFilepath)
    kit.sendwhats_image(myPhoneNumber, screenshotFilepath, intershipRow.link)

driver.quit()
