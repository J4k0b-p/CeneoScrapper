from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

@app.route('/')
def render_main_template():
    return render_template('main.html')

@app.route('/extraction')
def render_extraction_template():
    return render_template('extraction.html')

@app.route('/submit', methods=['POST'])
def handle_submit():
    product_id = request.form['extractionInput']
    print(product_id)
    return redirect("https://www.ceneo.pl/149239580")
   #TO DO - Change this redirect to try catch

if __name__ == '__main__':
    app.run(debug=True)