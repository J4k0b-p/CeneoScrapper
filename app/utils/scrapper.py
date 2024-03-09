import requests
from flask import redirect
from bs4 import BeautifulSoup

def get_data(product_id):
    url = f"https://www.ceneo.pl/{product_id}"
    response = requests.get(url)

    if response.status_code == 500 or response.status_code == 404 :
        print("This is not valid product ID")
        #To do : Show alert message
        return redirect("/extraction")

    return redirect(f"https://www.ceneo.pl/{product_id}")