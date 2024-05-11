def convert_from_f_string(original_string, value_dict):
    # This function takes the original string and a dictionary of variables

    # Define a function to replace placeholders with values
    def replace_placeholders(match):
        placeholder = match.group(1)  # Extract the placeholder name
        if placeholder in value_dict:
            return value_dict[placeholder]  # Replace with the variable value directly
        else:
            return match.group(0)  # If placeholder not found, keep it unchanged

    # Use regular expression to find all placeholders in the string
    import re
    pattern = r'{([^}]+)}'
    modified_string = re.sub(pattern, replace_placeholders, original_string)

    # Now, modified_string will contain the string with placeholders replaced
    return modified_string

# Example usage:
original_string = "#{MUNICIPALITY_SEARCH_ID} .{MUNICIPALITY_SECOND_MENU_CLASS_NAME} ul li a:contains('{MUNICIPALITY_SECOND_MENU_COMPRAR_TEXT}')"

# Define a dictionary with placeholder values
value_dict = {
    "MUNICIPALITY_SEARCH_ID": "search123",
    "MUNICIPALITY_SECOND_MENU_CLASS_NAME": "menuClass",
    "MUNICIPALITY_SECOND_MENU_COMPRAR_TEXT": "Comprar"
}

# Call the function to convert to f-string
resulting_f_string = convert_from_f_string(original_string, value_dict)

print(resulting_f_string)
