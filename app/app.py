from flask import Flask, request, render_template, redirect,flash, make_response
from utils import scrapper, product_parser
import json

app = Flask(__name__)
app.secret_key = "hd834!#28HDFGjj"

@app.route('/')
def render_main_template():
    return render_template('main.html')

@app.route('/extraction')
def render_extraction_template():
    return render_template('extraction.html')

@app.route('/products')
def render_products_template():
    data = product_parser.load_data()
    return render_template('products.html', data=data)

@app.route('/submit', methods=['POST'])
def handle_submit():
    product_id = request.form['extractionInput']
    return scrapper.get_data(product_id)

@app.route('/data-download')
def download_data(product_id):
    data = {"key": "value"} 
    response = make_response(json.dumps(data))
    response.headers['Content-Type'] = 'application/json'
    response.headers["Content-Disposition"] = "attachment; filename=data.json"
    return response

if __name__ == '__main__':
    app.run(debug=True)