from flask import Flask, request, render_template,make_response
from utils import scrapper, product_parser, charts
from bokeh.embed import components

import json

app = Flask(__name__)
app.secret_key = "hd834!#28HDFGjj"

@app.route('/')
def render_main_template():
    return render_template('main.html')

@app.route('/extraction/')
def render_extraction_template():
    return render_template('extraction.html')

@app.route('/products/')
def render_products_template():
    data = product_parser.load_data()
    return render_template('products.html', data=data)

@app.route('/product/<product_id>/')
def render_product_template (product_id):
    data = product_parser.get_product_data(product_id)
    return render_template('product_details.html', data=data, product_id = product_id)

@app.route('/submit/', methods=['POST'])
def handle_submit():
    product_id = request.form['extractionInput']
    return scrapper.get_data(product_id)

@app.route('/data-download/<product_id>')
def download_data(product_id):
    data = product_parser.get_product_data(product_id)
    response = make_response(json.dumps(data,ensure_ascii=False, indent=4))
    response.headers['Content-Type'] = 'application/json'
    response.headers["Content-Disposition"] = f"attachment; filename=data_{product_id}.json"
    return response

@app.route('/reviews-download/<product_id>')
def download_reviews(product_id):
    data = product_parser.get_product_reviews(product_id)
    response = make_response(json.dumps(data,ensure_ascii=False, indent=4))
    response.headers['Content-Type'] = 'application/json'
    response.headers["Content-Disposition"] = f"attachment; filename=reviews_{product_id}.json"
    return response


@app.route('/product/charts/<product_id>')
def render_charts_temnplate(product_id):
    product_name = product_parser.get_product_name(product_id)
    bar_chart = charts.create_bar_chart(product_id)
    bar_script, bar_div = components(bar_chart)
    dought_chart = charts.create_doughnut_chart(product_id)
    dought_script, dought_div = components(dought_chart)
    return render_template('product_charts.html', product_id=product_id, product_name = product_name, bar_script = bar_script, bar_div = bar_div, dought_script = dought_script, dought_div = dought_div)

@app.route('/about-me/')
def render_about_template():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)