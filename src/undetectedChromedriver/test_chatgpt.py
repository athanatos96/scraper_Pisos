from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions

import time


COOKIES_SECTION_CLASS = 'didomi-regular-notice didomi-banner-notice-optin-type didomi-notice-banner shape-banner bottom'
REJECT_COOKIES_BUTTON_ID = 'didomi-notice-disagree-button'
MUNICIPALITY_SEARCH_ID = 'municipality-search'


url = "https://www.idealista.com/"
URL = "https://www.idealista.com/"
#'''
options = ChromeOptions()
#options.add_argument("--headless")
driver = Chrome(options=options, use_subprocess=True)
#driver.get(url)
#time.sleep(5)
try:
    driver.execute_script(f"window.open('_blank', 'Testing');")
    print("Opened")
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[1])
    print("Changeed to 1")
    time.sleep(3)
    driver.switch_to.window(driver.window_handles[0])
    print("Changeed to 0")
    time.sleep(3)
    driver.execute_script(f"window.open('{url}', 'Testing');")
    print("Open URL ", url)
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    print("Changeed to 1")
    time.sleep(3)
    driver.save_screenshot('loadscreen.png') # Wait for 5 seconds to ensure that the browser has fully loaded
except:
    pass
driver.quit()

#'''
'''
import undetected_chromedriver as webdriver
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--use_subprocess")

browser = webdriver.Chrome(options=chrome_options)

browser.get(url)
browser.save_screenshot("screenshot.png")
'''