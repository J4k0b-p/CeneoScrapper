import requests
import math
from flask import redirect
from bs4 import BeautifulSoup
import json
import os


def get_data(product_id):
    url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
    response = requests.get(url)

    if response.status_code == 500 or response.status_code == 404 :
        print("This is not valid product ID")
        #To do : Show alert message
        return redirect("/extraction")
    elif response.status_code == 200:
        process(product_id, response)

    return redirect(f"https://www.ceneo.pl/{product_id}")

def process(product_id,response):
    main_info = get_main_product_info(product_id,response)
    amount_of_pages = main_info["user_reviews_pages_amount"]
    main_info["reviews"] = []
    for i in range(1,amount_of_pages +1):
        reviews_from_page = get_reviews_from_page(product_id, i)
        main_info["reviews"].extend(reviews_from_page) 

    append_product(main_info)

def get_main_product_info(product_id,response):
    product_structure = {}

    soup = BeautifulSoup(response.content, 'html.parser')
    product_name_div = soup.find('div', class_ = 'product-top__title').text
    reviews_amount = soup.find('div', class_ = 'score-extend__review').text
    reviews_score_span = soup.find('span', class_ = 'product-review__score') 
    product_el = soup.find('img', class_ = "js_gallery-media gallery-carousel__media")
    product_image_src = product_el['src']
    reviews = reviews_amount.split()

    product_structure["product_name"] = product_name_div
    product_structure["product_id"] = product_id
    product_structure["product_image_src"] = product_image_src
    product_structure["reviews_amount"] = reviews[0]
    product_structure["reviews_avg_score"] = reviews_score_span.get('content', None)
    product_structure["user_reviews_pages_amount"] =  get_reviews_pages_amount(reviews[0])

    return product_structure


def get_reviews_pages_amount(amount):
    return math.ceil(int(amount) / 10)

#spaghetti code  -- REFACTOR NEEDED
def get_reviews_from_page(product_id, page):
    reviews = []
    url = f"https://www.ceneo.pl/{product_id}/opinie-{page}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        user_reviews = soup.find_all('div', class_ = "user-post user-post__card js_product-review")
        for review in user_reviews:
            review_id = review.get('data-entry-id')
            author_name = review.find('span', class_ = "user-post__author-name").text
            try:
                recomendation = review.find('span', class_ = "user-post__author-recomendation").find('em').text
            except:
                recomendation = ""
            score = review.find('span', class_ = "user-post__score-count").text
            try:
                purchase_confirmation = bool(review.find('div', class_ = "review-pz").find("em").text)
            except:
                purchase_confirmation = False

            dates_span = review.find('span',class_ = "user-post__published").find_all('time')

            if len(dates_span) >= 2:
                reviev_date = dates_span[0]['datetime']
                purchase_date = dates_span[1]['datetime']

            else:
                reviev_date = dates_span[0]['datetime']               
                purchase_date = ""

            
            helpful_count = review.find('button', class_ = "vote-yes js_product-review-vote js_vote-yes")['data-total-vote']
            not_helpful_count = review.find('button', class_ = "vote-no js_product-review-vote js_vote-no")['data-total-vote']

            user_review = review.find('div', class_ = "user-post__text").text

            review_feature_col = review.findAll('div', class_="review-feature__col")
            
            try:
                cons_list, pros_list = [], []
                if len(review_feature_col) == 1:
                    is_pros_check = bool(review_feature_col[0].find('div', class_='review-feature__title review-feature__title--positives'))
                    if is_pros_check:
                        pros_divs =  review_feature_col[0].findAll('div', class_='review-feature__item')
                        pros_list = [div.text for div in pros_divs ]
                    else:
                        cons_divs =  review_feature_col[0].findAll('div', class_='review-feature__item')
                        cons_list = [div.text for div in cons_divs ]
                elif len(review_feature_col) == 2:
                    is_pros_check = bool(review_feature_col[0].find('div', class_='review-feature__title review-feature__title--positives'))
                    if is_pros_check:
                        pros_divs =  review_feature_col[0].findAll('div', class_='review-feature__item')
                        pros_list = [div.text for div in pros_divs ]
                        cons_divs =  review_feature_col[1].findAll('div', class_='review-feature__item')
                        cons_list = [div.text for div in cons_divs ]
            except:
                # There is no cons_pros_list element
                pass

            review_structure = {
                "review_id": review_id,
                "author": author_name,
                "recommendation": recomendation,
                "stars": score,
                "is_purchase_confirmed": purchase_confirmation,
                "review_date": reviev_date,
                "purchase_date": purchase_date,
                "helpful_count": helpful_count,
                "not_helpful_count": not_helpful_count,
                "content": user_review,
                "cons": cons_list,
                "pros": pros_list
            }

            reviews.append(review_structure)
        return reviews
    
def append_product(new_product):
    file_path = "ceneo_scrapper/app/static/scrapped_product_list.JSON"
    data = {'products': []}
    if os.path.exists(file_path):
        with open(file_path, 'r',encoding='utf-8') as file:
            data = json.load(file)
    else:
        data['products'] = []

    data['products'].append(new_product)

    with open(file_path, 'w',encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4) 
        file.flush()
