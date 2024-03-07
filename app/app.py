from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def render_main_template():
    return render_template('main.html')

@app.route('/extraction')
def render_extraction_template():
    return render_template('extraction.html')

if __name__ == '__main__':
    app.run(debug=True)