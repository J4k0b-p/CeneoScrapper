import requests
import math
from flask import redirect
from bs4 import BeautifulSoup


def get_data(product_id):
    url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
    response = requests.get(url)

    if response.status_code == 500 or response.status_code == 404 :
        print("This is not valid product ID")
        #To do : Show alert message
        return redirect("/extraction")
    elif response.status_code == 200:
        get_main_product_info(response)
        get_reviews_from_page(product_id,1)

    return redirect(f"https://www.ceneo.pl/{product_id}")

def get_main_product_info(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    product_name_div = soup.find('div', class_ = 'product-top__title')
    reviews_amount = soup.find('div', class_ = 'score-extend__review').text
    reviews_score_span = soup.find('span', class_ = 'product-review__score')  
    reviews = reviews_amount.split()
    print(product_name_div.text)
    print(reviews[0])
    print(reviews_score_span.get('content', None))



def get_reviews_pages_amount(amount):
    return math.ceil(amount / 10)

#spaghetti code  -- REFACTOR NEEDED
def get_reviews_from_page(product_id, page):
    url = f"https://www.ceneo.pl/{product_id}/opinie-{page}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        user_reviews = soup.find_all('div', class_ = "user-post user-post__card js_product-review")
        for review in user_reviews:
            review_id = review.get('data-entry-id')
            author_name = review.find('span', class_ = "user-post__author-name").text
            recomendation = review.find('span', class_ = "user-post__author-recomendation").find('em').text
            score = review.find('span', class_ = "user-post__score-count").text
            try:
                purchase_confirmation = bool(review.find('div', class_ = "review-pz").find("em").text)
            except:
                purchase_confirmation = False

            dates_span = review.find('span',class_ = "user-post__published").find_all('time')

            if len(dates_span) >= 2:
                rewiev_date = dates_span[0]['datetime']
                purchase_date = dates_span[1]['datetime']

            else:
                rewiev_date = dates_span[0]['datetime']               
                purchase_date = ""

            
            helpful_count = review.find('button', class_ = "vote-yes js_product-review-vote js_vote-yes")['data-total-vote']
            not_helpful_count = review.find('button', class_ = "vote-no js_product-review-vote js_vote-no")['data-total-vote']

            user_review = review.find('div', class_ = "user-post__text").text

            cons_pros_lists = soup.findAll('div', class_="review-feature__col")
            
            # ceneo devs no brainer
            # extracting lists to fix
            try:
                cons_list_test = cons_pros_lists[0]
                is_cons_check = bool(cons_list_test.find('div', class_='review-feature__title review-feature__title--positives', text='Zalety'))
                # check if first element is cons list 
                if(is_cons_check is not None):
                    cons_divs =  cons_list_test.findAll('div', class_='review-feature__item')
                    cons_list = [div.text for div in cons_divs ]
                else:
                    #first element is pros list
                    pros_list = cons_pros_lists[0]
                    pros_divs =  pros_list.findAll('div', class_='review-feature__item')
                    pros_list = [div.text for div in pros_divs ]

                #case when they are cons and pros
                pros_list = cons_pros_lists[1]
                pros_divs =  pros_list.findAll('div', class_='review-feature__item')
                pros_list = [div.text for div in pros_divs ]
                
            except:
                cons_list = []
                pros_list = []
            
            print(pros_list)

            cons_list = []
            pros_list = []



            


