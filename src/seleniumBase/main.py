from seleniumbase import SB
from seleniumbase.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

import json
import time
from tqdm import tqdm
from datetime import datetime
import os
import time

from utils.utils import print_section, random_sleep_with_progress, convert_from_f_string, explore_class
from utils.captcha_handeler import wait_for_captcha


with open('./src/seleniumBase/variables.json', 'r', encoding='utf-8') as json_file:
    VARIABLES_DICT = json.load(json_file)

with open('./src/seleniumBase/search_agregated_css_ids.json', 'r', encoding='utf-8') as json_file:
    SEARCH_PARAMS = json.load(json_file)
        
        
current_date = datetime.now() 
DATE = current_date.strftime('%Y%m%d')
    
TIME_WAIT_LONG = 30
TIME_WAIT_MEDIUM = 10
TIME_WAIT_SHORT = 5
TIME_WAIT_ULTRASHORT = 1


def click_botton_if_not_selected(sb, css_selector, text = ""):
    tqdm.write(css_selector)
    # wait for it
    elem = sb.find_element(css_selector)
    # Find if botton already selected
    new_css_selector = css_selector.replace('li a:contains','li:contains')
    elem_class = sb.find_element(new_css_selector).get_attribute("class")
    if elem_class != "actived":
        tqdm.write(f"{text} wasnt selected, clicking it now")
        # Click on it
        sb.driver.uc_click(css_selector)
        wait_for_captcha(sb, captcha_id = VARIABLES_DICT['CAPTCHA_ID'], max_attempts=10)
        random_sleep_with_progress(TIME_WAIT_ULTRASHORT, msg =f"After Clicked on {text}")
    else:
        tqdm.write(f"{text} already selected, skip clicking button")

def get_region_name(reg):
    try:
        reg_name = reg.find_element(By.CSS_SELECTOR, "a").text # Get the Name
    except Exception as e:
        # There is no <a> in provincia
        try:
            reg_name = reg.text
            if "\n" in reg_name:
                # there is a name and other extra text
                ll = reg_name.split("\n")
                if len(ll)==2:
                    # If there are 2 elements most likely a 0 with a name
                    try:
                        number = int(ll[0])
                        reg_name = ll[1]
                    except Exception as e:
                        reg_name = reg.text
        except Exception as e:
            reg_name = "Nan"
            pass
    try:
        number = reg.find_element(By.CSS_SELECTOR, "p").text # Get the Number
    except Exception as e:
        number = "Nan"
    return reg_name, number

def get_data_for_dict_queries(sb, search_params, out_path):
    i = 0
    for key, value in tqdm(search_params.items(), desc = "Extracting Data for buy/rent appartments"):
        tqdm.write(f" Getting data for {key}")
        
        for id, value in tqdm(value.items(), desc = f"Extracting Data for buy/rent appartments for {key}"):
            selection_name = value["selection_name"]
            second_menu_text = value["second_menu_text"]
            second_menu_selection = value["second_menu_selection"]
            third_menu_text = value["third_menu_text"]
            third_menu_selection = value["third_menu_selection"]
            fourth_menu_text = value["fourth_menu_text"]
            fourth_menu_selection = value["fourth_menu_selection"]
            save = value["save"]
            
            tqdm.write("\n")
            tqdm.write(f" Getting data for {selection_name}")

            # Select Second Menu
            css_selector = convert_from_f_string(second_menu_selection, value_dict = VARIABLES_DICT)
            click_botton_if_not_selected(sb, css_selector, text = second_menu_text)
            
            # Select Third Menu
            css_selector = convert_from_f_string(third_menu_selection, value_dict = VARIABLES_DICT)
            click_botton_if_not_selected(sb, css_selector, text = third_menu_text)
            
            if fourth_menu_text != "":
                # Select fourth Menu
                css_selector = convert_from_f_string(fourth_menu_selection, value_dict = VARIABLES_DICT)
                click_botton_if_not_selected(sb, css_selector, text = fourth_menu_text)

            ###################################################
            ## Get the data for the comunities and provinces ##
            ###################################################
             
            # Wait for the RESULTS to apear
            css_selector = f"#{VARIABLES_DICT['MUNICIPALITY_SEARCH_ID']} .{VARIABLES_DICT['MUNICIPALITY_LOCATIONS_LIST_MENU_CLASS_NAME']} > ul" # article ul
            comunidades = sb.find_elements(css_selector)
            text = {}
            for comunidad in tqdm(comunidades, desc = f"Iter Comunidades {selection_name}"):
                #print('\n\n\n')
                #explore_class(comunidad)
                #print('\n\n\n')
    
                provincias = comunidad.find_elements(By.CSS_SELECTOR, ".locations-list__links > li")
                comunidad_name = None
                comunidad_values = {}
                for provincia in tqdm(provincias, desc = f"Iter Provincias {selection_name}"):
                    provincia_name, number = get_region_name(provincia)
                        
                    if provincia_name =="Nan" and number =="Nan":
                        continue # If there is no number and  no text we continue
                    if comunidad_name is None and number =="Nan": # The first one is the comunidad name
                        comunidad_name = provincia_name
                        tqdm.write(f"Comunidad: {comunidad_name}")
                        continue 
                    
                    comunidad_values[provincia_name] = number
                
                if comunidad_name is None:
                    comunidad_name = f"Nan_{str(i)}"
                    i+=1
                
                text[comunidad_name] = comunidad_values
                
             
            ###################################################
            ###### Get the data for the special regions #######
            ###################################################   
            
            css_selector = f"#{VARIABLES_DICT['MUNICIPALITY_SEARCH_ID']} .{VARIABLES_DICT['MUNICIPALITY_LOCATIONS_LIST_MENU_CLASS_NAME']} > article" # article ul
            special_regions = sb.find_elements(css_selector)
            for special_region in tqdm(special_regions, desc = f"Iter Special Regions {selection_name}"):
                name = special_region.find_element(By.CSS_SELECTOR, ".location-list__special-regions > .outer-region-title").text
                regions = special_region.find_elements(By.CSS_SELECTOR, ".location-list__special-regions .locations-list__links > li")
                special_region_values = {}
                for region in tqdm(regions, desc = f"Iter Regions {selection_name}"):
                    provincia_name, number = get_region_name(region)
                    special_region_values[provincia_name] = number
                text[name] = special_region_values  
              
            # Save the results
            pp = os.path.join(out_path,save)
            with open(pp, "w", encoding="utf-8") as json_file:
                json.dump(text, json_file, ensure_ascii=False, indent=4)
            #break
        #break

def get_buyrentagencias_apartments_by_municipality(sb):
    out_path = f"./data/results/agregated/{DATE}"
    if not os.path.exists(out_path):
        # Create the folder if it doesn't exist
        os.makedirs(out_path)
        
        
    search_params_comprar = SEARCH_PARAMS["Comprar"]
    get_data_for_dict_queries(sb, search_params = search_params_comprar, out_path = out_path)
    
    search_params_alquilar = SEARCH_PARAMS["Alquilar"]
    get_data_for_dict_queries(sb, search_params = search_params_alquilar, out_path = out_path)
    
    search_params_agencias = SEARCH_PARAMS["Agencias"]
    get_data_for_dict_queries(sb, search_params = search_params_agencias, out_path = out_path)



def search_bar_tool(sb, css_type_BuyRent, css_house_type, location_name, type_of_location = "Provincia", order_by_price = True):
    ###################################################
    # Select Mode: "Comprar", "Alquiler", "Compartir" #
    ###################################################
    sb.driver.uc_click(css_type_BuyRent)
    random_sleep_with_progress(TIME_WAIT_ULTRASHORT, msg =f"After Clicked on {css_type_BuyRent}")
    
    ##################################################################################################################################################################
    # Select Type from dropdown menu:  Obra nueva, Viviendas, Habitación, Garajes, Trasteros, Oficinas, Locales o naves, Terrenos, Edificios. [Opcional: Vacacional] #
    ##################################################################################################################################################################
    # Open dropdown menu
    css_selector = '.form-typology-wrapper button'
    elem_class = sb.find_element(css_selector).get_attribute("class")
    #print(f"Element Class {elem_class}")
    if elem_class != "dropdown-wrapper active":
        # If button not active click it
        sb.driver.uc_click(css_selector)
    # Select Option
    sb.driver.uc_click(css_house_type)
    random_sleep_with_progress(TIME_WAIT_ULTRASHORT, msg =f"After Clicked on {css_house_type}")

    #####################
    # Select Provincia: #
    #####################
    # type text
    css_selector = '.form-item-block input[type="text"]'
    sb.type(css_selector, location_name, by="css selector", timeout=None)
    random_sleep_with_progress(TIME_WAIT_ULTRASHORT, msg =f"After Clicked on {css_selector}")
    
    # Search all autofill options and click the correct one
    css_selector = '.form-item-block .container-result-list .result-list ul li'
    options = sb.find_elements(css_selector)
    for index, option in enumerate(options):
        #print(f"Option text: {option.text}")
        location_name_searched = option.get_attribute("data-location")
        print(f"Location text: {location_name_searched}")
        css_selector = '.icon-location'
        type_of_location_searched = option.find_element(By.CSS_SELECTOR, css_selector).text
        print(f"Type of Location text: {type_of_location}")
        
        if type_of_location_searched == type_of_location and location_name_searched == location_name:
            print("---- MATCH ----")
            css_selector = f'.form-item-block .container-result-list .result-list ul li:nth-child({index+1}) a'
            sb.driver.uc_click(css_selector)
            random_sleep_with_progress(TIME_WAIT_ULTRASHORT, msg =f"After Clicked on {css_selector}")
            break
        
    ##########
    # Search #
    ##########
    # When we selected the area it autmaticaly search
    # Now we want to show the results for the enire area that we are looking for
    
    css_selector = '.show-all-link'
    sb.driver.uc_click(css_selector)
    random_sleep_with_progress(TIME_WAIT_ULTRASHORT, msg =f"After Clicked on {css_selector}")

    ##################
    # Order by Price #
    ##################
    if order_by_price:
        css_selector = '#order-by ul li [data-value="precios-asc"]'
        #sb.highlight(css_selector, by="css selector", loops=6)
        sb.driver.uc_click(css_selector)
        random_sleep_with_progress(TIME_WAIT_ULTRASHORT, msg =f"After Clicked on {css_selector}")

def get_info_by_area(sb):
    
    # Compra
    css_type_BuyRent = 'div.form-new-radio-button-wrapper fieldset.new-radio-button label[for="free-search-operation-sale"]'
    css_house_type = '.form-typology-wrapper ul.dropdown li[data-value="newdevelopment"]'
    location_name = 'Almería'
    search_bar_tool(sb, css_type_BuyRent, css_house_type, location_name, type_of_location = "Provincia")
    
    
    # Open the first house
    
    # Iter untill end
        # Read values
        # Save Values
        # Go to next
    
    
    
def main():
    with SB(uc=True, test=True) as sb:
        
        # ------------------------------------------------------------------------------------------------------------------
        # -------------------------------------------------  Open Website  -------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------------
        print_section(section_name = 'Open Website')
        
        # Open the website
        url = "https://www.idealista.com/"
        sb.driver.uc_open_with_reconnect(url, 20)
        
        wait_for_captcha(sb, captcha_id = VARIABLES_DICT['CAPTCHA_ID'], max_attempts=10)
        # Random wait
        random_sleep_with_progress(TIME_WAIT_ULTRASHORT, msg ="After Open Website")
        
        # ------------------------------------------------------------------------------------------------------------------
        # ------------------------------------------------- Reject Cookies -------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------------
        print_section(section_name = 'Reject Cookies')
        
        # Wait for the Cookies pop up to apear
        sb.wait_for_element(f"#{VARIABLES_DICT['REJECT_COOKIES_BUTTON_ID']}")
        
        # Reject cookies
        sb.driver.uc_click(f"#{VARIABLES_DICT['REJECT_COOKIES_BUTTON_ID']}")
        
        random_sleep_with_progress(TIME_WAIT_ULTRASHORT, msg ="After Reject Cookies")
        
        
        # ------------------------------------------------------------------------------------------------------------------
        # -------------------------------------------- Get Info by Municipality --------------------------------------------
        # ------------------------------------------------------------------------------------------------------------------
        print_section(section_name = 'Get Info by Municipality')
        
        
        #get_buyrentagencias_apartments_by_municipality(sb)
        
        #random_sleep_with_progress(TIME_WAIT_MEDIUM, msg ="After Get Info by Municipality")
        
        # ------------------------------------------------------------------------------------------------------------------
        # ------------------------------------------------- Search By Area -------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------------
        
        
        get_info_by_area(sb)
        #get_buyrentagencias_apartments_by_municipality(sb)
        
        random_sleep_with_progress(TIME_WAIT_MEDIUM, msg ="After search for the different areas")
    
if __name__ == "__main__":
    start = time.time()

    main()
    
    end = time.time()
    elapsed = end - start
    print(f"Execution time: {elapsed:.2f}")