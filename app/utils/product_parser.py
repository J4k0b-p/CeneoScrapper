import os
import json

def load_data():
    file_path = "ceneo_scrapper/app/static/scrapped_product_list.JSON"
    data = {'products': []}
    if os.path.exists(file_path):
        with open(file_path, 'r',encoding='utf-8') as file:
            data = json.load(file)
    
    return data


