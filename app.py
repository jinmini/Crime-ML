from flask import Flask, render_template
from com.models.crime_controller import CrimeController

app = Flask(__name__)

@app.route('/') 
def home():
    controller = CrimeController()
    controller.modeling('cctv_in_seoul.csv', 'crime_in_seoul.csv', 'pop_in_seoul.xls')
    return render_template("index.html")

@app.route('/crimerate_ml')
def crimerate_ml():
    return render_template("/crimerate_ml.html")

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

app.config['TEMPLATES_AUTO_RELOAD'] = True
