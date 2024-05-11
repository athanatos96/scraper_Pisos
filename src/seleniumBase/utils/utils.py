import time
import random
from tqdm import tqdm
import re

def print_section(section_name = ''):
    print("\n")
    print(f"\t\t -- SECTION -- {section_name}")
    print("\n")
    

def explore_class(class_var):
    print('\n\n\n')
    print("- Explore Class -")
    print("Class: ")
    print(class_var)
    print("Class type: ")
    print(type(class_var))
    print("Class functions: ")
    print(dir(class_var))
    print("Class atributes: ")
    print(class_var.__dict__.keys())
    print('\n\n\n')

def random_sleep_with_progress(total_seconds, msg=""):
    sleep_time = random.uniform(0.7, 1.3) * total_seconds
    sleep_time = max(sleep_time, 0.0)
    tqdm.write(f" - INFO - ({msg}) Sleep_time: {sleep_time:.2f} seconds" )
    for _ in tqdm(range(int(sleep_time * 10)), desc=f"Sleeping ({msg})", unit="milliseconds"):
        time.sleep(0.1)
    tqdm.write(f" - INFO - Sleep completed: {sleep_time:.2f} seconds")
    
    
    
def convert_from_f_string(original_string, value_dict):
    """
    Converts a formatted string (f-string) back to a template string with placeholders replaced by values.

    Parameters:
    original_string (str): The original formatted string containing placeholders in f-string format.
    value_dict (dict): A dictionary mapping placeholder names to their corresponding values.

    Returns:
    str: A template string where placeholders have been replaced with values from the value_dict.

    Example:
    original_string = "#{MUNICIPALITY_SEARCH_ID} .{MUNICIPALITY_SECOND_MENU_CLASS_NAME} ul li a:contains('{MUNICIPALITY_SECOND_MENU_COMPRAR_TEXT}')"
    value_dict = {
        "MUNICIPALITY_SEARCH_ID": "search123",
        "MUNICIPALITY_SECOND_MENU_CLASS_NAME": "menuClass",
        "MUNICIPALITY_SECOND_MENU_COMPRAR_TEXT": "Comprar"
    }
    resulting_template = convert_from_f_string(original_string, value_dict)
    # Output: "#search123 .menuClass ul li a:contains('Comprar')"
    """
    # This function takes the original string and a dictionary of variables

    # Define a function to replace placeholders with values
    def replace_placeholders(match):
        placeholder = match.group(1)  # Extract the placeholder name
        if placeholder in value_dict:
            return value_dict[placeholder]  # Replace with the variable value directly
        else:
            return match.group(0)  # If placeholder not found, keep it unchanged

    # Use regular expression to find all placeholders in the string
    pattern = r'{([^}]+)}'
    modified_string = re.sub(pattern, replace_placeholders, original_string)

    # Now, modified_string will contain the string with placeholders replaced
    return modified_string



