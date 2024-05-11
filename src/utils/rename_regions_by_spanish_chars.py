import os
import json

def replace_keys(json_data, key_mapping):
    map_keys = list(key_mapping.keys())
    new_dict = {}
    
    for key, value in json_data.items():
        if key in map_keys:
            new_key = key_mapping[key]
        else:
            new_key = key
        new_dict[new_key] = json_data[key]
              
        if isinstance(value, dict):
            out = replace_keys(value, key_mapping)
            new_dict[new_key] = out
    return new_dict

def replace_keys_in_files(folder_path, key_mapping):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            #print(filename)
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                
                data = replace_keys(data, key_mapping)
                
                with open(file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data, json_file, ensure_ascii=False, indent=4)

                print(f"Replaced keys in: {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")


# Provide the path to the folder containing your JSON files
folder_path = './data/results/agregated/20240427'

key_mapping = {
    'Andalucia': 'Andalucía',
    'Almeria': 'Almería',
    'Cadiz': 'Cádiz',
    'Cordoba': 'Córdoba',
    'Jaen': 'Jaén',
    'Malaga': 'Málaga',
    'Aragon': 'Aragón',
    'Castilla y Leon': 'Castilla y León',
    'Avila': 'Ávila',
    'Leon': 'León',
    'Cataluna': 'Cataluña',
    'Castellon': 'Castellón',
    'Valencia': 'València',
    'Caceres': 'Cáceres',
    'A Coruna': 'A Coruña',
    'Pais Vasco': 'País Vasco',
    'Alava': 'Álava',
    'Guipuzcoa': 'Guipúzcoa',
    'Region de Murcia': 'Región de Murcia'
    # Add more key-value pairs as needed
}

# Call the function to replace keys in the folder
replace_keys_in_files(folder_path, key_mapping)