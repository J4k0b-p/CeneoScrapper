from flask import Flask, request, render_template, redirect,flash
from utils import scrapper
app = Flask(__name__)

@app.route('/')
def render_main_template():
    return render_template('main.html')

@app.route('/extraction')
def render_extraction_template():
    return render_template('extraction.html')

@app.route('/products')
def render_products_template():
    return render_template('products.html')

@app.route('/submit', methods=['POST'])
def handle_submit():
    product_id = request.form['extractionInput']
    return scrapper.get_data(product_id)

if __name__ == '__main__':
    app.run(debug=True)