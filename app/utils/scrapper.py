import requests
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
        process_data(response)

    return redirect(f"https://www.ceneo.pl/{product_id}")

def process_data(response):
    soup = BeautifulSoup(response.content, 'html.parser')

    product_name_div = soup.find('div', class_ = 'product-top__title')
    reviews_amount_div = soup.find('div', class_ = 'score-extend__review')
    reviews_score_span = soup.find('span', class_ = 'product-review__score')  
    if product_name_div:
        print(product_name_div.text)
        print(reviews_amount_div.text)
        print(reviews_score_span.get('content', None))
