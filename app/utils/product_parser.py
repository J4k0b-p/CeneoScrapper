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

def get_product_name(product_id):
    product = get_product_data(product_id)
    return product['product_name']

def get_reviews_rate_data(product_id):
    reviews = get_product_reviews(product_id)
    rating_counts = {}
    rating_counts = {rate: 0 for rate in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]}
    for review in reviews:
        actual_rate = float(review['rate'])
        if actual_rate in rating_counts:
            rating_counts[actual_rate] += 1
        else:
            rating_counts[actual_rate] = 1
    return rating_counts

def get_recomendation_data(product_id):
    reviews = get_product_reviews(product_id)
    recomendation_counts = {}
    recomendation_counts = {"Polecam":0, "Nie polecam":0}
    for review in reviews:
        recomendation = review['recommendation']
        if recomendation in recomendation_counts:
            recomendation_counts[recomendation] += 1
        else:
            recomendation_counts[recomendation] = 1

    if "" in recomendation_counts:
        recomendation_counts["Bez rekomendacji"] = recomendation_counts[""]
        del recomendation_counts[""]

    return recomendation_counts

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