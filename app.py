from flask import Flask, render_template, url_for, flash, redirect
#from forms import RegistrationForm, LoginForm
from variables import *
app = Flask(__name__)

desc_list = longDesc()

app.config['SECRET_KEY'] = 'd5fda74dcf2c2fdbfca06a4ebfc65b86a9e0da08d0115dce61f522f183b156d8'

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/docs')
def about():
    return render_template('docs.html', title='Docs')

@app.route('/algorithms')
def algorithms():
    return render_template('algorithms.html', title= 'Algoritmos', algos_list= algos_list)

@app.route('/algorithms/arima')
def algorithms_arima():
    text = desc_list['arima']

    return render_template('algorithms_arima.html', title='ARIMA', text=text)

@app.route('/algorithms/autocorrelation')
def algorithms_autocorrelation():
    text = desc_list['autocorrelation']

    return render_template('algorithms_arima.html', title='Autocorr', text=text)

if __name__ == '__main__':
    app.run(debug= True)
