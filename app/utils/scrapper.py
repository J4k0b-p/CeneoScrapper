import requests, math
from utils import product_parser
from flask import redirect, flash
from bs4 import BeautifulSoup

def get_data(product_id):

    if product_id == "":
        show_error("Product ID can't be empty")
        return redirect("/extraction")
    
    url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
    response = requests.get(url)

    print(response.status_code)
    if response.status_code == 500 or response.status_code == 404 :
        show_error("Invalid product ID")
        return redirect("/extraction")
    elif response.status_code == 200:
        extract_all_data(product_id, response)

    return redirect(f"https://www.ceneo.pl/{product_id}")

def extract_all_data(product_id,response):
    main_info = extract_main_product_info(product_id,response)
    amount_of_pages = main_info["user_reviews_pages_amount"]
    main_info["reviews"] = []
    for i in range(1,amount_of_pages +1):
        reviews_from_page = extract_reviews_from_page(product_id, i)
        main_info["reviews"].extend(reviews_from_page) 

    product_parser.append_product(main_info)

def extract_main_product_info(product_id,response):
    product_structure = {}

    soup = BeautifulSoup(response.content, 'html.parser')
    product_name_div = soup.find('div', class_ = 'product-top__title').text
    reviews_amount = soup.find('div', class_ = 'score-extend__review').text
    reviews_score_span = soup.find('span', class_ = 'product-review__score') 
    product_el = soup.find('img', class_ = "js_gallery-media gallery-carousel__media")
    product_image_src = product_el['src']
    reviews = reviews_amount.split()

    product_structure["product_name"] = product_name_div.strip()
    product_structure["product_id"] = product_id
    product_structure["product_image_src"] = product_image_src
    product_structure["reviews_amount"] = reviews[0]
    product_structure["reviews_avg_score"] = reviews_score_span.get('content', None)
    product_structure["user_reviews_pages_amount"] =  get_reviews_pages_amount(reviews[0])

    return product_structure


def get_reviews_pages_amount(amount):
    return math.ceil(int(amount) / 10)

def extract_reviews_from_page(product_id, page):
    reviews = []
    url = f"https://www.ceneo.pl/{product_id}/opinie-{page}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        user_reviews = soup.find_all('div', class_ = "user-post user-post__card js_product-review")
        for review in user_reviews:
            review_id = extract_review_id(review)
            author_name = extract_autor_name(review)
            recomendation = extract_user_recomendation(review)
            rate = extract_product_rate(review)
            purchase_confirmation = extract_purchase_confirmation(review)
            review_date, purchase_date = extract_dates(review)
            helpful_count = extract_helpfull_count(review)
            not_helpful_count = extract_not_helpfull_count(review)
            user_review = extract_user_review(review)
            pros_list,cons_list = extract_cons_pros_list(review)
            review_structure = {
                "review_id": review_id,
                "author": author_name,
                "recommendation": recomendation,
                "rate": rate,
                "is_purchase_confirmed": purchase_confirmation,
                "review_date": review_date,
                "purchase_date": purchase_date,
                "helpful_count": helpful_count,
                "not_helpful_count": not_helpful_count,
                "content": user_review,
                "cons": cons_list,
                "pros": pros_list,
            }

            reviews.append(review_structure)
        return reviews
    
def show_error(msg):
    return flash(msg)

def extract_review_id(review):
    try:
        review_id = review.get('data-entry-id')
    except:
        review_id = ""
    return review_id

def extract_autor_name(review):
    try:
        author_name = review.find('span', class_ = "user-post__author-name").text
    except:
        author_name = ""
    return author_name.strip()

def extract_user_recomendation(review):
    try:
        recomendation = review.find('span', class_ = "user-post__author-recomendation").find('em').text
    except:
        recomendation = ""
    return recomendation

def extract_product_rate(review):
    try:
        score = review.find('span', class_ = "user-post__score-count").text
        rate = score.split('/')[0].replace(",",".")
    except:
        rate = ""
    return rate

def extract_purchase_confirmation(review):
    try:
        purchase_confirmation = bool(review.find('div', class_ = "review-pz").find("em").text)
    except:
        purchase_confirmation = False

    return purchase_confirmation

def extract_dates(review):
    dates_span = review.find('span',class_ = "user-post__published").find_all('time')

    if len(dates_span) >= 2:
        review_date = dates_span[0]['datetime']
        purchase_date = dates_span[1]['datetime']
    else:
        review_date = dates_span[0]['datetime']               
        purchase_date = ""
    
    return review_date, purchase_date

def extract_helpfull_count(review):
    try:
        helpfull_count = review.find('button', class_ = "vote-yes js_product-review-vote js_vote-yes")['data-total-vote']
    except:
        helpfull_count = ""
    
    return helpfull_count

def extract_not_helpfull_count(review):
    try:
        not_helpfull_count = review.find('button', class_ = "vote-no js_product-review-vote js_vote-no")['data-total-vote']
    except:
        not_helpfull_count = ""
    
    return not_helpfull_count

def extract_user_review(review):
    try:
        user_review = review.find('div', class_ = "user-post__text").text
    except:
        user_review = ""
    
    return user_review.strip()

def extract_cons_pros_list(review):
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
    return pros_list, cons_list