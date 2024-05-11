import time
import random

from scraper_class import WebScraper
from utils import random_sleep_with_progress

CAPTCHA_ID = 'captcha-container'
REJECT_COOKIES_BUTTON_ID = 'didomi-notice-disagree-button'
MUNICIPALITY_SEARCH_ID = 'municipality-search'
MUNICIPALITY_SECOND_MENU_CLASS_NAME = 'second-level-menu'
MUNICIPALITY_SECOND_MENU_COMPRAR_TEXT = 'Comprar'
MUNICIPALITY_SECOND_MENU_ALQUILAR_TEXT = 'Alquilar'
MUNICIPALITY_SECOND_MENU_AGENCIAS_TEXT = 'Agencias'
MUNICIPALITY_THIRD_MENU_CLASS_NAME = 'third-level-menu'


def get_obra_nueva():
    pass

def get_buy_appartemts_by_municipality(webScraper):
    # Get the municipality search section
    municipality_search = webScraper.get_element_by_id(MUNICIPALITY_SEARCH_ID)
    print(municipality_search.text)
    print('\n')
    
    # Get the second menu ("Comprar-Alquilar-Agencias")
    second_menu = webScraper.get_element_within_element_by_class_name(municipality_search, MUNICIPALITY_SECOND_MENU_CLASS_NAME)
    print('\n')
    
    # Sleep aprox 10 seconds
    random_sleep_with_progress(10)
    print('\n')
    
    # Click on the Comprar Section
    clicked = webScraper.click_button_within_element_by_xpath(parent_element = second_menu, child_xpath = MUNICIPALITY_SECOND_MENU_ALQUILAR_TEXT) # MUNICIPALITY_SECOND_MENU_COMPRAR_TEXT
    if clicked:
        print(" - INFO - Clicked on Comprar")
    else:
        print(" - ERROR - Didnt Clicked on Comprar")
        return
    print('\n')
    
    # Sleep aprox 10 seconds
    random_sleep_with_progress(30)
    print('\n')
    
    print(' - '*50)
    print(' Checking for captcha 3')
    print(' - '*50)
    webScraper.handle_captcha_3(captcha_id = CAPTCHA_ID)
    print(' - '*50)
    print()
    print(' - '*50)
    municipality_search = webScraper.get_element_by_id(MUNICIPALITY_SEARCH_ID)
    print(municipality_search.text)
    print('\n')
    
    
    # Sleep aprox 10 seconds
    random_sleep_with_progress(10)
    print('\n')
    

def main(webScraper):
    
    # wait for it to load
    wait_response = webScraper.wait_for_element_by_id(REJECT_COOKIES_BUTTON_ID, timeout = 30)
    
    if wait_response is None:
        #didnt load
        print(" - ERROR - Dint load cookies")
        return
    print('\n')
    
    # Sleep aprox 10 seconds
    random_sleep_with_progress(10)
    print('\n')
    
    
    # Close cookies pop up
    clicked = webScraper.click_button_by_id(REJECT_COOKIES_BUTTON_ID)
    if clicked:
        print(" - INFO - Closed Cookies by rejection")
    else:
        print(" - ERROR - Didnt close cookies")
        return
    print('\n')
    
    # Sleep aprox 30 seconds
    random_sleep_with_progress(10)
    print('\n')
    
    get_buy_appartemts_by_municipality(webScraper)
    print('\n')
    
    #time.sleep(10)    





if __name__ == "__main__":

    start = time.time()
    url = "https://www.idealista.com/"
    
    # Open Idealista
    idealista_webScraper = WebScraper(url = url,  headless = False, captcha_id = CAPTCHA_ID, handle_captcha_attempts = 10, wait_time_for_button = 2)
    print(" - INFO - Open the driver\n")
    
    try:
        main(idealista_webScraper)
    except Exception as e:
        print(" - ERROR - :")
        print(e)
    idealista_webScraper.close()
    
    
    
    
    end = time.time()
    execution_time = end-start
    print(f"\n\nExecution time: {execution_time:.2f} seconds")