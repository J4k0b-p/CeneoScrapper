import os
import json

def load_data():
    file_path = "ceneo_scrapper/app/static/scrapped_product_list.JSON"
    data = {'products': []}
    if os.path.exists(file_path):
        with open(file_path, 'r',encoding='utf-8') as file:
            data = json.load(file)
    
    return data

def get_product_data(product_id):
    data = load_data()
    for product in data['products']:
        if product['product_id'] == str(product_id):
            return product
        
def get_product_reviews(product_id):
    product = get_product_data(product_id)
    return product['reviews']

def append_product(new_product):
    file_path = "ceneo_scrapper/app/static/scrapped_product_list.JSON"
    data = {'products': []}
    if os.path.exists(file_path):
        with open(file_path, 'r',encoding='utf-8') as file:
            data = json.load(file)
    else:
        data['products'] = []

    #calculate total cons and pros per product
    total_pros = sum(len(review['pros']) for review in new_product['reviews'])
    total_cons = sum(len(review['cons']) for review in new_product['reviews'])
    new_product['total_pros'] = total_pros
    new_product['total_cons'] = total_cons

    data['products'].append(new_product)

    with open(file_path, 'w',encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4) 
        file.flush()



