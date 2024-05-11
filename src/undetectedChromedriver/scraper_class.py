from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time
import beepy as beep
import random

from utils import random_sleep_with_progress

class WebScraper:
    def __init__(self, url, headless=True, captcha_id = None, handle_captcha_attempts = 10, wait_time_for_button = 10, **kwargs):
        self.url = url
        self.headless = headless
        self.captcha_id = captcha_id
        self.handle_captcha_attempts = handle_captcha_attempts
        self.wait_time_for_button = wait_time_for_button
        self.kwargs = kwargs
        self.driver = self._initialize_driver()
        self.driver.get(self.url)
        self.counter = 0
    def _initialize_driver(self):
        options = ChromeOptions()
        options.add_argument("--headless") if self.headless else None
        for key, value in self.kwargs.items():
            options.add_argument(value)

        driver = Chrome(options=options)
        return driver
    def _find_element(self, by, value):
        try:
            element = self.driver.find_element(by, value)
            return element
        except NoSuchElementException:
            print(f" - ERROR - [_find_element()] Element not found using {by}: {value}")
            return None
    def _find_element_within_element(self, parent_element, by, value):
        try:
            element = parent_element.find_element(by, value)
            return element
        except NoSuchElementException:
            print(f" - ERROR - [_find_element()] Element not found for elem using {by}: {value}")
            return None

    def handle_captcha_3(self, captcha_id, max_attempts=10):
        print(" - DEBUG - handle_captcha_3()")
        
        # Looks for the Iframe that contains teh captcha
        #iframe_element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
        iframe_element = self.wait_for_elememt_by_tag_name(tag_name = 'iframe', timeout=30)
        if iframe_element is None:
            print(" - INFO - No Iframe found with in the page")
            print(" - DEBUG - No capcha Iframe found")
            return True
        iframe_src = iframe_element.get_attribute('src')
        print(" - INFO - The src attribute of the captcha iframe is:", iframe_src)
        if 'captcha' not in iframe_src:
            print(" - DEBUG - SRC of the Iframe doesnt contain captcha")
            return True
        print(" - DEBUG - after wait for iframe element")
        self.driver.switch_to.frame(iframe_element)
        print(" - DEBUG - Switched to iframe element")
        
        # Now inside the iframe, find the <body> element
        print(" - DEBUG - Wait for the body of the captcha page to load")
        #iframe_body = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))   
        iframe_body = self.wait_for_elememt_by_tag_name(tag_name = 'body', timeout=10) 
        if iframe_element is None:
            print(" - ERROR - No Body found for the Iframe of the captcha")
            self.driver.switch_to.default_content()
            return False
        print(" - DEBUG - Body loaded")
        #self.driver.switch_to.frame(iframe_body)
        #print(" - DEBUG - Switched to captcha html body element")
        
        attempt = 1
        while attempt <= max_attempts:
            captcha_element = self.wait_for_element_by_id(element_id = captcha_id, timeout=30)
            if captcha_element:
                # There is a captcha
                print(" - WARNING - Captcha Present, Please fix")
                
                # Emit a NOISE sound to alert a human
                for ii in range(1,7): 
                    beep.beep(ii)
                    
                # Wait for 30 seconds before checking again
                time.sleep(30)
                attempt += 1
            else:
                html_content = self.get_page_source()
                file_path = f"./saved_html_{self.counter}.html"
                self.counter+=1
                # Open the file in write mode ('w' mode)
                with open(file_path, 'w', encoding='utf-8') as file:
                    # Write the HTML content to the file
                    file.write(html_content)
                print(f"HTML content has been saved to: {file_path}")
                
                self.driver.switch_to.default_content()
                return True
            
        self.driver.switch_to.default_content()
        # If max_attempts reached without success, raise an exception
        raise Exception(f"Reached maximum attempts ({max_attempts}) to handle CAPTCHA")   
    
    def handle_captcha_2(self):
        print(" - DEBUG - handle_captcha_2()")
        div_id_to_find = 'captcha-container'
        try:
            #iframe_element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'your iframe selector')))
            iframe_element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
            iframe_src = iframe_element.get_attribute('src')
            print(" - INFO - The src attribute of the iframe is:", iframe_src)


            print(" - DEBUG - after wait for element")
            self.driver.switch_to.frame(iframe_element)
            print(" - DEBUG - Switched to iframe")
            # Now inside the iframe, find the <body> element
            iframe_body = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
            
            try:
                # Attempt to find the <div> element by its id
                div_element = iframe_body.find_element(By.ID, div_id_to_find)
                print(f"Found <div> with id '{div_id_to_find}' inside the iframe!")
            except:
                print(f"Did not find <div> with id '{div_id_to_find}' inside the iframe.")
                
            print(" - DEBUG - after wait for element inside iframe")
            
        except Exception as e:
            print(' - ERROR - in handle_captcha_2')
            print(e)
            self.driver.switch_to.default_content()
            raise e
        
    def handle_captcha(self, captcha_id, max_attempts=10):
        print(" - DEBUG - handle_captcha()")
        attempt = 1
        while attempt <= max_attempts:
            captcha_element = self.wait_for_element_by_id(element_id = captcha_id, timeout=30)
            if captcha_element:
                # There is a captcha
                
                # Emit a NOISE sound to alert a human
                for ii in range(1,7): 
                    beep.beep(ii)
                    
                print(" - WARNING - Captcha Present, Please fix")
                # Wait for 30 seconds before checking again
                time.sleep(30)
                attempt += 1
            else:
                html_content = self.get_page_source()
                file_path = f"./saved_html_{self.counter}.html"
                self.counter+=1
                # Open the file in write mode ('w' mode)
                with open(file_path, 'w', encoding='utf-8') as file:
                    # Write the HTML content to the file
                    file.write(html_content)
                print(f"HTML content has been saved to: {file_path}")
                return True
        
        # If max_attempts reached without success, raise an exception
        raise Exception(f"Reached maximum attempts ({max_attempts}) to handle CAPTCHA")   
            
                  
    def click_button_by_id(self, button_id):
        print(" - DEBUG - click_button_by_id: ", button_id)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        button = self._find_element(By.ID, button_id)
        if button:
            button.click()
            print(" - INFO - Clicked button id: ", button_id)
            if self.captcha_id:
                # Handle Captcha
                self.handle_captcha_3(self.captcha_id, max_attempts = self.handle_captcha_attempts) 
            return True
        else:
            print(" - WARNING - Clicked button id: ", button_id, " NOT FOUND")
            return False
    def click_button_by_class_name(self, button_class):
        print(" - DEBUG - click_button_by_class_name: ", button_class)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        button = self._find_element(By.CLASS_NAME, button_class)
        if button:
            button.click()
            print(" - INFO - Clicked button class name: ", button_class)
            if self.captcha_id:
                # Handle Captcha
                self.handle_captcha_3(self.captcha_id, max_attempts = self.handle_captcha_attempts)
            return True
        else:
            print(" - WARNING - Clicked button class name: ", button_class, " NOT FOUND")
            return False
    
    def click_button_within_element_by_id(self, parent_element, child_id):
        print(" - DEBUG - click_button_within_element_by_id: ", child_id)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        button = self._find_element_within_element(parent_element, By.ID, child_id)
        if button:
            button.click()
            print(" - INFO - Clicked button ID: ", child_id)
            if self.captcha_id:
                # Handle Captcha
                self.handle_captcha_3(self.captcha_id, max_attempts = self.handle_captcha_attempts) 
            return True
        else:
            print(" - WARNING - Clicked button ID: ", child_id, " NOT FOUND")
            return False
    def click_button_within_element_by_class_name(self, parent_element, child_class):
        print(" - DEBUG - click_button_within_element_by_class_name: ", child_class)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        button = self._find_element_within_element(parent_element, By.CLASS_NAME, child_class)
        if button:
            button.click()
            print(" - INFO - Clicked button class name: ", child_class)
            if self.captcha_id:
                # Handle Captcha
                self.handle_captcha_3(self.captcha_id, max_attempts = self.handle_captcha_attempts) 
            return True
        else:
            print(" - WARNING - Clicked button class name: ", child_class, " NOT FOUND")
            return False
    def click_button_within_element_by_xpath(self, parent_element, child_xpath):
        print(" - DEBUG - click_button_within_element_by_xpath: ", child_xpath)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        button_xpath = f"//span[text()='{child_xpath}']"
        button = self._find_element_within_element(parent_element, By.XPATH, button_xpath)
        if button:
            button.click()
            print(" - INFO - Clicked button xpath: ", child_xpath)
            if self.captcha_id:
                # Handle Captcha
                self.handle_captcha_3(self.captcha_id, max_attempts = self.handle_captcha_attempts)
            return True
        else:
            print(" - WARNING - Clicked button xpath: ", child_xpath, " NOT FOUND")
            return False
    
    
    def get_element_by_id(self, element_id):
        print(" - DEBUG - get_element_by_id: ", element_id)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        return self._find_element(By.ID, element_id)
    def get_element_by_class_name(self, element_class):
        print(" - DEBUG - get_element_by_class_name: ", element_class)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        return self._find_element(By.CLASS_NAME, element_class)
    def get_element_by_xpath(self, element_xpath):
        print(" - DEBUG - get_element_by_xpath: ", element_xpath)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        button_xpath = f"//span[text()='{element_xpath}']"
        return self._find_element(By.XPATH, button_xpath)
    
    def get_element_within_element_by_id(self, parent_element, child_id):
        print(" - DEBUG - get_element_within_element_by_id: ", child_id)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        child_element = self._find_element_within_element(parent_element, By.ID, child_id)
        if child_element:
            print(f" - INFO - Element with ID '{child_id}' found within parent")
            return child_element
        else:
            print(f" - ERROR - [get_element_within_element_by_id()] Child element with ID '{child_id}' not found within the parent element.")
            return None
    def get_element_within_element_by_class_name(self, parent_element, child_class):
        print(" - DEBUG - get_element_within_element_by_class_name: ", child_class)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        child_element = self._find_element_within_element(parent_element, By.CLASS_NAME, child_class)
        if child_element:
            print(f" - INFO - Element with class name '{child_class}' found within parent")
            return child_element
        else:
            print(f" - ERROR - [get_element_within_element_by_class_name()] Child element with Class '{child_class}' not found within the parent element.")
            return None
    def get_element_within_element_by_xpath(self, parent_element, child_xpath):
        print(" - DEBUG - get_element_within_element_by_xpath: ", child_xpath)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        button_xpath = f"//span[text()='{child_xpath}']"
        child_element = self._find_element_within_element(parent_element, By.XPATH, button_xpath)
        if child_element:
            print(f" - INFO - Element with xpath '{child_xpath}' found within parent")
            return child_element
        else:
            print(f" - ERROR - [get_element_within_element_by_xpath()] Child element with XPATH '{child_xpath}' not found within the parent element.")
            return None
    
    
    def get_elements_by_id(self, element_id):
        print(" - DEBUG - get_elements_by_id: ", element_id)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        return self.driver.find_elements(By.ID, element_id)
    def get_elements_by_class_name(self, element_class):
        print(" - DEBUG - get_elements_by_class_name: ", element_class)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        return self.driver.find_elements(By.CLASS_NAME, element_class)
    def get_elements_by_xpath(self, element_xpath):
        print(" - DEBUG - get_elements_by_xpath: ", element_xpath)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button)
        
        button_xpath = f"//span[text()='{element_xpath}']"
        return self.driver.find_elements(By.XPATH, button_xpath)
    
    
    def wait_for_element_by_id(self, element_id, timeout=10):
        print(" - DEBUG - wait_for_element_by_id: ", element_id)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button-5)
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            print(f" - INFO - Element with ID '{element_id}' found within {timeout} seconds.")
            return element
        except:
            print(f" - WARNING - Element with ID '{element_id}' not found within {timeout} seconds.")
            return None
    def wait_for_element_by_class_name(self, class_name, timeout=10):
        print(" - DEBUG - wait_for_element_by_class_name: ", class_name)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button-5)
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            print(f" - INFO - Element with class name '{class_name}' found within {timeout} seconds.")
            return element
        except:
            print(f"- WARNING - Element with class name '{class_name}' not found within {timeout} seconds.")
            return None
    def wait_for_elememt_by_tag_name(self, tag_name, timeout=10):
        print(" - DEBUG - wait_for_elememt_by_tag_name: ", tag_name)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button-5)
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, tag_name))
            )
            print(f" - INFO - Element with tag name '{tag_name}' found within {timeout} seconds.")
            return element
        except:
            print(f" - WARNING - Element with tag name '{tag_name}' not found within {timeout} seconds.")
            return None
    def get_element_html_by_id(self, element_id):
        print(" - DEBUG - get_element_html_by_id: ", element_id)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button-5)
        
        element = self._find_element(By.ID, element_id)
        if element:
            return element.get_attribute("outerHTML")
        else:
            return None
    def get_element_html_by_class_name(self, class_name):
        print(" - DEBUG - get_element_html_by_class_name: ", class_name)
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button-5)
        
        element = self._find_element(By.CLASS_NAME, class_name)
        if element:
            return element.get_attribute("outerHTML")
        else:
            return None
    def get_page_source(self):
        print(" - DEBUG - get_page_source: ")
        # Sleep aprox self.wait_time_for_button seconds
        random_sleep_with_progress(self.wait_time_for_button-5)
        
        return self.driver.page_source



    def close(self):
        self.driver.quit()